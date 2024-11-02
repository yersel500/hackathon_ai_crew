# 🌍 EcoHealth - Tu Asistente Personal de Salud Ambiental

## 🌟 Acerca de EcoHealth
EcoHealth es una plataforma innovadora que integra datos de calidad del aire en tiempo real con tu perfil médico personal para proporcionarte recomendaciones personalizadas y proteger tu salud. Utilizando inteligencia artificial avanzada, EcoHealth analiza múltiples factores para ofrecerte alertas y consejos adaptados a tus condiciones médicas específicas.

## ⭐ Arquitectura del Proyecto

- Azure OpenAI
- Document Intelligence
- PII
- Web app services
- Azure database for Postgresql
- Docker
- Azure Container Registry
- Virtual Networks
- Azure Bastion
- Load Balancers
- AI Studio
- Key Vault

![hackathon5png drawio](https://github.com/user-attachments/assets/e6e5c651-9717-4a2c-882a-1821ca4f3206)


## ✨ Características Principales

### 🤖 Asistente IA Personalizado
- Chat en tiempo real impulsado por GPT-4
- Recomendaciones personalizadas basadas en tus condiciones médicas
- Análisis contextual de tus documentos médicos
- Conteo de tokens para optimizar las interacciones

### 📊 Monitoreo de Calidad del Aire
- Datos en tiempo real de la calidad del aire en tu ubicación
- Visualización interactiva de métricas de contaminación
- Alertas personalizadas basadas en tus condiciones de salud

### 📋 Gestión de Documentos Médicos
- Carga segura de documentos médicos (PDF, imágenes)
- Procesamiento automático con Azure Document Intelligence
- Anonimización automática de información sensible
- Encriptación de extremo a extremo

### 🗺️ Visualización Geoespacial
- Mapa interactivo de calidad del aire
- Identificación de zonas de riesgo
- Recomendaciones basadas en tu ubicación

## 🛡️ Seguridad y Privacidad
- Encriptación de datos médicos
- Anonimización automática de información personal
- Cumplimiento con estándares de privacidad médica
- Retención de datos controlada (60 días)

## 🚀 Tecnologías Utilizadas
- **Frontend**: HTML5, TailwindCSS
- **Backend**: Python, Flask
- **Base de Datos**: PostgreSQL
- **IA & ML**: Azure OpenAI, Azure Document Intelligence
- **Seguridad**: Fernet Encryption
- **APIs**: EPA AirNow

## 📌 Requisitos del Sistema
```python
Python >= 3.8
PostgreSQL >= 12
Node.js >= 14 (para TailwindCSS)
```


## 🛠️ Instalación

### Clonar el repositorio

```bash
git clone git@github.com:yersel500/hackathon_ai_crew.git
cd ecohealth
```

### Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### Inicializar la base de datos

```bash
flask db upgrade
```

### Ejecutar la aplicación

```bash
flask run
```

## 📊 Capturas de Pantalla
[Incluir 3-4 capturas de pantalla de las características principales]

## 🌱 Próximas Características

- Notificaciones push para alertas de calidad del aire
- Análisis predictivo de riesgos de salud
- Expansión a más ciudades y regiones
- Reportes personalizados de salud ambiental
- Rutas de trafico para movilizarse por zonas menos contaminadas
- Agregar más puntos de medición
- Agregar nuevos parámetros como: Temperatura, Radiación, etc

## 🤝 Contribuir
¡Agradecemos al equipo de Código Facilito por el soporte durante el proceso de desarrollo de la Hackaton, y en especial a Evelyn y Tomás por la asesoría brindada, que ha sido de gran ayuda para la realización del proyecto.

## 📄 Licencia
Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📬 Contacto
- Demian Hernandez: duhr@ciencias.unam.mx
- Yersel Hurtado: yersel500@gmail.com


## 🏗️ Infraestructura

La carpeta `Infra` contiene todos los archivos necesarios para configurar y desplegar la infraestructura del proyecto en Azure a traves de Biceps. A continuación se describe el contenido de esta carpeta y su propósito:

### Contenido de la carpeta `infra`

- **modules**: Contiene los archivos del despliegue automático de los recuros de azure usando Infraestructura como Código(IAAC) a traves de Biceps.
- **deploy.sh**: Script para realizar el flujo del despliegue de la arquitecura.
- **main.bicep**: Archivo bicep principal para el despliegue de la arquitectura
- **main.bicepparam**: Tiene que ser modificado por el usuario, colocando sus propios parámetros.

### Despliegue de la Infraestructura

Para desplegar la infraestructura, sigue estos pasos:

#### Step 1: Clonar el Repositorio

Empieza clonando el repositorio en tu máquina local:

```bash
git clone https://github.com/yersel500/hackathon_ai_crew
cd bicep
```

#### Step 2: Configurar Parámetros

Edit the [main.bicepparam](./main.bicepparam) parameters file:
Location
ObjectID: Azure Entra
prefix and suffix


#### Step 3: Despliega los Recursos

Usa el script Bash [deploy.sh](./deploy.sh) para desplegar los recursos de Azure a través de Bicep. Este script aprovisionará todos los recursos necesarios según lo definido en las plantillas Bicep.

Ejecuta el siguiente comando para desplegar los recursos:

```bash
./deploy.sh --resourceGroupName <resource-group-name> --location <location> --virtualNetworkResourceGroupName <client-virtual-network-resource-group-name>
./deploy.sh --resourceGroupName azureservices4 --location canadaeast --virtualNetworkResourceGroupName vnetgroup4
```



<p align="center">
  Made with ❤️ for a healthier environment by AI Crew team
</p>
