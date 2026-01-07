# 🏗️ Arquitectura del Sistema

> Retail Backend API - Diseño, decisiones arquitectónicas y casos de uso

---

## 📋 Tabla de Contenidos

- [Visión General](#visión-general)
- [Principios de Diseño](#principios-de-diseño)
- [Arquitectura en Capas](#arquitectura-en-capas)
- [Modelo de Dominio](#modelo-de-dominio)
- [Casos de Uso](#casos-de-uso)
- [Flujos de Negocio](#flujos-de-negocio)
- [Decisiones Arquitectónicas](#decisiones-arquitectónicas)
- [Patrones de Diseño](#patrones-de-diseño)
- [Escalabilidad](#escalabilidad)

---

## Visión General

Este backend está diseñado como **núcleo universal para retail**, desacoplado de cualquier interfaz específica, permitiendo que múltiples clientes (POS desktop, web admin, mobile app) consuman la misma API con lógica de negocio consistente.

### Objetivo Principal

Proporcionar un sistema backend **realista y profesional** que replique el funcionamiento de sistemas empresariales de retail, no solo un CRUD básico.

---

## Principios de Diseño

### 🎯 Separación de Responsabilidades

```
┌─────────────────────────────────────────────┐
│         CLIENTE (cualquier tipo)            │
│   No conoce la lógica de negocio            │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST
┌──────────────────▼──────────────────────────┐
│              API LAYER                       │
│   FastAPI - Validación - Serialización      │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         SERVICE LAYER (Lógica)              │
│   Reglas de negocio - Validaciones         │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         DATA LAYER (Persistencia)           │
│   SQLAlchemy ORM - PostgreSQL               │
└─────────────────────────────────────────────┘
```

### 🔹 El Backend NO es el POS

- ❌ El backend **NO** sabe si es un kiosco, almacén o minimarket
- ❌ El backend **NO** renderiza interfaces
- ✅ El backend **EXPONE** reglas, datos y flujos de negocio
- ✅ Cualquier cliente consume la **MISMA API**

### 🌍 Universalidad

El sistema está diseñado para ser **agnóstico al tipo de negocio**:

```python
# ❌ MAL - Acoplado a un tipo de negocio
class KioskProduct:
    def apply_kiosk_discount(self):
        pass

# ✅ BIEN - Universal
class Product:
    def apply_discount(self, percentage):
        pass
```

---

## Arquitectura en Capas

### Capa 1: Routers (API Endpoints)

**Responsabilidad**: Recibir requests, validar entrada, llamar servicios, devolver respuestas.

```python
# Ejemplo conceptual
@router.post("/products", status_code=201)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    # 1. Validación automática por Pydantic ✅
    # 2. Llamar al servicio
    new_product = product_service.create(db, product)
    # 3. Retornar response
    return new_product
```

**Características:**
- ✅ Validación de entrada (Pydantic)
- ✅ Documentación automática (Swagger)
- ✅ Status codes HTTP apropiados
- ✅ Manejo de excepciones

---

### Capa 2: Services (Lógica de Negocio)

**Responsabilidad**: Implementar las reglas del dominio.

```python
# Ejemplo conceptual
class ProductService:
    def create(self, db: Session, product_data: ProductCreate):
        # 1. Validaciones de negocio
        if self.exists_by_barcode(db, product_data.barcode):
            raise ProductAlreadyExistsError()

        # 2. Aplicar reglas
        if product_data.price <= 0:
            raise InvalidPriceError()

        # 3. Persistir
        db_product = Product(**product_data.dict())
        db.add(db_product)
        db.commit()

        return db_product
```

**Reglas implementadas:**
- ✅ Validaciones de negocio
- ✅ Cálculos complejos
- ✅ Orquestación de operaciones
- ✅ Transacciones

---

### Capa 3: Models (Persistencia)

**Responsabilidad**: Definir estructura de datos y relaciones.

```python
# Ejemplo conceptual
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    barcode = Column(String(50), unique=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))

    # Relaciones
    brand = relationship("Brand", back_populates="products")
    stock_movements = relationship("StockMovement")
```

---

### Capa 4: Schemas (Contratos de API)

**Responsabilidad**: Definir qué datos entran y salen de la API.

```python
# Ejemplo conceptual
class ProductBase(BaseModel):
    name: str
    barcode: str
    price: Decimal

class ProductCreate(ProductBase):
    brand_id: int

class ProductResponse(ProductBase):
    id: int
    brand: BrandResponse
    created_at: datetime

    class Config:
        orm_mode = True
```

---

## Modelo de Dominio

### Entidades Principales

```
┌──────────────┐
│    Brand     │ (Marca del producto)
│ - id         │
│ - name       │
└──────┬───────┘
       │ 1
       │
       │ N
┌──────▼───────┐
│   Product    │ (Producto en catálogo)
│ - id         │
│ - name       │
│ - barcode    │
│ - price      │
│ - brand_id   │
└──────┬───────┘
       │
       ├─────────────┐
       │             │
       │ N           │ N
┌──────▼───────┐    ┌▼──────────────┐
│   Purchase   │    │  SaleDetail   │
│ (Compra)     │    │  (Venta)      │
└──────┬───────┘    └───────────────┘
       │
       │ N
┌──────▼───────┐
│   Provider   │ (Proveedor)
│ - id         │
│ - name       │
│ - contact    │
└──────────────┘
```

### 🔹 Diseño Cuidadoso: Marcas vs Proveedores

**Problema común**: Confundir marca con proveedor

```
❌ MAL DISEÑO:
Product → Provider (Coca-Cola es proveedor?)

✅ BUEN DISEÑO:
Product → Brand (Coca-Cola)
Purchase → Provider (Distribuidora XYZ que vende Coca-Cola)
```

**Justificación**:
- Una **marca** identifica el producto ("Coca-Cola")
- Un **proveedor** es quien te vende ese producto
- El **mismo producto** puede comprarse a **distintos proveedores**
- Cada **compra** registra el proveedor específico

---

## Casos de Uso

### 📍 Caso de Uso 1: Registro de Nueva Compra

**Actor**: Dueño/Administrador
**Objetivo**: Registrar compra de mercadería a un proveedor

**Flujo Principal:**

1. Usuario selecciona proveedor
2. Usuario agrega productos a la compra:
   - Producto
   - Cantidad
   - Costo unitario
3. Sistema calcula total automáticamente
4. Usuario confirma compra
5. **Sistema:**
   - ✅ Registra la compra histórica
   - ✅ **Incrementa stock** de cada producto
   - ✅ Almacena costo de la compra
   - ✅ Registra fecha y proveedor

**Reglas de Negocio:**
- La compra queda registrada como **evidencia histórica**
- El stock **no se inventa**, se construye desde compras
- Permite **auditoría** completa del negocio

---

### 📍 Caso de Uso 2: Venta en POS

**Actor**: Cajero
**Objetivo**: Registrar venta de productos a un cliente

**Flujo Principal:**

1. Cajero escanea productos (barcode)
2. Sistema muestra:
   - Nombre del producto
   - Precio actual
   - Stock disponible
3. Cajero ingresa cantidad
4. Sistema valida stock disponible
5. Cajero selecciona medio de pago
6. Cajero confirma venta
7. **Sistema:**
   - ✅ Registra la venta con **precio congelado**
   - ✅ **Descuenta stock** automáticamente
   - ✅ Asocia venta a cajero
   - ✅ Genera boleta interna

**Reglas de Negocio:**
- **Precio se congela** al momento de la venta
  - Si el precio cambia después, las ventas anteriores mantienen su precio
- Stock se valida **antes** de confirmar
- Cada venta registra **quién** la hizo (accountability)

---

### 📍 Caso de Uso 3: Actualización de Precio

**Actor**: Dueño/Administrador
**Objetivo**: Actualizar precio de venta de un producto

**Flujo Principal:**

1. Usuario busca producto
2. Usuario ingresa nuevo precio
3. Sistema actualiza precio
4. **Ventas futuras** usan el nuevo precio
5. **Ventas pasadas** mantienen su precio original

**Reglas de Negocio:**
- Ventas históricas son **inmutables**
- El precio es parte del registro de venta, no una referencia

```python
# ❌ MAL - Precio por referencia
class Sale:
    product_id: int  # Precio viene del producto actual

# ✅ BIEN - Precio congelado
class SaleDetail:
    product_id: int
    unit_price: Decimal  # Precio al momento de la venta
    quantity: int
```

---

### 📍 Caso de Uso 4: Consulta de Stock

**Actor**: Dueño/Empleado
**Objetivo**: Ver stock actual de productos

**Flujo Principal:**

1. Usuario consulta stock
2. Sistema muestra para cada producto:
   - Nombre
   - Stock actual
   - Stock mínimo (crítico)
   - Última compra
   - Última venta

**Reglas de Negocio:**
- El stock es **calculado**, no manual:
  ```
  Stock Actual = Σ Compras - Σ Ventas
  ```
- Se identifica **stock crítico** (bajo stock mínimo)
- Permite alertas proactivas

---

### 📍 Caso de Uso 5: Reporte de Ventas

**Actor**: Dueño
**Objetivo**: Analizar ventas por período

**Flujo Principal:**

1. Usuario selecciona período (fecha inicio/fin)
2. Sistema genera reporte:
   - Total vendido ($)
   - Cantidad de ventas
   - Productos más vendidos
   - Ventas por día
   - Ventas por cajero
   - Ventas por medio de pago

**Valor de Negocio:**
- 📈 Tomar decisiones basadas en datos
- 🎯 Identificar productos estrella
- 👥 Evaluar desempeño de cajeros
- 📅 Detectar patrones de venta

---

## Flujos de Negocio

### Flujo: Gestión de Stock

```
┌─────────────┐
│   COMPRA    │
│  (entrada)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   STOCK     │ ◄───┐
│  (actual)   │     │
└──────┬──────┘     │
       │            │
       ▼            │
┌─────────────┐     │
│    VENTA    │     │
│  (salida)   │     │
└──────┬──────┘     │
       │            │
       ▼            │
┌─────────────┐     │
│  AJUSTE     │─────┘
│  (opcional) │
└─────────────┘
```

**Características:**
- ✅ Stock **siempre rastreable**
- ✅ Trazabilidad completa
- ✅ Auditoría de movimientos
- ✅ Permite ajustes manuales con justificación

---

### Flujo: Ciclo de Vida del Producto

```
1. CREACIÓN
   ↓
2. ASIGNACIÓN DE MARCA
   ↓
3. PRIMERA COMPRA (producto entra al stock)
   ↓
4. VENTAS (producto sale del stock)
   ↓
5. RECOMPRA (se repone stock)
   ↓
6. ACTUALIZACIÓN DE PRECIO
   ↓
7. (OPCIONAL) DISCONTINUACIÓN
```

---

## Decisiones Arquitectónicas

### ¿Por qué FastAPI?

✅ **Alto rendimiento**: Basado en Starlette + Pydantic
✅ **Type hints nativos**: Validación automática
✅ **Async/await**: Concurrencia moderna
✅ **Documentación automática**: Swagger out-of-the-box
✅ **Comunidad activa**: Amplio ecosistema

### ¿Por qué PostgreSQL?

✅ **Relacional**: Perfecto para datos estructurados
✅ **ACID compliant**: Transacciones confiables
✅ **Maduro y probado**: Usado en Fortune 500
✅ **JSON support**: Flexibilidad cuando se necesita
✅ **Open source**: Sin vendor lock-in

### ¿Por qué Neon?

✅ **Serverless**: Zero configuración
✅ **Free tier generoso**: Perfecto para portafolios
✅ **Branching**: Desarrollo aislado
✅ **Auto-scaling**: Crece con el proyecto
✅ **Backups automáticos**: Seguridad incluida

### ¿Por qué SQLAlchemy?

✅ **ORM maduro**: Battle-tested
✅ **Migraciones**: Via Alembic
✅ **Type safety**: Con Python types
✅ **Relaciones complejas**: Bien soportadas
✅ **Raw SQL cuando sea necesario**: Flexibilidad

---

## Patrones de Diseño

### Repository Pattern

Abstraer acceso a datos:

```python
class GenericRepository:
    def get_by_id(self, id: int)
    def get_all(self, skip: int, limit: int)
    def create(self, obj)
    def update(self, obj)
    def delete(self, id: int)
```

### Service Layer Pattern

Encapsular lógica de negocio:

```python
class ProductService:
    def __init__(self, repository):
        self.repo = repository

    def create_with_validation(self, data):
        # Lógica de negocio aquí
        pass
```

### Dependency Injection

Via FastAPI Depends:

```python
@router.get("/products")
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pass
```

---

## Escalabilidad

### Preparado para Crecer

```
FASE 1 (Actual): Monolito Modular
  ↓
FASE 2: Cache Layer (Redis)
  ↓
FASE 3: Background Jobs (Celery)
  ↓
FASE 4: Microservicios (si es necesario)
```

### Estrategias de Optimización

**Base de Datos:**
- ✅ Índices en columnas frecuentemente consultadas
- ✅ Connection pooling
- ✅ Paginación en listados
- ✅ Queries optimizadas (evitar N+1)

**API:**
- ✅ Response caching
- ✅ Compresión (gzip)
- ✅ Rate limiting
- ✅ Async endpoints cuando corresponda

**Deployment:**
- ✅ Horizontal scaling (múltiples instancias)
- ✅ Load balancer
- ✅ CDN para assets estáticos
- ✅ Monitoreo proactivo

---

## Seguridad

### Medidas Implementadas/Planeadas

- 🔒 **Autenticación JWT**
- 🔒 **HTTPS obligatorio** (SSL)
- 🔒 **SQL Injection prevention** (ORM)
- 🔒 **CORS configurado**
- 🔒 **Rate limiting**
- 🔒 **Input validation** (Pydantic)
- 🔒 **Environment variables** (secretos)

---

## Próximos Pasos

✅ Entiendes la arquitectura
➡️ Ver [Configuración de Neon](./NEON_SETUP.md)
➡️ Ver [Ejemplos de API](./API_EXAMPLES.md)
➡️ Volver al [README principal](../README.md)

---

<div align="center">

**¿Preguntas sobre la arquitectura?**
[Abre un issue](https://github.com/marceloemmott-dev/retail-backend-api/issues)

---

Diseñado con 🧠 por [Marcelo Emmott](https://github.com/marceloemmott-dev)

</div>
