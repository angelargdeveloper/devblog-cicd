# ================================
# ETAPA 1: IMAGEN BASE
# ================================
FROM python:3.11-slim

# ================================
# ETAPA 2: METADATOS
# ================================
LABEL maintainer="tu-email@ejemplo.com"
LABEL description="DevBlog - Aplicación de blog para aprender DevOps"
LABEL version="1.0"

# ================================
# ETAPA 3: CONFIGURACIÓN DEL SISTEMA
# ================================
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# ================================
# ETAPA 4: INSTALACIÓN DE DEPENDENCIAS
# ================================
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ================================
# ETAPA 5: COPIAR CÓDIGO DE LA APLICACIÓN
# ================================
COPY . .

# ================================
# ETAPA 6: CONFIGURACIÓN DE USUARIO
# ================================
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# ================================
# ETAPA 7: CONFIGURACIÓN DE RED
# ================================
EXPOSE 5000

# ================================
# ETAPA 8: COMANDO DE INICIO
# ================================
CMD ["python", "app.py"]