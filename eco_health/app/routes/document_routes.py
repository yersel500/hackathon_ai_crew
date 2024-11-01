from flask import Blueprint, request, jsonify, current_app, render_template
from flask_login import login_required, current_user
import requests
import hashlib
import os
import json
from werkzeug.utils import secure_filename
from ..models.document import Document, db
from dotenv import load_dotenv
import time

load_dotenv()

document_routes = Blueprint('document_routes', __name__)

# Azure configurations
DOCUMENT_INTELLIGENCE_URI = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
OCR_ENDPOINT = f"{DOCUMENT_INTELLIGENCE_URI}/documentintelligence/documentModels/prebuilt-read:analyze?api-version=2024-02-29-preview"
DOCUMENT_INTELLIGENCE_KEY = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
PII_URI = os.getenv('AZURE_PII_ENDPOINT')
PII_ENDPOINT = f"{PII_URI}/language/:analyze-text?api-version=2022-05-01"
PII_KEY = os.getenv('AZURE_PII_KEY')

def get_content_type(filename):
    """Determine content type based on file extension"""
    ext = filename.rsplit('.', 1)[1].lower()
    content_types = {
        'pdf': 'application/pdf',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg'
    }
    return content_types.get(ext, 'application/octet-stream')

def allowed_file(filename):
    """Check if file type is allowed"""
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_document_with_azure(file_content, filename):
    """Process document with Azure Document Intelligence"""
    try:
        content_type = get_content_type(filename)
        
        headers = {
            'Ocp-Apim-Subscription-Key': DOCUMENT_INTELLIGENCE_KEY,
            'Content-Type': content_type
        }
        
        current_app.logger.info(f"Processing file: {filename}")
        
        response = requests.post(
            OCR_ENDPOINT,
            headers=headers,
            data=file_content,
            timeout=30
        )
        
        current_app.logger.info(f"Initial response status: {response.status_code}")
        
        if response.status_code == 202:  # Asynchronous operation
            operation_location = response.headers.get('Operation-Location')
            if not operation_location:
                raise Exception("No Operation-Location header in response")
            
            current_app.logger.info(f"Polling operation at: {operation_location}")
            
            # Poll for result
            max_retries = 10
            for i in range(max_retries):
                time.sleep(1)  # Wait before checking
                poll_response = requests.get(
                    operation_location,
                    headers={'Ocp-Apim-Subscription-Key': DOCUMENT_INTELLIGENCE_KEY}
                )
                
                if poll_response.status_code != 200:
                    current_app.logger.error(f"Poll failed: {poll_response.text}")
                    continue
                
                result = poll_response.json()
                status = result.get('status')
                
                current_app.logger.info(f"Poll attempt {i+1}, status: {status}")
                
                if status == 'succeeded':
                    # Asegúrate de obtener el resultado correcto del documento
                    if 'analyzeResult' in result:
                        return result['analyzeResult']
                    return result
                    
                elif status == 'failed':
                    raise Exception(f"Document analysis failed: {result.get('error', {}).get('message')}")
                    
            raise Exception("Operation timed out")
            
        else:  # Synchronous response
            if not response.ok:
                raise Exception(f"Request failed: {response.status_code} - {response.text}")
                
            return response.json()
            
    except Exception as e:
        current_app.logger.error(f"Error processing document: {str(e)}")
        raise

def remove_pii(text):
    """Remove PII using Azure service"""
    headers = {
        'Ocp-Apim-Subscription-Key': PII_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'kind': 'PiiEntityRecognition',
        'parameters': {
            'modelVersion': 'latest',
            'domain': 'phi',
            'piiCategories': ['All']
        },
        'analysisInput': {
            'documents': [{
                'id': '1',
                'text': text,
                'language': 'es'
            }]
        }
    }
    
    try:
        current_app.logger.info("Sending text to PII removal service")
        current_app.logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

        
        response = requests.post(
            PII_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if not response.ok:
            current_app.logger.error(f"PII API error: {response.text}")
            raise Exception(f"PII API error: {response.status_code} - {response.text}")
            
        result = response.json()
        current_app.logger.debug(f"PII API response: {json.dumps(result, indent=2)}")
        
        # Procesar el resultado para remover PII
        redacted_text = text
        
        # Verificar la estructura de la respuesta
        if (result and 
            'results' in result and 
            'documents' in result['results'] and 
            len(result['results']['documents']) > 0 and 
            'entities' in result['results']['documents'][0]):
            
            entities = result['results']['documents'][0]['entities']
            # Ordenar entidades de más larga a más corta para evitar solapamientos
            entities.sort(key=lambda x: len(x.get('text', '')), reverse=True)
            
            for entity in entities:
                if 'text' in entity and 'category' in entity:
                    if entity['category'] in ['Person', 'Email', 'Phone', 'Address', 'SSN', 'URL', 'Age']:
                        redacted_text = redacted_text.replace(entity['text'], f'[REDACTED-{entity["category"]}]')
        
        current_app.logger.info(f"PII removal completed. Found {len(entities) if 'entities' in locals() else 0} entities.")
        return redacted_text
            
    except Exception as e:
        current_app.logger.error(f"Error removing PII: {str(e)}")
        current_app.logger.error(f"Response content: {response.text if 'response' in locals() else 'No response'}")
        raise

def extract_text_from_document(doc_results):
    """Extract text from document results"""
    try:
        current_app.logger.debug(f"Starting text extraction")
        text_parts = []

        # Si hay un array de 'spans' con contenido
        if isinstance(doc_results, dict) and 'spans' in doc_results:
            for span in doc_results['spans']:
                if 'content' in span:
                    text_parts.append(span['content'])

        # Si es una estructura con arrays de contenido
        elif isinstance(doc_results, dict) and isinstance(doc_results.get('content', []), list):
            for content_item in doc_results['content']:
                if isinstance(content_item, dict) and 'content' in content_item:
                    text_parts.append(content_item['content'])

        # Unir todo el texto
        extracted_text = ' '.join(text_parts)
        
        if not extracted_text:
            current_app.logger.error("No text could be extracted from the document")
            current_app.logger.error(f"Document results structure: {json.dumps(doc_results, indent=2)}")
            raise Exception("No text could be extracted from document")

        current_app.logger.info(f"Successfully extracted text: {extracted_text[:100]}...")  # Log first 100 chars
        return extracted_text

    except Exception as e:
        current_app.logger.error(f"Error extracting text: {str(e)}")
        current_app.logger.error(f"Document results: {json.dumps(doc_results, indent=2)}")
        raise

@document_routes.route('/upload-documents', methods=['POST'])
@login_required
def upload_documents():
    try:
        if 'documents' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        files = request.files.getlist('documents')
        results = []
        
        for file in files:
            if file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    file_content = file.read()
                    
                    current_app.logger.info(f"Processing file: {filename}")
                    
                    # Process with Document Intelligence
                    doc_results = process_document_with_azure(file_content, filename)
                    current_app.logger.info("Document processed successfully")
                    
                    # Convert results to string for PII processing
                    json_string = doc_results['content']
                    
                    # Remove PII from the JSON string
                    pii_removed = remove_pii(json_string)
                    
                    # Create document record
                    doc = Document(
                        user_id=current_user.id,
                        filename=filename
                    )
                    doc.set_content(pii_removed)
                    
                    db.session.add(doc)
                    results.append({
                        'filename': filename,
                        'status': 'success'
                    })
                    
                except Exception as e:
                    current_app.logger.error(f"Error processing file {filename}: {str(e)}")
                    results.append({
                        'filename': filename,
                        'status': 'error',
                        'error': str(e)
                    })
        
        if results:
            db.session.commit()
            return jsonify({
                'status': 'success',
                'results': results
            })
            
        return jsonify({'error': 'No valid files processed'}), 400
        
    except Exception as e:
        current_app.logger.error(f"Error in upload_documents: {str(e)}")
        return jsonify({'error': str(e)}), 500

@document_routes.route('/documents', methods=['GET'])
@login_required
def list_documents():
    try:
        documents = Document.query.filter_by(user_id=current_user.id).order_by(Document.uploaded_at.desc()).all()
        return render_template('auth/documentos.html', documents=documents)
    except Exception as e:
        current_app.logger.error(f"Error listing documents: {str(e)}")
        return render_template('auth/documentos.html', error="Error loading documents")