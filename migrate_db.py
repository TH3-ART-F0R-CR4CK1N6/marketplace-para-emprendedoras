"""
Script de migración para agregar nuevos campos a la tabla User
Ejecutar este script en Render para actualizar la base de datos sin perder datos
"""
from app import app, db
from sqlalchemy import text

def migrate_database():
    with app.app_context():
        try:
            # Verificar si las columnas ya existen
            with db.engine.connect() as conn:
                # Agregar columnas nuevas si no existen
                columns_to_add = [
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS phone VARCHAR(20);",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS address VARCHAR(200);",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS facebook VARCHAR(200);",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS instagram VARCHAR(200);",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS twitter VARCHAR(200);",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS whatsapp VARCHAR(20);",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS bio TEXT;",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS profile_image VARCHAR(300);"
                ]
                
                for sql in columns_to_add:
                    try:
                        conn.execute(text(sql))
                        conn.commit()
                        print(f"✓ Ejecutado: {sql}")
                    except Exception as e:
                        print(f"⚠ Ya existe o error: {sql} - {str(e)}")
                
            print("\n✅ Migración completada exitosamente!")
            
        except Exception as e:
            print(f"❌ Error en la migración: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_database()
