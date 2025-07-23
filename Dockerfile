# ================================
# ETAPA 1: IMAGEN BASE
# ================================
FROM python:3.11-slim as builder

# ================================
# ETAPA 2: METADATOS
# ================================
LABEL maintainer="angelarguijo18@gmail.com"
LABEL description="DevBlog - Aplicación de blog para aprender DevOps"
LABEL version="1.0"

# ================================
# ETAPA 3: CONFIGURACIÓN DEL SISTEMA
# ================================
# PYTHONDONTWRITEBYTECODE=1: Evita crear archivos .pyc (optimización)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
#AGREGAR PARA PRODUCCION
ENV FLASK_ENV=production
ENV PORT=5000

WORKDIR /app

# ================================
# ETAPA 4: INSTALACIÓN DE DEPENDENCIAS
# ================================
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
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
# Configuración de usuario
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/health || exit 1

# ================================
# ETAPA 7: CONFIGURACIÓN DE RED
# ================================
EXPOSE $PORT

# ================================
# ETAPA 8: COMANDO DE INICIO
# ================================
CMD ["python", "app.py"]