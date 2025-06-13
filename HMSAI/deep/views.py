from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template
from django.conf import settings

import os
import uuid
import numpy as np
import logging
from io import BytesIO

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)


def covid(request):
    return render(request, 'covid.html')


def load_filter_model():
    filter_model_path = os.path.join(settings.BASE_DIR, 'HMSAI', 'model', 'XraysNew10.h5')
    if not os.path.exists(filter_model_path):
        logger.error(f"Filter model not found at: {filter_model_path}")
        raise FileNotFoundError(f"Filter model missing at: {filter_model_path}")
    return load_model(filter_model_path)


# Load filter model once at server startup
try:
    filter_model = load_filter_model()
except Exception as e:
    filter_model = None
    logger.error(f"Failed to load filter model: {e}")


def is_xray_image(img_array):
    if not filter_model:
        raise RuntimeError("Filter model is not loaded.")
    prediction = filter_model.predict(img_array)
    return prediction[0][0] >= 0.5  # Threshold can be adjusted


def predict_image_covid(request):
    if 'image' not in request.FILES:
        return HttpResponseBadRequest("No file uploaded")

    file_obj = request.FILES['image']
    fs = FileSystemStorage()

    filename = str(uuid.uuid4()) + os.path.splitext(file_obj.name)[-1]
    filepath = fs.save(filename, file_obj)

    try:
        img = image.load_img(fs.path(filepath), target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        if not is_xray_image(img_array):
            return HttpResponseBadRequest("The uploaded image is not an X-ray")

        # Load trained COVID detection model
        model_path = os.path.join(settings.BASE_DIR, 'HMSAI', 'model', 'cnnwithoutpretrained.h5')
        if not os.path.exists(model_path):
            logger.error(f"COVID model not found at: {model_path}")
            return HttpResponse("Model not found on server.", status=500)

        model = load_model(model_path)

        predictions = model.predict(img_array)
        predicted_class = "You have Covid" if predictions[0][0] > 0.05 else "Normal"

        context = {
            'filepath': fs.url(filename),
            'prediction': predicted_class
        }
        return render(request, 'resultcov.html', context)

    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        return HttpResponse("Error processing image", status=500)


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
        logger.error(f"Error processing PDF generation: {e}")
        return HttpResponse("Error processing request", status=500)
