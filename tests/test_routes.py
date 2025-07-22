import pytest
from flask import url_for

class TestWebRoutes:
    """Clase que agrupa todas las pruebas de rutas web (páginas HTML)"""

    def test_index_page_loads(self, client):
        """Test: La página principal carga correctamente"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'DevBlog' in response.data
        assert b'Posts Recientes' in response.data
        assert b'Bienvenido a DevBlog' in response.data

    def test_index_shows_posts(self, client):
        """Test: La página principal muestra los posts correctamente"""
        response = client.get('/')
        assert b'Bienvenido a DevBlog' in response.data
        assert b'Mi experiencia con Docker' in response.data
        assert b'Leer m\xc3\xa1s' in response.data

    def test_view_post_exists(self, client):
        """Test: Ver un post individual que existe"""
        response = client.get('/post/1')
        assert response.status_code == 200
        assert b'Bienvenido a DevBlog' in response.data
        assert b'DevOps Student' in response.data

    def test_view_post_not_found(self, client):
        """Test: Ver un post que no existe devuelve 404"""
        response = client.get('/post/999')
        assert response.status_code == 404

    def test_create_post_get(self, client):
        """Test: La página de crear post carga correctamente (GET)"""
        response = client.get('/create')
        assert response.status_code == 200
        assert b'Crear Nuevo Post' in response.data
        assert b'<form' in response.data
        assert b'name="title"' in response.data
        assert b'name="content"' in response.data

    def test_create_post_success(self, client):
        """Test: Crear un post exitosamente (POST)"""
        post_data = {
            'title': 'Test Post',
            'content': 'Este es un post de prueba.\n\nCon múltiples párrafos.',
            'author': 'Test Author'
        }
        response = client.post('/create', data=post_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Test Post' in response.data
        assert b'Test Author' in response.data
        assert b'Este es un post de prueba' in response.data

    def test_create_post_validation_errors(self, client):
        """Test: Validación de formulario funciona correctamente"""
        post_data = {
            'title': '',  # Título vacío (inválido)
            'content': 'Contenido válido',
            'author': 'Test Author'
        }
        response = client.post('/create', data=post_data)
        assert response.status_code == 200
        assert b'El t\xc3\xadtulo es requerido' in response.data

    def test_search_page_loads(self, client):
        """Test: La página de búsqueda carga correctamente"""
        response = client.get('/search')
        assert response.status_code == 200
        assert b'B\xc3\xbasqueda de Posts' in response.data
        assert b'<form' in response.data

    def test_search_with_query(self, client):
        """Test: Búsqueda con término devuelve resultados"""
        response = client.get('/search?q=Docker')
        assert response.status_code == 200
        assert b'Docker' in response.data
        assert b'Mi experiencia con Docker' in response.data

    def test_search_no_results(self, client):
        """Test: Búsqueda sin resultados maneja correctamente"""
        response = client.get('/search?q=TerminoQueNoExiste')
        assert response.status_code == 200
        assert b'No se encontraron resultados' in response.data

    def test_navigation_links(self, client):
        """Test: Los enlaces de navegación funcionan correctamente"""
        response = client.get('/')
        assert b'href="/create"' in response.data
        response = client.get('/create')
        assert response.status_code == 200