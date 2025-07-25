# ================================
# ETAPA 1: IMAGEN BASE
# ================================
FROM python:3.11-slim

# ================================
# ETAPA 2: METADATOS
# ================================
LABEL maintainer="angelarguijo18@gmail.com"
LABEL description="DevBlog - Aplicación de blog para aprender DevOps"
LABEL version="1.0"

# ================================
# ETAPA 3: CONFIGURACIÓN DEL SISTEMA
# ================================
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV PORT=5000
ENV FLASK_APP=app.py

WORKDIR /app

# ================================
# ETAPA 4: INSTALACIÓN DE DEPENDENCIAS
# ================================
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalar dependencias de forma más robusta
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

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/health || exit 1

EXPOSE $PORT

CMD ["python", "app.py"]