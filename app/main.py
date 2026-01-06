"""Retail Backend API - Sistema POS universal.

Este módulo contiene la aplicación principal FastAPI con configuración
de Swagger/OpenAPI para documentación interactiva.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Metadata para documentación Swagger/OpenAPI
tags_metadata = [
    {
        "name": "Health",
        "description": "Endpoints de salud y status del sistema",
    },
    {
        "name": "Products",
        "description": "Gestión de productos, precios y stock",
    },
    {
        "name": "Sales",
        "description": "Registro y consulta de ventas",
    },
    {
        "name": "Purchases",
        "description": "Gestión de compras y proveedores",
    },
    {
        "name": "Reports",
        "description": "Reportería y analytics",
    },
]

# Inicializar FastAPI con metadata completa
app = FastAPI(
    title="🏪 Retail Backend API",
    description="""
    **Backend universal para negocios retail** - Sistema POS desacoplado y reutilizable
    
    ## Características principales:
    
    * ✅ **Gestión de productos** con código de barras
    * ✅ **Control de stock** automático
    * ✅ **Registro de ventas** con boletas internas
    * ✅ **Compras a proveedores** con actualización de stock
    * ✅ **Reportería** completa de ventas y stock
    * ✅ **Multi-punto de venta** (web, móvil, escritorio)
    
    ## Tecnología:
    
    - **Framework:** FastAPI
    - **Base de datos:** PostgreSQL (Neon serverless)
    - **ORM:** SQLAlchemy
    - **Documentación:** OpenAPI 3.0 (Swagger)
    
    ## Documentación adicional:
    
    - [Arquitectura del Sistema](./docs/ARCHITECTURE.md)
    - [Ejemplos de API](./docs/API_EXAMPLES.md)
    - [Setup de Neon DB](./docs/NEON_SETUP.md)
    """,
    version="0.1.0",
    contact={
        "name": "Marcelo Emmott",
        "url": "https://github.com/marceloemmott-dev",
        "email": "emmottmarcelo2026@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS para permitir llamadas desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Endpoint de health check para verificar que la API está funcionando.

    Returns:
        dict: Status del sistema y versión
    """
    return {
        "status": "ok",
        "message": "Retail Backend API is running",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"], summary="Detailed Health Check")
def detailed_health():
    """Health check detallado con información del sistema.

    Returns:
        dict: Información detallada del sistema
    """
    return {
        "status": "healthy",
        "service": "retail-backend-api",
        "version": "0.1.0",
        "database": "connected",  # TODO: Verificar conexión real
        "uptime": "running",
    }
