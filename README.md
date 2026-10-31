# Marketplace de Emprendedoras 💜

Una plataforma marketplace moderna diseñada para mujeres emprendedoras, con un diseño en colores morados y lilas. Permite a las emprendedoras publicar sus productos y servicios, y a los clientes explorar y descubrir ofertas únicas.

## 🌟 Características

- **Sistema de usuarios con roles**:
  - **Administrador**: Gestión completa de usuarios y productos
  - **Emprendedora**: Puede crear, editar y gestionar sus productos
  - **Cliente**: Puede explorar y buscar productos

- **Gestión de productos**:
  - Crear y editar productos/servicios
  - Subir imágenes
  - Categorización
  - Activar/desactivar productos

- **Búsqueda y filtrado**:
  - Búsqueda por palabra clave
  - Filtrar por categoría
  - Filtrar por tipo (producto/servicio)

- **Diseño responsive**: Adaptado para móviles y tablets

## 🚀 Despliegue en Render

### Paso 1: Preparar el repositorio

1. Crea un repositorio en GitHub
2. Sube todos los archivos del proyecto

### Paso 2: Crear Web Service en Render

1. Ve a [Render](https://render.com) y crea una cuenta
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Name**: marketplace-emprendedoras (o el nombre que prefieras)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Paso 3: Configurar Base de Datos PostgreSQL

1. En Render, ve a "New +" → "PostgreSQL"
2. Crea la base de datos
3. Copia la "External Database URL"

### Paso 4: Variables de Entorno

En tu Web Service de Render, ve a "Environment" y agrega:

```
DATABASE_URL=<tu-postgres-url-aquí>
SECRET_KEY=<genera-una-clave-secreta-aleatoria>
```

### Paso 5: Crear usuario administrador

Una vez desplegado, abre la Shell en Render y ejecuta:

```bash
python
>>> from app import app, db, User
>>> with app.app_context():
...     admin = User(username='admin', email='admin@marketplace.com', role='admin')
...     admin.set_password('tu_contraseña_segura')
...     db.session.add(admin)
...     db.session.commit()
...     print('Admin creado')
```

## 💻 Desarrollo Local

### Requisitos

- Python 3.11+
- pip

### Instalación

1. Clona el repositorio:
```bash
git clone <tu-repositorio>
cd marketplace-emprendedoras
```

2. Crea un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
```

3. Instala dependencias:
```bash
pip install -r requirements.txt
```

4. Configura variables de entorno (opcional, usa `.env`):
```
SECRET_KEY=tu-clave-secreta
DATABASE_URL=sqlite:///marketplace.db
```

5. Ejecuta la aplicación:
```bash
python app.py
```

6. Abre tu navegador en `http://localhost:5000`

### Crear usuario administrador local

```bash
python
>>> from app import app, db, User
>>> with app.app_context():
...     db.create_all()
...     admin = User(username='admin', email='admin@marketplace.com', role='admin')
...     admin.set_password('admin123')
...     db.session.add(admin)
...     db.session.commit()
```

## 📁 Estructura del Proyecto

```
marketplace-emprendedoras/
├── app.py                  # Aplicación principal Flask
├── requirements.txt        # Dependencias Python
├── Procfile               # Configuración para Render
├── runtime.txt            # Versión de Python
├── templates/             # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── emprendedora_dashboard.html
│   ├── product_form.html
│   ├── product_detail.html
│   └── search.html
└── static/                # Archivos estáticos
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── uploads/           # Imágenes subidas
```

## 🎨 Paleta de Colores

- **Púrpura Principal**: #8B5CF6
- **Púrpura Claro**: #C4B5FD
- **Púrpura Oscuro**: #6D28D9
- **Lavanda**: #E9D5FF
- **Blanco**: #FFFFFF

## 🔐 Roles de Usuario

### Administrador
- Ver estadísticas de la plataforma
- Gestionar usuarios
- Ver todos los productos
- Eliminar usuarios

### Emprendedora
- Crear productos/servicios
- Editar sus productos
- Activar/desactivar productos
- Subir imágenes

### Cliente
- Explorar productos
- Buscar y filtrar
- Ver detalles de productos

## 📝 Categorías Disponibles

- Moda y Accesorios
- Belleza y Cuidado
- Hogar y Decoración
- Alimentos y Bebidas
- Arte y Manualidades
- Servicios Profesionales
- Otros

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **ORM**: SQLAlchemy
- **Autenticación**: Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **Despliegue**: Render

## 📱 Responsive Design

La aplicación está completamente optimizada para:
- 📱 Móviles
- 💻 Tablets
- 🖥️ Desktop

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👩💼 Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio.

---

**Hecho con 💜 para apoyar a mujeres emprendedoras**
