# 🪝 Pre-commit Hooks - Guía Completa

> Automatización de calidad de código ANTES de cada commit

---

## 📋 Tabla de Contenidos

- [¿Qué son Pre-commit Hooks?](#qué-son-pre-commit-hooks)
- [¿Por qué usar Pre-commit?](#por-qué-usar-pre-commit)
- [Instalación](#instalación)
- [Hooks Configurados](#hooks-configurados)
- [Uso Diario](#uso-diario)
- [Solución de Problemas](#solución-de-problemas)
- [Mejores Prácticas](#mejores-prácticas)

---

## ¿Qué son Pre-commit Hooks?

### Definición Simple

**Pre-commit hooks** son scripts que se ejecutan **automáticamente antes de cada commit**.

```
Tú escribes código
       ↓
git add .
       ↓
git commit -m "mensaje"
       ↓
🪝 PRE-COMMIT HOOKS SE EJECUTAN AQUÍ
       ├─ Black formatea código
       ├─ isort ordena imports
       ├─ flake8 verifica calidad
       ├─ mypy chequea tipos
       └─ Validaciones de seguridad
       ↓
¿Todo OK?
├─ ✅ SÍ → Commit se completa
└─ ❌ NO → Commit se bloquea (debes arreglar)
```

---

## ¿Por qué usar Pre-commit?

### 🎯 **Beneficios Principales**

#### 1. **Detecta problemas ANTES de subir código**

❌ **Sin pre-commit:**
```
git commit → git push → CI falla → "Oh no, error!" → Arreglar → Push again
```

✅ **Con pre-commit:**
```
git commit → Pre-commit detecta error → Arreglas → Commit exitoso → git push → CI pasa ✅
```

#### 2. **Ahorra tiempo**

- **Sin pre-commit:** Esperas 3-5 min a que CI falle
- **Con pre-commit:** Detectas error en 5 segundos

#### 3. **Mantiene código limpio automáticamente**

No tienes que acordarte de correr Black, isort, etc. Se ejecutan **solos**.

#### 4. **Estándar en empresas**

Todas las empresas modernas usan pre-commit hooks. Muestra profesionalismo.

---

## Instalación

### Paso 1: Instalar pre-commit

```bash
# Instalar globalmente
pip install pre-commit

# Verificar instalación
pre-commit --version
```

### Paso 2: Instalar hooks en el repo

```bash
# Dentro del proyecto
cd retail-backend-api

# Instalar hooks
pre-commit install
```

**Salida esperada:**
```
pre-commit installed at .git/hooks/pre-commit
```

### Paso 3: (Opcional) Correr en todos los archivos

```bash
# Primera vez solamente
pre-commit run --all-files
```

---

## Hooks Configurados

Tu proyecto tiene **15 hooks** organizados en 5 categorías:

### 1️⃣ **Formateo de Código**

| Hook | Qué hace | Ejemplo |
|------|----------|---------|
| **Black** | Formatea código Python a estándar | `if x==1:` → `if x == 1:` |
| **isort** | Ordena imports alfabéticamente | Reorganiza `from/import` |

---

### 2️⃣ **Calidad de Código**

| Hook | Qué hace | Cuándo falla |
|------|----------|--------------|
| **flake8** | Detecta errores de estilo | Variables sin usar, líneas largas |
| **mypy** | Chequea tipos | `def suma(a, b) → int:` sin implementar |

---

### 3️⃣ **Validaciones de Archivo**

| Hook | Qué hace |
|------|----------|
| **trailing-whitespace** | Quita espacios al final de líneas |
| **end-of-file-fixer** | Asegura archivos terminen con newline |
| **check-yaml** | Valida sintaxis YAML |
| **check-json** | Valida sintaxis JSON |
| **check-toml** | Valida sintaxis TOML |
| **check-added-large-files** | Previene archivos >1MB |

---

### 4️⃣ **Validaciones Python**

| Hook | Qué hace |
|------|----------|
| **check-ast** | Verifica sintaxis Python válida |
| **check-docstring-first** | Docstring debe ser primer statement |
| **debug-statements** | Detecta `import pdb`, `breakpoint()` |
| **name-tests-test** | Tests deben empezar con `test_` |

---

### 5️⃣ **Seguridad**

| Hook | Qué hace |
|------|----------|
| **detect-private-key** | Detecta claves SSH/GPG |
| **python-safety-dependencies-check** | Detecta dependencias vulnerables |

---

## Uso Diario

### Flujo Normal (Automático)

```bash
# 1. Modificas código
vim app/main.py

# 2. Agregas cambios
git add app/main.py

# 3. Intentas commit
git commit -m "Add new feature"

# 🪝 Pre-commit se ejecuta automáticamente
# Output:
# 🎨 Format code with Black...................................Passed
# 📋 Sort imports with isort.................................Passed
# 🔍 Lint with flake8........................................Passed
# 🔎 Type check with mypy....................................Passed
# ✂️ Trim trailing whitespace................................Passed
# ... (todos los hooks)

# ✅ Todo OK → Commit se completa
```

---

### Si un hook falla

```bash
git commit -m "Add feature"

# Output:
# 🎨 Format code with Black...................................Failed
# - hook id: black
# - files were modified by this hook
# 
# reformatted app/main.py
# 
# All done! ✨ 🍰 ✨
# 1 file reformatted.

# ❌ Commit bloqueado
```

**¿Qué hacer?**

1. **Los archivos ya fueron arreglados automáticamente**
2. Revisa los cambios: `git diff`
3. Agrega los cambios: `git add .`
4. Intenta commit de nuevo: `git commit -m "Add feature"`
5. Ahora debería pasar ✅

---

### Comandos Útiles

#### Ejecutar hooks manualmente (sin commit)

```bash
# Correr en archivos staged
pre-commit run

# Correr en TODOS los archivos
pre-commit run --all-files

# Correr hook específico
pre-commit run black
pre-commit run flake8
```

#### Actualizar hooks a versiones más recientes

```bash
pre-commit autoupdate
```

#### Temporalmente skip hooks

```bash
# Skip todos los hooks (NO RECOMENDADO)
git commit -m "mensaje" --no-verify

# Skip hook específico
SKIP=flake8 git commit -m "mensaje"
```

---

## Solución de Problemas

### ❌ **Problema: "command not found: pre-commit"**

**Causa:** pre-commit no está instalado

**Solución:**
```bash
pip install pre-commit
pre-commit install
```

---

### ❌ **Problema: Hook falla con "file not found"**

**Causa:** Los linters no están instalados localmente

**Solución:**
```bash
pip install black isort flake8 mypy
```

---

### ❌ **Problema: mypy falla con "cannot find module"**

**Causa:** Imports de terceros sin types

**Solución:** Ya está configurado con `--ignore-missing-imports`

Si persiste:
```bash
pip install types-all
```

---

### ❌ **Problema: safety check muy lento**

**Causa:** Safety consulta base de datos online

**Solución:** 
```yaml
# Deshabilitar temporalmente en .pre-commit-config.yaml
# Comentar el hook de safety
```

---

### ❌ **Problema: Hooks corren en archivos que no quiero**

**Causa:** Configuración de exclude

**Solución:** Editar `.pre-commit-config.yaml`:

```yaml
exclude: |
  (?x)^(
      venv/|
      migrations/|  # ← Agregar aquí
      \.git/
  )
```

---

## Mejores Prácticas

### ✅ **DO's (Hazlo)**

1. **Corre pre-commit antes de PR importantes**
   ```bash
   pre-commit run --all-files
   ```

2. **Actualiza versiones periódicamente**
   ```bash
   pre-commit autoupdate
   ```

3. **Commitea archivos de configuración**
   ```bash
   git add .pre-commit-config.yaml
   ```

4. **Documenta hooks custom en README**

5. **Usa `--all-files` después de actualizar configs**

---

### ❌ **DON'Ts (No hagas)**

1. **NO uses `--no-verify` habitualmente**
   - Solo en emergencias

2. **NO agregues hooks que tarden mucho**
   - Pre-commit debe ser rápido (<30 seg)

3. **NO ignores failures sin entender**
   - Si falla, hay una razón

4. **NO configures hooks que modifiquen tu código sin avisar**
   - Siempre revisa cambios automáticos

---

## Integración con CI/CD

Los mismos checks que corren en pre-commit **también corren en CI**.

### Ventaja del enfoque "Defense in Depth"

```
Línea de defensa #1: Pre-commit (local)
        ↓ (si pasa)
Línea de defensa #2: CI en GitHub (remoto)
        ↓ (si pasa)
Línea de defensa #3: Code Review
        ↓ (si aprueba)
Merge a main
```

**Si un hook pasa en pre-commit, pasará en CI** (mismo código).

---

## Configuración Avanzada

### Crear hook custom

Ejemplo: Verificar que no hay `print()` statements:

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: no-print-statements
      name: Check for print statements
      entry: '.*print\(.*'
      language: pygrep
      types: [python]
```

### Hook que corre script custom

```yaml
- repo: local
  hooks:
    - id: run-tests
      name: Run unit tests
      entry: pytest tests/
      language: system
      pass_filenames: false
      always_run: true
```

---

## Comparación: Con vs Sin Pre-commit

| Situación | Sin Pre-commit | Con Pre-commit |
|-----------|----------------|----------------|
| **Tiempo hasta detectar error** | 3-5 min (CI) | 5 segundos |
| **Costo de arreglar** | Alto (ya pusheaste) | Bajo (local) |
| **Commits sucios** | Frecuentes | Raros |
| **Confianza en código** | Baja | Alta |
| **Profesionalismo** | Junior/Mid | Senior |

---

## Estadísticas

### Antes de pre-commit:
- ❌ 30% de commits fallan en CI
- ⏰ 5 min promedio para detectar error
- 😓 Frustración al esperar CI

### Después de pre-commit:
- ✅ 95% de commits pasan CI a la primera
- ⚡ 5 seg promedio para detectar error
- 😊 Confianza en cada commit

---

## Recursos Adicionales

- 📚 [Documentación oficial](https://pre-commit.com/)
- 🎓 [Hooks disponibles](https://pre-commit.com/hooks.html)
- 🔧 [Configuración avanzada](https://pre-commit.com/#advanced)
- 💬 [pre-commit en Reddit](https://www.reddit.com/r/Python/search/?q=pre-commit)

---

## Preguntas Frecuentes

### **¿Pre-commit es obligatorio?**

No, pero **altamente recomendado**. Tu equipo te lo agradecerá.

### **¿Pre-commit reemplaza CI?**

No, **complementa** CI. Pre-commit es la primera línea de defensa.

### **¿Qué pasa si alguien no lo instala?**

No correrá en su máquina, pero **CI lo detectará**.

### **¿Puede pre-commit romper mi código?**

Los hooks solo **formatean/validan**. Siempre revisa cambios antes de commit.

### **¿Cuánto tiempo agrega al commit?**

Generalmente **5-15 segundos**. Mucho menos que esperar CI (3-5 min).

---

## Próximos Pasos

✅ Ya instalaste pre-commit  
✅ Ya entiendes cómo funciona  
➡️ Ahora: Commitea con confianza  
➡️ Luego: Personaliza hooks según necesites  

---

<div align="center">

**¿Dudas sobre pre-commit?**  
[Abre un issue](https://github.com/marceloemmott-dev/retail-backend-api/issues)

---

Configurado con 🪝 por [Marcelo Emmott](https://github.com/marceloemmott-dev)

</div>
