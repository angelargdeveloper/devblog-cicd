import pytest
from app import create_app
from app.models import blog_storage

@pytest.fixture
def app():
    """
    Fixture que crea una instancia de la aplicación para testing
    
    ¿Qué es un fixture?
    - Función que prepara datos/objetos para las pruebas
    - Se ejecuta antes de cada test que lo necesite
    - Garantiza un estado limpio para cada prueba
    """
    
    # Crear aplicación en modo testing
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Desactivar CSRF para testing
    
    return app

@pytest.fixture
def client(app):
    """
    Fixture que crea un cliente de testing para hacer peticiones HTTP
    
    ¿Para qué sirve?
    - Simula un navegador web
    - Permite hacer GET, POST, PUT, DELETE
    - No necesita servidor real corriendo
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    Fixture para testing de comandos CLI (si los tuviéramos)
    """
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def reset_storage():
    """
    Fixture que resetea el almacenamiento antes de cada test
    
    ¿Por qué autouse=True?
    - Se ejecuta automáticamente antes de cada test
    - Garantiza que cada test empiece con datos limpios
    - Evita que los tests se afecten entre sí
    """
    # Limpiar todos los posts
    blog_storage._posts.clear()
    blog_storage._next_id = 1
    
    # Recrear posts de ejemplo para tests consistentes
    blog_storage._create_sample_posts()
    
    yield  # Aquí se ejecuta el test
    
    # Cleanup después del test (si fuera necesario)
    pass



# ================================
# SELENIUM E2E FIXTURES
# ================================
import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def flask_test_app():
    """Fixture que inicia la aplicación Flask para testing E2E"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    def run_app():
        app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_app, daemon=True)
    server_thread.start()
    time.sleep(3)
    
    yield app

@pytest.fixture
def selenium_driver():
    """Fixture que crea un driver de Chrome para testing"""
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    try:
        # Intentar con webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error con webdriver-manager: {e}")
        try:
            # Fallback: usar Chrome del sistema
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e2:
            print(f"Error con Chrome del sistema: {e2}")
            # Último recurso: usar Edge (disponible en Windows 10/11)
            from selenium.webdriver.edge.options import Options as EdgeOptions
            from selenium.webdriver.edge.service import Service as EdgeService
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            
            edge_options = EdgeOptions()
            #edge_options.add_argument('--headless')
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('--disable-dev-shm-usage')
            
            edge_service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=edge_service, options=edge_options)
    
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def e2e_base_url():
    """URL base para los tests E2E"""
    return "http://127.0.0.1:5001"