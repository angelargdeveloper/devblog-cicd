import pytest
import json
from app.models import blog_storage

class TestAPIEndpoints:
    """Clase que agrupa todas las pruebas de la API REST (endpoints JSON)"""

    def test_get_all_posts_success(self, client):
        """Test: GET /api/posts devuelve todos los posts en formato JSON"""
        response = client.get('/api/posts')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert 'success' in data
        assert 'data' in data
        assert 'count' in data
        assert data['success'] is True
        assert data['count'] == 2
        for post in data['data']:
            assert 'id' in post
            assert 'title' in post
            assert 'content' in post
            assert 'author' in post
            assert 'created_at' in post
            assert 'summary' in post

    def test_get_single_post_success(self, client):
        """Test: GET /api/posts/<id> devuelve un post específico"""
        response = client.get('/api/posts/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == 1
        assert 'Bienvenido a DevBlog' in data['data']['title']

    def test_get_single_post_not_found(self, client):
        """Test: GET /api/posts/<id> con ID inexistente devuelve 404"""
        response = client.get('/api/posts/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data

    def test_create_post_success(self, client):
        """Test: POST /api/posts crea un nuevo post correctamente"""
        new_post = {
            'title': 'Post creado via API',
            'content': 'Este post fue creado usando la API REST.\n\nEs muy útil para integraciones.',
            'author': 'API Tester'
        }
        response = client.post('/api/posts',
                             data=json.dumps(new_post),
                             content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == new_post['title']
        assert len(blog_storage.get_all_posts()) == 3

    def test_create_post_missing_data(self, client):
        """Test: POST /api/posts sin datos requeridos devuelve error"""
        incomplete_post = {
            'title': 'Solo título',
            # Falta 'content'
        }
        response = client.post('/api/posts',
                             data=json.dumps(incomplete_post),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'requeridos' in data['error'].lower()

    def test_create_post_no_json(self, client):
        """Test: POST /api/posts sin JSON devuelve error"""
        response = client.post('/api/posts')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'json' in data['error'].lower()

    def test_create_post_invalid_json(self, client):
        """Test: POST /api/posts con JSON malformado devuelve error"""
        response = client.post('/api/posts',
                             data='{"title": "incomplete json"',
                             content_type='application/json')
        assert response.status_code == 400

    def test_update_post_success(self, client):
        """Test: PUT /api/posts/<id> actualiza un post correctamente"""
        update_data = {
            'title': 'Título actualizado',
            'content': 'Contenido actualizado via API'
        }
        response = client.put('/api/posts/1',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == update_data['title']
        updated_post = blog_storage.get_post_by_id(1)
        assert updated_post.title == update_data['title']

    def test_update_post_not_found(self, client):
        """Test: PUT /api/posts/<id> con ID inexistente devuelve 404"""
        update_data = {'title': 'No importa'}
        response = client.put('/api/posts/999',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False

    def test_delete_post_success(self, client):
        """Test: DELETE /api/posts/<id> elimina un post correctamente"""
        assert blog_storage.get_post_by_id(1) is not None
        response = client.delete('/api/posts/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert blog_storage.get_post_by_id(1) is None
        assert len(blog_storage.get_all_posts()) == 1

    def test_delete_post_not_found(self, client):
        """Test: DELETE /api/posts/<id> con ID inexistente devuelve 404"""
        response = client.delete('/api/posts/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False

    def test_search_api_success(self, client):
        """Test: GET /api/search?q=término busca posts correctamente"""
        response = client.get('/api/search?q=Docker')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['query'] == 'Docker'
        assert data['count'] >= 1
        for post in data['data']:
            assert ('docker' in post['title'].lower() or
                   'docker' in post['content'].lower())

    def test_search_api_no_query(self, client):
        """Test: GET /api/search sin parámetro q devuelve error"""
        response = client.get('/api/search')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'requerido' in data['error'].lower()

    def test_search_api_empty_query(self, client):
        """Test: GET /api/search?q= (vacío) devuelve error"""
        response = client.get('/api/search?q=')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_search_api_no_results(self, client):
        """Test: GET /api/search con término que no existe"""
        response = client.get('/api/search?q=TerminoQueNoExiste')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 0