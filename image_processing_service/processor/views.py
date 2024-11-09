from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from google.cloud import vision
import io

@csrf_exempt
def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Usar Google Vision API para procesar la imagen
        client = vision.ImageAnnotatorClient()
        content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if not texts:
            return JsonResponse({'error': 'No text found'}, status=404)
        
        detected_text = texts[0].description

        print(f"Texto detectado: {detected_text}")

        return JsonResponse({'text': detected_text})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)