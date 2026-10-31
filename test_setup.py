"""
Script de prueba para verificar la configuración del marketplace
"""
from app import app, db, User, Product

def test_app():
    with app.app_context():
        print("🧪 Verificando configuración del marketplace...\n")
        
        # Verificar base de datos
        try:
            users = User.query.all()
            products = Product.query.all()
            print(f"✅ Base de datos: OK")
            print(f"   - Usuarios: {len(users)}")
            print(f"   - Productos: {len(products)}")
        except Exception as e:
            print(f"❌ Error en base de datos: {e}")
            return False
        
        # Verificar roles
        admin = User.query.filter_by(role='admin').first()
        emprendedora = User.query.filter_by(role='emprendedora').first()
        
        if admin:
            print(f"✅ Usuario admin encontrado: {admin.username}")
        else:
            print("⚠️  No hay usuario administrador")
        
        if emprendedora:
            print(f"✅ Usuario emprendedora encontrado: {emprendedora.username}")
        else:
            print("⚠️  No hay usuario emprendedora")
        
        # Verificar productos
        print(f"\n📦 Productos en el sistema:")
        for product in products:
            tipo = "Servicio" if product.is_service else "Producto"
            estado = "Activo" if product.active else "Inactivo"
            print(f"   - {product.name} ({tipo}) - ${product.price} - {estado}")
        
        # Verificar carpetas
        import os
        upload_folder = app.config['UPLOAD_FOLDER']
        if os.path.exists(upload_folder):
            print(f"\n✅ Carpeta de uploads: {upload_folder}")
        else:
            print(f"\n⚠️  Carpeta de uploads no existe: {upload_folder}")
        
        print("\n✅ ¡Todas las verificaciones completadas!")
        print("\n🚀 La aplicación está lista para usarse")
        print("\n📝 Para iniciar el servidor:")
        print("   python app.py")
        print("\n🌐 Luego abre tu navegador en:")
        print("   http://localhost:5000")
        
        return True

if __name__ == '__main__':
    test_app()
