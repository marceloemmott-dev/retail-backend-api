# 🏪 Retail Backend API

> Backend universal para negocios retail pequeños y medianos - Sistema POS desacoplado y reutilizable

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## 📖 Tabla de Contenidos

- [🧠 Historia y Contexto](#-historia-y-contexto)
- [🎯 Motivación](#-motivación)
- [✨ Características Principales](#-características-principales)
- [🏗️ Arquitectura](#️-arquitectura)
- [🛠️ Stack Tecnológico](#️-stack-tecnológico)
- [🚀 Instalación y Configuración](#-instalación-y-configuración)
- [📚 Documentación API](#-documentación-api)
- [🗂️ Estructura del Proyecto](#️-estructura-del-proyecto)
- [🌍 Universalidad del Sistema](#-universalidad-del-sistema)
- [🔐 Usuarios y Roles](#-usuarios-y-roles)
- [📊 Reportería](#-reportería)
- [🔜 Roadmap](#-roadmap)
- [👤 Autor](#-autor)
- [📄 Licencia](#-licencia)

---

## 🧠 Historia y Contexto

Este proyecto nace a partir de una **necesidad real**: contar con un **backend universal** para negocios retail pequeños y medianos, como kioscos, almacenes o tiendas de barrio, que pueda ser **reutilizado por distintos tipos de clientes** (software de escritorio, aplicaciones web o móviles) sin depender de una interfaz específica.

La idea central no fue construir un simple CRUD, sino **diseñar un sistema backend con lógica de negocio real**, inspirado en cómo funcionan los puntos de venta (POS) y los sistemas internos de gestión en empresas reales.

### 🎯 Motivación

En muchos negocios pequeños, la gestión de productos, stock, compras y ventas se realiza de forma manual o con herramientas poco estructuradas (planillas Excel, sistemas cerrados o soluciones difíciles de adaptar).

Este proyecto busca resolver ese problema creando:

- ✅ Un **backend desacoplado del frontend**
- ✅ Capaz de **servir como núcleo central del negocio**
- ✅ **Reutilizable** para distintos escenarios:
  - 🖥️ POS de escritorio
  - 🌐 Panel web del dueño
  - 📱 Aplicación móvil
  - 🔌 Futuras integraciones

---

## ✨ Características Principales

### 🏷️ Diseño del Dominio (pensado como sistema real)

Durante el diseño se tomó especial cuidado en no cometer errores comunes:

#### 🔹 Marcas vs Proveedores
- Las **marcas** identifican al producto (ej: Maravilla, Coca-Cola)
- Los **proveedores** son quienes venden esos productos al negocio
- Un mismo producto puede comprarse a distintos proveedores
- El sistema mantiene historial completo de compras

#### 🔹 Compras y Stock
- El stock **no se "inventa"**, se construye a partir de **compras reales**
- Cada compra queda registrada como evidencia histórica
- Permite auditoría y análisis a futuro

#### 🔹 Ventas y Boletas Internas
- El sistema maneja **boletas internas de venta**, no documentos tributarios
- Cada venta:
  - ✅ Descuenta stock automáticamente
  - ✅ Queda asociada a productos, cantidades y usuario
  - ✅ Registra medio de pago
  - ✅ **Congela el precio** al momento de la venta

---

## 🏗️ Arquitectura

### Enfoque Arquitectónico

Desde el inicio, el proyecto se planteó con una **separación clara de responsabilidades**:

```
┌─────────────────────────────────────────────┐
│         CLIENTES (Múltiples)                │
├─────────────────────────────────────────────┤
│  🖥️ POS Desktop  │  🌐 Web Panel  │ 📱 Mobile │
└───────────┬─────────────────┬───────────┬───┘
            │                 │           │
            └────────┬────────┴───────────┘
                     │
            ┌────────▼────────┐
            │   REST API       │
            │   (FastAPI)      │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │  Lógica de      │
            │  Negocio        │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │  PostgreSQL      │
            │  (Neon Cloud)    │
            └─────────────────┘
```

**Principios clave:**
- 🔹 El backend **NO es el POS**
- 🔹 El backend **no conoce la interfaz**
- 🔹 El backend **expone reglas, datos y flujos de negocio**
- 🔹 Cualquier cliente consume **la misma API**

Esto permite que el sistema sea **escalable, mantenible y profesional**, incluso si el frontend cambia completamente en el futuro.

---

## 🛠️ Stack Tecnológico

| Tecnología | Descripción |
|------------|-------------|
| **[FastAPI](https://fastapi.tiangolo.com/)** | Framework moderno y de alto rendimiento para construir APIs |
| **[Python 3.11+](https://www.python.org/)** | Lenguaje de programación principal |
| **[SQLAlchemy](https://www.sqlalchemy.org/)** | ORM para manejo de la base de datos |
| **[PostgreSQL](https://www.postgresql.org/)** | Base de datos relacional |
| **[Neon](https://neon.tech/)** | PostgreSQL serverless en la nube |
| **[Pydantic](https://docs.pydantic.dev/)** | Validación de datos y schemas |
| **[Uvicorn](https://www.uvicorn.org/)** | Servidor ASGI de alto rendimiento |
| **[Swagger/OpenAPI](https://swagger.io/)** | Documentación automática de la API |

---

## 🚀 Instalación y Configuración

### Prerequisitos

- Python 3.11 o superior
- PostgreSQL (local o cuenta en [Neon](https://neon.tech/))
- Git

### ⚙️ Ejecución Local (Desarrollo)

#### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/marceloemmott/retail-backend-api.git
cd retail-backend-api
```

#### 2️⃣ Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configurar variables de entorno

Crear archivo `.env` basado en `.env.example`:

```env
ENV=development
DEBUG=true
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
```

> 💡 **Nota:** Para usar Neon, copia la connection string desde tu panel de Neon

#### 5️⃣ Levantar el servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: **http://localhost:8000**

---

## 📚 Documentación API

Una vez el servidor esté corriendo, puedes acceder a la documentación interactiva:

### 📘 Swagger UI (Recomendado)
👉 **http://localhost:8000/docs**

### � ReDoc
👉 **http://localhost:8000/redoc**

Ambas interfaces permiten:
- ✅ Explorar todos los endpoints disponibles
- ✅ Ver schemas de request/response
- ✅ Probar la API directamente desde el navegador

---

## 🗂️ Estructura del Proyecto

```
retail-backend-api/
├── 📁 app/
│   ├── 📁 core/           # Configuración central
│   │   ├── config.py      # Variables de entorno
│   │   └── database.py    # Conexión a BD
│   ├── 📁 models/         # Modelos SQLAlchemy
│   ├── 📁 schemas/        # Schemas Pydantic
│   ├── 📁 routers/        # Endpoints de la API
│   ├── 📁 services/       # Lógica de negocio
│   └── main.py            # Punto de entrada
├── 📄 .env                # Variables de entorno (no versionado)
├── 📄 .env.example        # Ejemplo de configuración
├── 📄 .gitignore          # Archivos ignorados por git
├── 📄 requirements.txt    # Dependencias Python
├── 📄 test_db.py          # Script de prueba de conexión
└── 📄 README.md           # Este archivo
```

---

## 🌍 Universalidad del Sistema

El backend fue diseñado para ser **agnóstico al tipo de negocio**, evitando reglas rígidas o nombres específicos.

No importa si el sistema se usa en:
- 🏪 Un kiosco
- 🛒 Un almacén
- 🏬 Una tienda pequeña
- 🏪 Un minimarket

**El modelo siempre es el mismo:**
- 📦 Productos
- 🏷️ Marcas
- 🚚 Proveedores
- 📥 Compras
- 💰 Ventas
- 📊 Stock
- 📈 Reportes

> **El negocio cambia, el backend no.**

---

## 🔐 Usuarios y Roles

El proyecto contempla distintos tipos de usuarios:

| Rol | Responsabilidades |
|-----|-------------------|
| **👑 Dueño/Administrador** | Gestiona productos, stock, proveedores y reportes |
| **👤 Cajero/Empleado** | Realiza ventas y consulta productos |

Esto replica el funcionamiento real de un sistema POS empresarial.

---

## 📊 Reportería

Uno de los focos principales del proyecto es la **reportería**, ya que es ahí donde el backend entrega **verdadero valor al negocio**.

El sistema está pensado para permitir:

- 📈 Historial de ventas por producto
- 🚚 Historial de compras por proveedor
- 📦 Stock actual y stock crítico
- 🏆 Productos más vendidos
- 📅 Análisis por períodos de tiempo

Toda esta información se expone mediante **endpoints listos** para ser consumidos por un dashboard web en el futuro.

---

## 🔜 Roadmap

### ✅ Fase 1: Fundamentos (Completado)
- [x] Estructura base profesional
- [x] Configuración DEV / PROD
- [x] Conexión real a base de datos en la nube (Neon)
- [x] Documentación automática (Swagger)

### � Fase 2: Modelos y Persistencia (En Progreso)
- [ ] Crear modelos de dominio (Brand, Product, Provider, etc.)
- [ ] Implementar migraciones con Alembic
- [ ] Persistencia real en PostgreSQL

### 📅 Fase 3: Endpoints de Negocio (Próximamente)
- [ ] CRUD de productos y marcas
- [ ] Gestión de compras y proveedores
- [ ] Sistema de ventas y boletas
- [ ] Control de stock automático

### 📅 Fase 4: Reportería Avanzada
- [ ] Endpoints de reportes
- [ ] Análisis de ventas
- [ ] Estadísticas de stock
- [ ] Historial de compras

### 📅 Fase 5: Producción
- [ ] Despliegue en producción
- [ ] CI/CD
- [ ] Monitoreo y logs
- [ ] Tests automatizados

---

## 👤 Autor

Desarrollado con ❤️ como proyecto de portafolio profesional

**Marcelo Emmott Sanchez**

[![GitHub](https://img.shields.io/badge/GitHub-marceloemmott-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/marceloemmott)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Marcelo%20Emmott-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marcelo-emmott)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## ⭐ Agradecimientos

- **[FastAPI](https://fastapi.tiangolo.com/)** por su excelente framework
- **[Neon](https://neon.tech/)** por proporcionar PostgreSQL serverless
- **[SQLAlchemy](https://www.sqlalchemy.org/)** por su poderoso ORM
- A todos los que contribuyen con feedback y mejoras

---

<div align="center">

### ⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐

**¿Tienes sugerencias o encontraste un bug?**  
[Abre un issue](https://github.com/marceloemmott/retail-backend-api/issues) o envía un pull request

---

Hecho con 💻 y ☕ por [Marcelo Emmott](https://github.com/marceloemmott)

</div>