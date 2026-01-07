# 📚 Ejemplos de Uso de la API

> Guía práctica con ejemplos reales de cómo usar el Retail Backend API

---

## 📋 Tabla de Contenidos

- [Primeros Pasos](#primeros-pasos)
- [Autenticación](#autenticación)
- [Gestión de Productos](#gestión-de-productos)
- [Gestión de Compras](#gestión-de-compras)
- [Gestión de Ventas](#gestión-de-ventas)
- [Reportes](#reportes)
- [Casos de Uso Completos](#casos-de-uso-completos)

---

## Primeros Pasos

### Base URL

```
http://localhost:8000
```

### Documentación Interactiva

```
http://localhost:8000/docs
```

### Health Check

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "Retail Backend API - Sistema POS",
  "version": "1.0.0",
  "status": "active",
  "environment": "development"
}
```

---

## Autenticación

### 🔐 Login

**Endpoint:** `POST /auth/login`

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

### 🔑 Usar el Token

Incluye el token en el header `Authorization`:

```bash
curl -H "Authorization: Bearer eyJhbGci..." \
  "http://localhost:8000/products"
```

---

## Gestión de Productos

### 📦 Crear Producto

**Endpoint:** `POST /products`

```bash
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Coca-Cola 2L",
    "barcode": "7790001234567",
    "brand_id": 1,
    "price": 1250.50,
    "cost": 850.00,
    "stock_min": 10
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Coca-Cola 2L",
  "barcode": "7790001234567",
  "brand": {
    "id": 1,
    "name": "Coca-Cola"
  },
  "price": 1250.50,
  "cost": 850.00,
  "stock_min": 10,
  "stock_current": 0,
  "created_at": "2026-01-05T10:30:00Z"
}
```

### 📋 Listar Productos

**Endpoint:** `GET /products`

```bash
curl "http://localhost:8000/products?skip=0&limit=10" \
  -H "Authorization: Bearer {token}"
```

**Response:**
```json
{
  "total": 50,
  "items": [
    {
      "id": 1,
      "name": "Coca-Cola 2L",
      "barcode": "7790001234567",
      "price": 1250.50,
      "stock_current": 24,
      "brand": {
        "name": "Coca-Cola"
      }
    },
    {
      "id": 2,
      "name": "Pepsi 2L",
      "barcode": "7790002345678",
      "price": 1150.00,
      "stock_current": 18,
      "brand": {
        "name": "PepsiCo"
      }
    }
  ]
}
```

### 🔍 Buscar Producto por Barcode

**Endpoint:** `GET /products/barcode/{barcode}`

```bash
curl "http://localhost:8000/products/barcode/7790001234567" \
  -H "Authorization: Bearer {token}"
```

### ✏️ Actualizar Precio

**Endpoint:** `PATCH /products/{id}/price`

```bash
curl -X PATCH "http://localhost:8000/products/1/price" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "new_price": 1350.00
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Coca-Cola 2L",
  "price": 1350.00,
  "previous_price": 1250.50,
  "updated_at": "2026-01-05T11:00:00Z"
}
```

---

## Gestión de Compras

### 🛒 Registrar Compra

**Endpoint:** `POST /purchases`

```bash
curl -X POST "http://localhost:8000/purchases" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "provider_id": 1,
    "items": [
      {
        "product_id": 1,
        "quantity": 24,
        "unit_cost": 850.00
      },
      {
        "product_id": 2,
        "quantity": 12,
        "unit_cost": 780.00
      }
    ]
  }'
```

**Response:**
```json
{
  "id": 1,
  "provider": {
    "id": 1,
    "name": "Distribuidora Central"
  },
  "items": [
    {
      "product": {
        "id": 1,
        "name": "Coca-Cola 2L"
      },
      "quantity": 24,
      "unit_cost": 850.00,
      "subtotal": 20400.00
    },
    {
      "product": {
        "id": 2,
        "name": "Pepsi 2L"
      },
      "quantity": 12,
      "unit_cost": 780.00,
      "subtotal": 9360.00
    }
  ],
  "total": 29760.00,
  "created_at": "2026-01-05T09:00:00Z",
  "created_by": {
    "username": "admin"
  }
}
```

**Efecto:**
- ✅ Stock de Coca-Cola: 0 → 24
- ✅ Stock de Pepsi: 0 → 12
- ✅ Registro histórico de compra creado

### 📊 Historial de Compras

**Endpoint:** `GET /purchases`

```bash
curl "http://localhost:8000/purchases?from=2026-01-01&to=2026-01-31" \
  -H "Authorization: Bearer {token}"
```

---

## Gestión de Ventas

### 💰 Registrar Venta

**Endpoint:** `POST /sales`

```bash
curl -X POST "http://localhost:8000/sales" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_method": "cash",
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      },
      {
        "product_id": 2,
        "quantity": 1
      }
    ]
  }'
```

**Response:**
```json
{
  "id": 1,
  "receipt_number": "000001",
  "items": [
    {
      "product": {
        "id": 1,
        "name": "Coca-Cola 2L"
      },
      "quantity": 2,
      "unit_price": 1350.00,
      "subtotal": 2700.00
    },
    {
      "product": {
        "id": 2,
        "name": "Pepsi 2L"
      },
      "quantity": 1,
      "unit_price": 1150.00,
      "subtotal": 1150.00
    }
  ],
  "total": 3850.00,
  "payment_method": "cash",
  "created_at": "2026-01-05T14:30:00Z",
  "sold_by": {
    "username": "cajero01"
  }
}
```

**Efecto:**
- ✅ Stock Coca-Cola: 24 → 22
- ✅ Stock Pepsi: 12 → 11
- ✅ Precio congelado al momento de la venta

### 🧾 Consultar Venta

**Endpoint:** `GET /sales/{id}`

```bash
curl "http://localhost:8000/sales/1" \
  -H "Authorization: Bearer {token}"
```

### 📋 Listar Ventas del Día

**Endpoint:** `GET /sales/today`

```bash
curl "http://localhost:8000/sales/today" \
  -H "Authorization: Bearer {token}"
```

---

## Reportes

### 📊 Reporte de Ventas por Período

**Endpoint:** `GET /reports/sales`

```bash
curl "http://localhost:8000/reports/sales?from=2026-01-01&to=2026-01-31" \
  -H "Authorization: Bearer {token}"
```

**Response:**
```json
{
  "period": {
    "from": "2026-01-01",
    "to": "2026-01-31"
  },
  "summary": {
    "total_sales": 125,
    "total_amount": 485750.50,
    "average_ticket": 3886.00
  },
  "by_day": [
    {
      "date": "2026-01-05",
      "sales_count": 12,
      "total_amount": 45890.00
    }
  ],
  "top_products": [
    {
      "product": {
        "id": 1,
        "name": "Coca-Cola 2L"
      },
      "quantity_sold": 145,
      "revenue": 195750.00
    }
  ]
}
```

### 📦 Productos con Stock Bajo

**Endpoint:** `GET /reports/low-stock`

```bash
curl "http://localhost:8000/reports/low-stock" \
  -H "Authorization: Bearer {token}"
```

**Response:**
```json
{
  "products": [
    {
      "id": 5,
      "name": "Sprite 2L",
      "stock_current": 3,
      "stock_min": 10,
      "status": "critical"
    },
    {
      "id": 8,
      "name": "Fanta 2L",
      "stock_current": 8,
      "stock_min": 10,
      "status": "low"
    }
  ]
}
```

### 🏆 Top Productos Más Vendidos

**Endpoint:** `GET /reports/top-products`

```bash
curl "http://localhost:8000/reports/top-products?limit=10" \
  -H "Authorization: Bearer {token}"
```

### 💵 Ventas por Medio de Pago

**Endpoint:** `GET /reports/sales-by-payment`

```bash
curl "http://localhost:8000/reports/sales-by-payment?from=2026-01-01&to=2026-01-31" \
  -H "Authorization: Bearer {token}"
```

**Response:**
```json
{
  "data": [
    {
      "payment_method": "cash",
      "total_amount": 285400.00,
      "transaction_count": 78,
      "percentage": 58.7
    },
    {
      "payment_method": "card",
      "total_amount": 200350.50,
      "transaction_count": 47,
      "percentage": 41.3
    }
  ]
}
```

---

## Casos de Uso Completos

### 🎯 Escenario 1: Apertura de un Nuevo Negocio

```bash
# 1. Crear marcas
curl -X POST "http://localhost:8000/brands" \
  -H "Authorization: Bearer {token}" \
  -d '{"name": "Coca-Cola"}'

# 2. Crear proveedores
curl -X POST "http://localhost:8000/providers" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "name": "Distribuidora Central",
    "contact": "contacto@distribuidora.com",
    "phone": "+541112345678"
  }'

# 3. Crear productos
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "name": "Coca-Cola 2L",
    "barcode": "7790001234567",
    "brand_id": 1,
    "price": 1350.00,
    "cost": 850.00,
    "stock_min": 10
  }'

# 4. Primera compra (stock inicial)
curl -X POST "http://localhost:8000/purchases" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "provider_id": 1,
    "items": [
      {"product_id": 1, "quantity": 50, "unit_cost": 850.00}
    ]
  }'

# 5. Primera venta
curl -X POST "http://localhost:8000/sales" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "payment_method": "cash",
    "items": [
      {"product_id": 1, "quantity": 2}
    ]
  }'
```

### 🎯 Escenario 2: Actualización de Precios

```bash
# Usuario ve que un producto está muy barato
# 1. Consultar producto actual
curl "http://localhost:8000/products/1" \
  -H "Authorization: Bearer {token}"

# 2. Actualizar precio
curl -X PATCH "http://localhost:8000/products/1/price" \
  -H "Authorization: Bearer {token}" \
  -d '{"new_price": 1450.00}'

# 3. Nueva venta usa el nuevo precio
curl -X POST "http://localhost:8000/sales" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "items": [{"product_id": 1, "quantity": 1}]
  }'
# Esta venta registrará $1450.00, no $1350.00

# 4. Ventas anteriores mantienen su precio original
curl "http://localhost:8000/sales/1" \
  -H "Authorization: Bearer {token}"
# Esta venta sigue mostrando $1350.00
```

### 🎯 Escenario 3: Control de Stock

```bash
# 1. Ver productos con stock bajo
curl "http://localhost:8000/reports/low-stock" \
  -H "Authorization: Bearer {token}"

# 2. Realizar compra de reposición
curl -X POST "http://localhost:8000/purchases" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "provider_id": 1,
    "items": [
      {"product_id": 5, "quantity": 30, "unit_cost": 750.00}
    ]
  }'

# 3. Verificar que stock se actualizó
curl "http://localhost:8000/products/5" \
  -H "Authorization: Bearer {token}"
```

---

## Códigos de Estado HTTP

| Código | Significado | Cuándo se usa |
|--------|-------------|---------------|
| `200` | OK | Operación exitosa (GET, PUT, PATCH) |
| `201` | Created | Recurso creado (POST) |
| `204` | No Content | Eliminación exitosa (DELETE) |
| `400` | Bad Request | Datos inválidos |
| `401` | Unauthorized | Sin autenticación |
| `403` | Forbidden | Sin permisos |
| `404` | Not Found | Recurso no existe |
| `409` | Conflict | Conflicto (ej: barcode duplicado) |
| `422` | Unprocessable Entity | Validación falló |
| `500` | Internal Server Error | Error del servidor |

---

## Errores Comunes

### ❌ Error 401: No autenticado

```json
{
  "detail": "Not authenticated"
}
```

**Solución:** Incluir header `Authorization: Bearer {token}`

---

### ❌ Error 422: Validación falló

```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

**Solución:** Revisar que los datos cumplan las validaciones

---

### ❌ Error 409: Código de barras duplicado

```json
{
  "detail": "Product with barcode 7790001234567 already exists"
}
```

**Solución:** Usar un barcode único

---

## Mejores Prácticas

### ✅ Usar Paginación

```bash
# ❌ MAL - Puede traer miles de registros
curl "http://localhost:8000/products"

# ✅ BIEN - Traer de a páginas
curl "http://localhost:8000/products?skip=0&limit=20"
```

### ✅ Filtrar por Fechas

```bash
# Usar formato ISO para fechas
curl "http://localhost:8000/sales?from=2026-01-01&to=2026-01-31"
```

### ✅ Buscar por Barcode (no por ID)

```bash
# ✅ BIEN - En un POS real se escanea barcode
curl "http://localhost:8000/products/barcode/7790001234567"
```

---

## Próximos Pasos

✅ Ya conoces la API
➡️ Ver [Arquitectura del Sistema](./ARCHITECTURE.md)
➡️ Ver [Configuración de Neon](./NEON_SETUP.md)
➡️ Volver al [README principal](../README.md)

---

<div align="center">

**¿Necesitas más ejemplos?**
[Abre un issue](https://github.com/marceloemmott-dev/retail-backend-api/issues)

---

Ejemplos por [Marcelo Emmott](https://github.com/marceloemmott-dev)

</div>
