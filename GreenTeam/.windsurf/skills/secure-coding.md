---
description: Skill para guiar desarrollo de código seguro y mejores prácticas
---

# 🛡️ Secure Coding Skill

## Descripción

Este skill proporciona guía para escribir código seguro, aplicando mejores prácticas de seguridad y patrones de diseño seguros.

## Principios de Código Seguro

### 1. Input Validation
```python
# ❌ Inseguro
def process(data):
    return eval(data)

# ✅ Seguro
def process(data):
    if not isinstance(data, str):
        raise ValueError("Invalid input type")
    if len(data) > MAX_LENGTH:
        raise ValueError("Input too long")
    # Procesar de forma segura
```

### 2. Output Encoding
```javascript
// ❌ Inseguro
element.innerHTML = userInput;

// ✅ Seguro
element.textContent = userInput;
// O usar librería de sanitización
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 3. Parameterized Queries
```python
# ❌ Inseguro
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ Seguro
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### 4. Secure Authentication
```python
# ❌ Inseguro
if password == stored_password:
    authenticate()

# ✅ Seguro
import bcrypt
if bcrypt.checkpw(password.encode(), stored_hash):
    authenticate()
```

### 5. Secure Session Management
```python
# ✅ Configuración segura de sesión
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)
)
```

### 6. Error Handling
```python
# ❌ Inseguro - expone información
except Exception as e:
    return str(e)

# ✅ Seguro - log interno, mensaje genérico
except Exception as e:
    logger.error(f"Error: {e}")
    return "An error occurred. Please try again."
```

### 7. Cryptography
```python
# ❌ Inseguro
import hashlib
hash = hashlib.md5(password).hexdigest()

# ✅ Seguro
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### 8. File Operations
```python
# ❌ Inseguro
with open(user_provided_path, 'r') as f:
    return f.read()

# ✅ Seguro
import os
safe_path = os.path.join(ALLOWED_DIR, os.path.basename(user_provided_path))
if not safe_path.startswith(ALLOWED_DIR):
    raise SecurityError("Path traversal attempt")
with open(safe_path, 'r') as f:
    return f.read()
```

## Checklists por Lenguaje

### Python
- [ ] Usar `secrets` en lugar de `random` para criptografía
- [ ] Usar `subprocess` con `shell=False`
- [ ] Validar tipos con `isinstance()`
- [ ] Usar `bcrypt` o `argon2` para passwords
- [ ] Configurar `pickle` de forma segura

### JavaScript
- [ ] Usar `textContent` en lugar de `innerHTML`
- [ ] Implementar CSP headers
- [ ] Validar JSON antes de parsear
- [ ] Usar `crypto.randomUUID()` para IDs
- [ ] Sanitizar con DOMPurify

### Java
- [ ] Usar PreparedStatement para SQL
- [ ] Validar XML con DTD deshabilitado
- [ ] Usar SecureRandom para criptografía
- [ ] Implementar equals/hashCode correctamente
- [ ] Evitar deserialización de datos no confiables

### Go
- [ ] Usar `html/template` para HTML
- [ ] Validar certificados TLS
- [ ] Usar `crypto/rand` para random
- [ ] Manejar errores explícitamente
- [ ] Evitar `unsafe` package

## Patrones de Diseño Seguros

### 1. Least Privilege
```python
# Ejecutar con permisos mínimos
os.setuid(unprivileged_user)
```

### 2. Defense in Depth
```python
# Múltiples capas de validación
def process_request(request):
    validate_authentication(request)
    validate_authorization(request)
    validate_input(request.data)
    sanitize_input(request.data)
    # Procesar
```

### 3. Fail Secure
```python
def check_access(user, resource):
    try:
        return authorization_service.check(user, resource)
    except Exception:
        return False  # Denegar por defecto
```

### 4. Secure Defaults
```python
class SecureConfig:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = True
```

## Uso

Al escribir código nuevo o revisar código existente:
1. Aplicar principios de código seguro
2. Seguir checklist del lenguaje
3. Implementar patrones de diseño seguros
4. Validar contra OWASP Top 10
