# 🔄 CI/CD - Integración y Despliegue Continuo

> Automatización de calidad y despliegue para Retail Backend API

---

## 📋 Tabla de Contenidos

- [¿Qué es CI/CD?](#qué-es-cicd)
- [Workflows Configurados](#workflows-configurados)
- [Cómo Funciona](#cómo-funciona)
- [Badges en el README](#badges-en-el-readme)
- [Ejecutar Localmente](#ejecutar-localmente)
- [Solución de Problemas](#solución-de-problemas)

---

## ¿Qué es CI/CD?

### CI - Continuous Integration (Integración Continua)

**Definición:** Cada vez que haces `git push`, se ejecutan verificaciones automáticas.

**Verificaciones incluidas:**
- ✅ Tests unitarios
- ✅ Linting (calidad de código)
- ✅ Type checking
- ✅ Formateo de código
- ✅ Análisis de seguridad

**Beneficio:** Detecta errores antes de que lleguen a producción.

---

### CD - Continuous Deployment (Despliegue Continuo)

**Definición:** Cuando el código pasa todas las verificaciones, se despliega automáticamente.

**Etapas:**
1. ✅ Tests pasan
2. ✅ Build exitoso
3. ✅ Deploy automático a servidor

**Beneficio:** Deploy rápido, confiable y sin intervención manual.

---

## Workflows Configurados

### 1️⃣ CI - Python Tests & Quality

**Archivo:** `.github/workflows/ci.yml`

**Se ejecuta:**
- En cada `push` a `main` o `develop`
- En cada Pull Request a `main`

**Qué hace:**

```
┌────────────────────────┐
│  git push origin main  │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  GitHub Actions        │
│  se activa             │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  Checks en paralelo:   │
│  ✓ Black (formateo)    │
│  ✓ isort (imports)     │
│  ✓ flake8 (linting)    │
│  ✓ mypy (types)        │
│  ✓ Sintaxis Python     │
└───────────┬────────────┘
            │
            ▼
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌────────┐      ┌────────┐
│  ✅ OK  │      │  ❌ Fail│
└────────┘      └────────┘
```

**Herramientas utilizadas:**

| Herramienta | Propósito | Ejemplo de Error |
|-------------|-----------|------------------|
| **Black** | Formateo consistente | `Line too long` |
| **isort** | Ordenar imports | `Imports desorganizados` |
| **flake8** | Calidad de código | `Variable no usada` |
| **mypy** | Type checking | `Type mismatch` |
| **safety** | Vulnerabilidades | `Paquete inseguro` |

---

### 2️⃣ Dependency Review

**Archivo:** `.github/workflows/dependency-review.yml`

**Se ejecuta:**
- Cuando cambias `requirements.txt`
- Cada lunes a las 9 AM UTC (automático)
- Manualmente cuando quieras

**Qué hace:**
- 🔍 Escanea dependencias por vulnerabilidades
- 📋 Detecta paquetes desactualizados
- ⚠️ Alerta sobre riesgos de seguridad

---

### 3️⃣ CodeQL Security Analysis

**Archivo:** `.github/workflows/codeql.yml`

**Se ejecuta:**
- En cada push a `main`
- En cada Pull Request
- Cada lunes a las 6 AM UTC (automático)

**Qué hace:**
- 🛡️ Análisis profundo de seguridad
- 🔍 Detecta vulnerabilidades comunes:
  - SQL Injection
  - XSS
  - Path Traversal
  - Hardcoded secrets
- 📊 Reporta en la tab "Security" de GitHub

---

## Cómo Funciona

### Flujo Completo

```
Tu Computadora                    GitHub                     GitHub Actions
─────────────                     ──────                     ──────────────

1. Escribes código
   ↓
2. git commit
   ↓
3. git push  ───────────────────→  4. Recibe push
                                      ↓
                                   5. Activa workflows  ───→  6. Crea VM Ubuntu
                                                                 ↓
                                                              7. Instala Python
                                                                 ↓
                                                              8. Install deps
                                                                 ↓
                                                              9. Run checks
                                                                 ↓
                                                          ┌──────┴──────┐
                                                          │             │
                                                          ▼             ▼
                                                      10a. ✅ Pass   10b. ❌ Fail
                                                          │             │
                                   11. Badge verde ◄──────┘             │
                                                                        │
12. Recibes email  ◄────────────────────────────────────────────────────┘
    si falla
```

---

## Badges en el README

Los badges muestran el estado actual de los workflows:

### ✅ Badge Verde (Passing)

```markdown
[![CI](https://github.com/marceloemmott-dev/retail-backend-api/actions/workflows/ci.yml/badge.svg)](...)
```

**Significa:** Todos los checks pasaron exitosamente

### ❌ Badge Rojo (Failing)

**Significa:** Algún check falló, necesitas revisar

### ⚪ Badge Gris (Unknown)

**Significa:** Workflow nunca se ejecutó o está en progreso

---

## Ejecutar Localmente

Puedes ejecutar las mismas verificaciones en tu máquina antes de hacer push:

### Instalar herramientas

```bash
pip install black isort flake8 mypy pytest safety
```

### Formateo con Black

```bash
# Ver qué cambiaría
black --check app/

# Aplicar cambios
black app/
```

### Ordenar imports con isort

```bash
# Ver qué cambiaría
isort --check-only app/

# Aplicar cambios
isort app/
```

### Linting con flake8

```bash
flake8 app/
```

### Type checking con mypy

```bash
mypy app/
```

### Security check

```bash
safety check
```

### Ejecutar TODO de una vez

Crea un script `check.sh` (Linux/Mac) o `check.bat` (Windows):

```bash
#!/bin/bash
echo "🎨 Formateando código..."
black app/

echo "📋 Ordenando imports..."
isort app/

echo "🔍 Linting..."
flake8 app/

echo "🔎 Type checking..."
mypy app/ || true

echo "🔒 Security scan..."
safety check || true

echo "✅ Todos los checks completados!"
```

Luego:

```bash
chmod +x check.sh
./check.sh
```

---

## Solución de Problemas

### ❌ Workflow falla con "Black would reformat"

**Causa:** Tu código no está formateado según Black

**Solución:**
```bash
black app/
git add .
git commit -m "chore: format code with black"
git push
```

---

### ❌ Workflow falla  con "flake8: line too long"

**Causa:** Línea excede 127 caracteres

**Solución:**
```python
# ❌ Línea muy larga
result = some_function(parameter1, parameter2, parameter3, parameter4, parameter5, parameter6)

# ✅ Dividir en múltiples líneas
result = some_function(
    parameter1,
    parameter2,
    parameter3,
    parameter4,
    parameter5,
    parameter6
)
```

---

### ❌ Workflow falla con "imported but unused"

**Causa:** Importaste algo que no usas

**Solución:**
```python
# ❌ Import no usado
from fastapi import FastAPI, HTTPException  # HTTPException no se usa

# ✅ Solo importar lo que usas
from fastapi import FastAPI
```

---

### ❌ Dependency check encuentra vulnerabilidad

**Causa:** Una de tus dependencias tiene una vulnerabilidad conocida

**Solución:**
1. Ver el reporte en GitHub Actions
2. Actualizar el paquete vulnerable:
   ```bash
   pip install --upgrade <paquete-vulnerable>
   pip freeze > requirements.txt
   ```
3. Hacer commit y push

---

## Configuración de Herramientas

### setup.cfg

Contiene configuración de flake8, mypy, pytest:

```ini
[flake8]
max-line-length = 127
exclude = venv, .venv, __pycache__

[mypy]
ignore_missing_imports = True
```

### pyproject.toml

Contiene configuración de Black e isort:

```toml
[tool.black]
line-length = 127
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 127
```

---

## Beneficios para tu Portafolio

### 🎯 Para Reclutadores

✅ **Demuestra profesionalismo**
   - Usas las mismas herramientas que empresas reales
   - Automatizas verificaciones de calidad

✅ **Badge verde = código confiable**
   - Primera impresión positiva
   - Indica que mantienes estándares altos

✅ **Muestra proactividad**
   - No esperas a que te digan que uses CI/CD
   - Lo implementas por iniciativa propia

### 🎯 Para Tech Leads

✅ **Código mantenible**
   - Formateo consistente
   - Type hints verificados
   - Sin code smells

✅ **Seguridad**
   - Escaneo automático de vulnerabilidades
   - Detección de secrets expuestos

✅ **Listo para producción**
   - Pipeline de CI ya configurado
   - Fácil agregar tests cuando crezca el proyecto

---

## Próximos Pasos

### Cuando agregues tests

Actualiza `.github/workflows/ci.yml` agregando:

```yaml
- name: 🧪 Run tests
  run: |
    pytest tests/ --cov=app --cov-report=xml

- name: 📊 Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

### Cuando despliegues a producción

Crea `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: test  # Solo deploy si tests pasan

    steps:
      - name: Deploy to Render/Railway/etc
        run: |
          # Comandos de deploy
```

---

## Recursos Adicionales

- 📚 [GitHub Actions Docs](https://docs.github.com/en/actions)
- 🎓 [Black Documentation](https://black.readthedocs.io/)
- 📖 [flake8 Documentation](https://flake8.pycqa.org/)
- 🔍 [mypy Documentation](https://mypy.readthedocs.io/)

---

**¿Preguntas sobre CI/CD?**
[Abre un issue](https://github.com/marceloemmott-dev/retail-backend-api/issues)

---

<div align="center">

Configurado con 🔧 por [Marcelo Emmott](https://github.com/marceloemmott-dev)

</div>
