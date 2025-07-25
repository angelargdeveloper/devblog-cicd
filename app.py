import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("="*50)
    print("Iniciando DevBlog...")
    print(f"Entorno: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Puerto: {port}")
    print(f"Debug: {debug}")
    print("="*50)
    
    # Mostrar rutas disponibles
    print("\nRutas registradas:")
    for rule in app.url_map.iter_rules():
        print(f"- {rule}")
    print("\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )