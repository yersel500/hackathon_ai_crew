# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos en el contenedor y lo instala
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación en el directorio de trabajo
COPY . .

# Expone el puerto que usará Flask (por defecto es el 5000)
EXPOSE 5000

# Establece la variable de entorno para especificar la aplicación principal de Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0  # Permite que Flask esté disponible fuera del contenedor

# Comando para ejecutar la aplicación Flask
CMD ["flask", "--app", "app","run", "--debug"]
