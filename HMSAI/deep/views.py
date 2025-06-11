from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
import os
import uuid
import numpy as np
from django.http import HttpResponseBadRequest
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model 
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
import logging


logger = logging.getLogger(__name__)



def covid(request):
    return render(request, 'covid.html')


def load_filter_model():
    # Load the pre-trained X-ray filter model
    filter_model_path = 'D:/All Projects Important/MediPredictFinal/MediPredict/HMSAI/model/XraysNew10.h5'  # Replace with the actual path to your filter model
    return load_model(filter_model_path)

# Load the filter model once when the server starts
filter_model = load_filter_model()

def is_xray_image(img_array):
    # Use the filter model to predict if the image is an X-ray
    prediction = filter_model.predict(img_array)
    # Return True if the prediction confidence is above a threshold (0.5 here)
    return prediction[0][0] >= 0.5  # Adjust threshold based on your filter model



def predict_image_covid(request):
    # Check if 'image' file is present in the request.FILES
    if 'image' not in request.FILES:
        return HttpResponseBadRequest("No file uploaded")

    file_obj = request.FILES['image']
    fs = FileSystemStorage()

    # Generate a unique filename to avoid overwriting existing files
    filename = str(uuid.uuid4()) + os.path.splitext(file_obj.name)[-1]
    filepath = fs.save(filename, file_obj)

    # Process the uploaded image
    img = image.load_img(fs.path(filepath), target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image data


    # Check if the image is an X-ray
    if not is_xray_image(img_array):
        return HttpResponseBadRequest("The uploaded image is not an X-ray")
    
    # Load the trained model
    model_path = 'D:/All Projects Important/MediPredictFinal/MediPredict/HMSAI/model/cnnwithoutpretrained.h5'  # Replace with the actual path to your trained model
    model = load_model(model_path)

    # Make prediction
    predictions = model.predict(img_array)
    
    # Assuming binary classification, get the predicted class
    predicted_class = "You have Covid" if predictions[0][0] > 0.05 else "Normal"

    # Pass the prediction result and image path to the template
    context = {
        'filepath': fs.url(filename),
        'prediction': predicted_class
        
    }
    return render(request, 'resultcov.html', context)








def render_to_pdf(template_src, context_dict={}):
    try:
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            return result.getvalue()
    except Exception as e:
        logger.error(f"Error rendering PDF: {e}")
    return None

def pdf_covid(request):
    try:
        filepath = request.GET.get('filepath')
        prediction = request.GET.get('prediction')

        if not filepath or not prediction:
            return HttpResponse("Missing parameters", status=400)

        # Build absolute URI for the image file
        image_url = request.build_absolute_uri(filepath)

        context = {
            'filepath': image_url,
            'prediction': prediction
        }

        pdf_content = render_to_pdf('resultcov.html', context)
        if pdf_content:
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="covidResult_result.pdf"'
            return response
        else:
            return HttpResponse("Error generating PDF", status=400)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return HttpResponse("Error processing request", status=500)


