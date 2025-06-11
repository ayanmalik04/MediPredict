from django.shortcuts import render
from joblib import load
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse

# Create your views here.
def dai(request):
    return render(request, 'daibetes.html')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def daibres(request):
    model = load('./SavedModels/Diabiting.joblib')
    
    Pregnancies = request.GET.get('Pregnancies', '')
    Glucose = request.GET.get('Glucose', '')
    BloodPressure = request.GET.get('BloodPressure', '')
    SkinThickness = request.GET.get('SkinThickness', '')
    Insulin = request.GET.get('Insulin', '')
    BMI = request.GET.get('BMI', '')
    DiabetesPedigreeFunction = request.GET.get('DiabetesPedigreeFunction', '')
    Age = request.GET.get('Age', '')

    # Assuming 'model' is your trained machine learning model
    y_pred = model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
    print(y_pred)

    if y_pred[0] == 0:
        y_pred_text = "You Are Safe From Diabetes"
    else:
        y_pred_text = "You have diabetes!! Consult a Doctor As Soon As Possible"

    context = {
        'input_data': {
            'Pregnancies': Pregnancies,
            'Glucose': Glucose,
            'BloodPressure': BloodPressure,
            'SkinThickness': SkinThickness,
            'Insulin': Insulin,
            'BMI': BMI,
            'DiabetesPedigreeFunction': DiabetesPedigreeFunction,
            'Age': Age,
        },
        'result': y_pred_text,
    }

    return render(request, 'daibres.html', context)

def generate_pdf_dia(request):
    model = load('./SavedModels/Diabiting.joblib')
    
    Pregnancies = request.GET.get('Pregnancies', '')
    Glucose = request.GET.get('Glucose', '')
    BloodPressure = request.GET.get('BloodPressure', '')
    SkinThickness = request.GET.get('SkinThickness', '')
    Insulin = request.GET.get('Insulin', '')
    BMI = request.GET.get('BMI', '')
    DiabetesPedigreeFunction = request.GET.get('DiabetesPedigreeFunction', '')
    Age = request.GET.get('Age', '')

    y_pred = model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
    print(y_pred)

    if y_pred[0] == 0:
        y_pred_text = "You Are Safe From Heart Diabetes"
    else:
        y_pred_text = "You have Heart Diabetes!! Consult a Doctor As Soon As Possible"

    context = {
        'input_data': {
            'Pregnancies': Pregnancies,
            'Glucose': Glucose,
            'BloodPressure': BloodPressure,
            'SkinThickness': SkinThickness,
            'Insulin': Insulin,
            'BMI': BMI,
            'DiabetesPedigreeFunction': DiabetesPedigreeFunction,
            'Age': Age,
        },
        'result': y_pred_text,
    }

    pdf = render_to_pdf('daibres.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="diabetes_result.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=400)



