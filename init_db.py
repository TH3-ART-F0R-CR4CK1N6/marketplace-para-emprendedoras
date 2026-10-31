from app import app, db, User, Product

with app.app_context():
    # Crear tablas
    db.create_all()
    print('✓ Base de datos creada')
    
    # Crear admin si no existe
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@marketplace.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print('✓ Usuario admin creado (user: admin, pass: admin123)')
    
    # Crear emprendedora de ejemplo
    emp = User.query.filter_by(username='maria_emprendedora').first()
    if not emp:
        emp = User(username='maria_emprendedora', email='maria@example.com', role='emprendedora')
        emp.set_password('123456')
        db.session.add(emp)
        db.session.flush()
        print('✓ Usuario emprendedora creado (user: maria_emprendedora, pass: 123456)')
        
        # Crear productos de ejemplo
        p1 = Product(
            name='Aretes Artesanales',
            description='Hermosos aretes hechos a mano con materiales de alta calidad. Perfectos para cualquier ocasión.',
            price=15.99,
            category='moda',
            is_service=False,
            user_id=emp.id
        )
        
        p2 = Product(
            name='Asesoría de Imagen',
            description='Sesión personalizada de asesoría de imagen y estilo. Te ayudo a encontrar tu mejor versión.',
            price=50.00,
            category='servicios',
            is_service=True,
            user_id=emp.id
        )
        
        p3 = Product(
            name='Velas Aromáticas',
            description='Velas aromáticas hechas con cera de soja natural. Varios aromas disponibles.',
            price=12.50,
            category='hogar',
            is_service=False,
            user_id=emp.id
        )
        
        db.session.add_all([p1, p2, p3])
        print('✓ Productos de ejemplo creados')
    
    db.session.commit()
    print('\n✓ ¡Todo listo! La base de datos está configurada.')
    print('\nPuedes iniciar sesión con:')
    print('  - Admin: admin / admin123')
    print('  - Emprendedora: maria_emprendedora / 123456')
