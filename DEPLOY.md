# Guía de Despliegue en Render

## 📋 Pasos para Desplegar

### 1. Preparar el Repositorio en GitHub

1. Crea un nuevo repositorio en GitHub
2. Inicializa git en tu proyecto local:
```bash
git init
git add .
git commit -m "Initial commit: Marketplace de Emprendedoras"
git branch -M main
git remote add origin https://github.com/tu-usuario/tu-repositorio.git
git push -u origin main
```

### 2. Crear PostgreSQL Database en Render

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click en **"New +"** → **"PostgreSQL"**
3. Configura:
   - **Name**: `marketplace-db`
   - **Database**: `marketplace`
   - **Region**: Elige el más cercano
   - **Plan**: Free
4. Click en **"Create Database"**
5. **IMPORTANTE**: Copia la **"External Database URL"**

### 3. Crear Web Service en Render

1. En Render Dashboard, click en **"New +"** → **"Web Service"**
2. Conecta tu cuenta de GitHub
3. Selecciona tu repositorio
4. Configura:
   - **Name**: `marketplace-emprendedoras`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

### 4. Configurar Variables de Entorno

En **"Environment"** agrega:

```
DATABASE_URL=<pega-la-url-de-postgresql>
SECRET_KEY=<genera-una-clave-segura>
```

Para generar SECRET_KEY:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Desplegar

Click en **"Create Web Service"**. El proceso toma 2-5 minutos.

### 6. Inicializar la Base de Datos

En tu Web Service → **"Shell"**:
```bash
python init_db.py
```

Credenciales creadas:
- Admin: `admin` / `admin123`
- Emprendedora: `maria_emprendedora` / `123456`

### 7. Verificar

Abre tu URL: `https://tu-app.onrender.com`

## 🔄 Actualizaciones

```bash
git add .
git commit -m "Tus cambios"
git push origin main
```

Render re-desplegará automáticamente.

## 🔒 Seguridad

**Cambia las contraseñas predeterminadas** después del primer despliegue.

## 📊 Límites Plan Free

- Se duerme después de 15 min de inactividad
- 750 horas/mes
- PostgreSQL: 1 GB

## ✅ Checklist

- [ ] Repo en GitHub
- [ ] Base de datos PostgreSQL creada
- [ ] Web Service creado
- [ ] Variables de entorno configuradas
- [ ] init_db.py ejecutado
- [ ] Contraseñas cambiadas

Ver README.md para más detalles.
