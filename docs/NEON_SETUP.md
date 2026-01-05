# ⚙️ Configuración de Base de Datos con Neon

> Guía completa paso a paso para configurar PostgreSQL serverless con Neon

---

## 📋 Tabla de Contenidos

- [¿Qué es Neon?](#qué-es-neon)
- [¿Por qué usar Neon?](#por-qué-usar-neon)
- [Configuración Paso a Paso](#configuración-paso-a-paso)
- [Solución de Problemas](#solución-de-problemas)
- [Mejores Prácticas](#mejores-prácticas)

---

## ¿Qué es Neon?

**Neon** es una plataforma de PostgreSQL serverless diseñada para la nube. Ofrece:

- 🚀 **Serverless**: Sin gestión de servidores
- ⚡ **Rápido**: Escalado automático instantáneo
- 💰 **Capa gratuita generosa**: Perfecta para desarrollo y portafolios
- 🔒 **Seguro**: SSL por defecto, backups automáticos
- 🌿 **Branches de BD**: Crea copias de tu BD como git branches

---

## ¿Por qué usar Neon?

### Para Proyectos de Portafolio

✅ **Demuestra experiencia con cloud**: No solo código local  
✅ **Production-ready**: Infraestructura real desde el inicio  
✅ **Gratis para proyectos pequeños**: Sin costos ocultos  
✅ **Fácil de mostrar**: Comparte tu proyecto funcionando  

### Ventajas Técnicas

- **Sin configuración de servidor**: Cero mantenimiento
- **SSL incluido**: Conexiones seguras por defecto
- **Backups automáticos**: Recover point in time
- **Monitoreo integrado**: Dashboard con métricas
- **API REST**: Automatización completa

---

## Configuración Paso a Paso

### 📝 Paso 1: Crear cuenta en Neon

1. Navega a [neon.tech](https://neon.tech/)
2. Haz clic en **"Sign Up"** o **"Get Started"**
3. Elige tu método de autenticación:
   - **GitHub** (recomendado para desarrolladores)
   - **Google**
   - **Email**
4. Confirma tu email si es necesario

> 💡 **Tip**: Usar GitHub permite integración directa con tus repos

---

### 🗄️ Paso 2: Crear un nuevo proyecto

1. Desde el dashboard, haz clic en **"Create a project"** o **"New Project"**

2. **Configura tu proyecto:**

   | Campo | Recomendación | Descripción |
   |-------|---------------|-------------|
   | **Project Name** | `retail-backend` | Nombre descriptivo de tu proyecto |
   | **Region** | Más cercana a ti | `US East (Ohio)`, `EU (Frankfurt)`, etc. |
   | **PostgreSQL Version** | 16 o superior | Usa la más reciente |
   | **Compute Size** | Compartido (Free tier) | Suficiente para desarrollo |

3. Haz clic en **"Create Project"**

4. **¡Listo!** Neon creará automáticamente:
   - Base de datos `neondb`
   - Usuario con credenciales
   - Connection string completa

---

### 🔌 Paso 3: Obtener la Connection String

#### Opción A: Desde la pantalla de creación

Después de crear el proyecto, Neon muestra inmediatamente la connection string.

#### Opción B: Desde el Dashboard

1. Ve a **Dashboard** → Tu proyecto
2. Haz clic en **"Connection Details"** o **"Connect"**
3. Selecciona:
   - **Database**: `neondb`
   - **Role**: (tu usuario por defecto)
   - **Compute**: (el compute creado)

4. La connection string se verá así:

```
postgresql://username:password@ep-xxxxx-xxxxx.region.aws.neon.tech/neondb?sslmode=require
```

#### Componentes de la Connection String

```
postgresql://[username]:[password]@[host]/[database]?sslmode=require
              ^^^^^^^^   ^^^^^^^^   ^^^^^^  ^^^^^^^^
              Usuario    Password   Host    BD Name
```

> ⚠️ **IMPORTANTE**: 
> - Guarda esta string de forma **segura**
> - Nunca la compartas públicamente
> - Nunca la subas a GitHub en `.env`

---

### 🔐 Paso 4: Configurar el archivo `.env`

1. En tu proyecto, copia `.env.example` a `.env`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

2. Abre `.env` y pega tu connection string:

```env
ENV=development
DEBUG=true
DATABASE_URL=postgresql://username:password@ep-xxxxx-xxxxx.region.aws.neon.tech/neondb?sslmode=require
```

3. **Verifica que incluya:**
   - ✅ `?sslmode=require` al final
   - ✅ No hay espacios extras
   - ✅ Password sin caracteres especiales problemáticos

> 💡 **Tip**: Si tu password tiene caracteres especiales (`@`, `#`, `&`, etc.), puede necesitar URL encoding.

---

### ✅ Paso 5: Verificar la conexión

El proyecto incluye un script de prueba:

```bash
# Asegúrate de tener el entorno virtual activo
python test_db.py
```

#### Salida Exitosa

```
✅ Conexión exitosa a la base de datos
Versión de PostgreSQL: PostgreSQL 16.x on x86_64-pc-linux-gnu
```

#### Si hay error

```
❌ Error de conexión
Error: could not translate host name "..." to address
```

→ Ver [Solución de Problemas](#solución-de-problemas)

---

### 📊 Paso 6: Explorar tu base de datos

#### SQL Editor (En Neon Dashboard)

Neon incluye un editor SQL integrado:

1. Dashboard → Tu proyecto → **"SQL Editor"**
2. Puedes ejecutar queries directamente:

```sql
-- Ver versión de PostgreSQL
SELECT version();

-- Crear tabla de ejemplo
CREATE TABLE test (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- Ver todas las tablas
SELECT tablename FROM pg_tables WHERE schemaname = 'public';
```

#### Monitoreo

En el dashboard también puedes ver:
- 📈 **Métricas de uso**: CPU, memoria, almacenamiento
- 🔍 **Logs de conexiones**: Quién se conectó y cuándo
- 💾 **Storage usado**: Cuánto espacio ocupas
- ⏱️ **Query performance**: Queries más lentas

---

## Solución de Problemas

### ❌ Error: "could not translate host name"

**Causa**: Connection string incorrecta o problemas de red

**Solución**:
1. Verifica que copiaste la connection string completa
2. Revisa que no haya espacios al inicio/final
3. Verifica tu conexión a internet

---

### ❌ Error: "password authentication failed"

**Causa**: Credenciales incorrectas

**Solución**:
1. Regenera la password en Neon:
   - Dashboard → Settings → Reset password
2. Copia la nueva connection string
3. Actualiza tu `.env`

---

### ❌ Error: "SSL required"

**Causa**: Falta `sslmode=require` en la connection string

**Solución**:

Asegúrate de que tu `DATABASE_URL` termine con:
```
?sslmode=require
```

Si ya tiene otros parámetros:
```
?other_param=value&sslmode=require
```

---

### ❌ Error: "too many connections"

**Causa**: Límite de conexiones alcanzado (raro en free tier)

**Solución**:
1. Cierra conexiones no usadas
2. En el dashboard: Operations → Restart compute
3. Revisa tu código por connection leaks

---

## Mejores Prácticas

### 🔒 Seguridad

✅ **NUNCA** subas `.env` a GitHub  
✅ Usa `.gitignore` para excluir archivos sensibles  
✅ Rota passwords periódicamente  
✅ Usa variables de entorno en producción  
✅ Limita acceso por IP si es posible (en plan Pro)  

### ⚡ Rendimiento

✅ **Connection pooling**: Usa SQLAlchemy pool  
✅ **Índices**: Crea índices en columnas frecuentes  
✅ **Cierra conexiones**: No dejes conexiones abiertas  
✅ **Prepared statements**: SQLAlchemy lo hace automáticamente  

### 💰 Optimización de Recursos (Free Tier)

✅ **Monitora almacenamiento**: Solo tienes 3GB  
✅ **Limpia datos de prueba**: No ocupes espacio innecesario  
✅ **Usa branches**: Para testing sin afectar main  
✅ **Revisa métricas**: Dashboard → Metrics  

---

## Características Avanzadas

### 🌿 Database Branching

Neon permite crear "branches" de tu BD como Git:

```bash
# Crear branch desde el dashboard
# Se crea una copia completa de tu BD
```

**Casos de uso:**
- Testing de migraciones
- Desarrollo de features
- Staging environments

### 📸 Point-in-Time Recovery

Restaura tu BD a cualquier punto en el tiempo:

1. Dashboard → Settings → Recovery
2. Selecciona timestamp
3. Crea restore point

### 🔄 Autoscaling

Neon escala automáticamente basado en carga:
- Sube CPU cuando hay más queries
- Baja recursos cuando está idle
- Zero-downtime scaling

---

## Recursos Adicionales

- 📚 [Documentación oficial de Neon](https://neon.tech/docs)
- 💬 [Discord de Neon](https://discord.gg/neon)
- 🎓 [Tutoriales en YouTube](https://www.youtube.com/@neondatabase)
- 📖 [Blog de Neon](https://neon.tech/blog)

---

## Comparación con Alternativas

| Característica | Neon | Supabase | Railway | Render |
|----------------|------|----------|---------|--------|
| PostgreSQL Serverless | ✅ | ✅ | ❌ | ❌ |
| Free tier | 3GB | 500MB | ❌ | 90 días |
| Branches de BD | ✅ | ❌ | ❌ | ❌ |
| SSL incluido | ✅ | ✅ | ✅ | ✅ |
| Auto-scaling | ✅ | ⚠️ | ⚠️ | ❌ |
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## Preguntas Frecuentes

### ¿Cuánto cuesta Neon?

**Free Tier (para siempre):**
- 1 proyecto
- 10 branches
- 3 GB storage
- Shared compute
- **$0/mes**

**Pro ($19/mes):**
- Proyectos ilimitados
- Autoscaling avanzado
- Más almacenamiento
- IP allowlisting

### ¿Puedo migrar desde otra BD?

Sí, hay varias opciones:
1. **pg_dump/pg_restore** (tradicional)
2. **Import desde Neon CLI**
3. **Replication continua** (Pro)

### ¿Es confiable para producción?

✅ Sí, usado por miles de empresas  
✅ SLA del 99.9% (en plan Pro)  
✅ Backups automáticos  
✅ Monitoreo 24/7  

### ¿Puedo usar con ORMs?

✅ SQLAlchemy (Python) - **Este proyecto**  
✅ Prisma (Node.js)  
✅ Django ORM (Python)  
✅ TypeORM (TypeScript)  
✅ Cualquier driver PostgreSQL estándar  

---

## Próximos Pasos

✅ Configuraste Neon exitosamente  
➡️ Continúa con [Arquitectura del Proyecto](./ARCHITECTURE.md)  
➡️ Ver [Ejemplos de API](./API_EXAMPLES.md)  
➡️ Volver al [README principal](../README.md)  

---

<div align="center">

**¿Problemas con la configuración?**  
[Abre un issue](https://github.com/marceloemmott-dev/retail-backend-api/issues) y te ayudaremos

---

Documentado con ❤️ por [Marcelo Emmott](https://github.com/marceloemmott-dev)

</div>
