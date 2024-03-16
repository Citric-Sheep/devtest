# Usa la imagen oficial de Python
FROM python:latest

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias de la aplicación
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia el contenido actual del directorio al contenedor en /app
COPY . /app

# Expone el puerto 5000 para que la aplicación Flask pueda ser accesible desde fuera del contenedor
EXPOSE 5000

# Comando para ejecutar la aplicación Flask cuando se inicie el contenedor
# Comando para ejecutar la aplicación Flask cuando se inicie el contenedor
CMD ["python", "main.py"]
