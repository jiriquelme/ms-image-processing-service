import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch, Mock
import django
from django.conf import settings

if not settings.configured:
    django.setup()


@pytest.mark.django_db
@patch('processor.views.vision.ImageAnnotatorClient')
def test_process_image(mock_vision_client):
    # Configura el mock para Google Vision API
    mock_client_instance = mock_vision_client.return_value
    mock_response = Mock()
    mock_response.text_annotations = [Mock(description="DEPTO.\n64H")]
    mock_client_instance.text_detection.return_value = mock_response

    # Configura el cliente de prueba de DRF
    client = APIClient()

    # Cargar una imagen real desde el sistema de archivos
    with open('tests/images/64H.jpeg', 'rb') as image_file:
        url = reverse('process_image')  # Ajusta el nombre si es diferente
        response = client.post(url, {'image': image_file}, format='multipart')

    print(response)

    # Verifica la respuesta
    assert response.status_code == 200
    assert response.json()['text'] == "DEPTO.\n64H"
