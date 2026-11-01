# 🚀 DESPLIEGUE EN RENDER - GUÍA RÁPIDA

## 📋 PASOS RÁPIDOS

**Tiempo total:** 15-20 minutos

### PASO 1: Crear Cuenta en Render
1. Ve a: **https://render.com**
2. Click **"Get Started"** → **"Sign Up with GitHub"**
3. Autoriza Render

### PASO 2: Crear Base de Datos PostgreSQL
1. En Render Dashboard → **"New +"** → **"PostgreSQL"**
2. Configuración:
   - Name: `marketplace-db`
   - Database: `marketplace_emprendedoras`
   - Region: Oregon (US West)
   - Plan: **Free** ⭐
3. Click **"Create Database"**
4. **COPIA la "External Database URL"** (la necesitarás después)

### PASO 3: Crear Web Service
1. Dashboard → **"New +"** → **"Web Service"**
2. Conecta tu repo: **marketplace-para-emprendedoras**
3. Configuración:
   - Name: `marketplace-emprendedoras`
   - Region: Oregon (US West) - MISMO que la BD
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Plan: **Free** ⭐

4. **Variables de Entorno** (antes de crear):
   
   Click en "Add Environment Variable":
   
   **Variable 1:**
   ```
   Key: DATABASE_URL
   Value: [PEGA LA URL DE POSTGRESQL]
   ```
   
   **Variable 2:**
   ```
   Key: SECRET_KEY
   Value: [GENERA UNA CLAVE - ver abajo]
   ```

**Para generar SECRET_KEY**, ejecuta en tu terminal:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

5. Click **"Create Web Service"**
6. Espera 3-5 minutos hasta ver **"Live"** ✅

### PASO 4: Inicializar Base de Datos
1. En tu Web Service → Click **"Shell"** (menú lateral)
2. Ejecuta en la terminal:
```bash
python init_db.py
```
3. Deberías ver:
```
✓ Base de datos creada
✓ Usuario admin creado (user: admin, pass: admin123)
```

### PASO 5: ¡Listo!
Tu marketplace estará en:
```
https://marketplace-emprendedoras.onrender.com
```

**Prueba iniciando sesión:**
- Admin: `admin` / `admin123`
- Emprendedora: `maria_emprendedora` / `123456`

⚠️ **IMPORTANTE:** Cambia las contraseñas después del primer login.

---

## 🔧 SOLUCIÓN DE PROBLEMAS

**App no inicia:**
- Verifica DATABASE_URL en Environment Variables
- Revisa los Logs

**Se queda cargando:**
- Plan Free se "duerme" - espera 30-50 segundos

**Error de base de datos:**
- Verifica que PostgreSQL esté "Available"
- Ejecuta `python init_db.py` de nuevo

---

## 📊 LIMITACIONES PLAN FREE

✅ 750 horas/mes (24/7)
⚠️ Se duerme tras 15 min de inactividad
⚠️ Almacenamiento de imágenes efímero
✅ SSL/HTTPS incluido

---

## ✅ CHECKLIST

- [ ] Cuenta Render creada
- [ ] PostgreSQL creado y URL copiada
- [ ] Web Service creado
- [ ] Variables de entorno configuradas
- [ ] Despliegue "Live"
- [ ] `python init_db.py` ejecutado
- [ ] App probada y funciona

**¡Tu marketplace estará en línea en 15-20 minutos! 💜**
