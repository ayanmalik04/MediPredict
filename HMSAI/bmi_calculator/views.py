# bmi_calculator/views.py

from django.shortcuts import render

def bmi_calculator(request):
    # Handle form submission and BMI calculation logic here
    if request.method == 'POST':
        # Retrieve weight and height from form
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height')) / 100  # Convert height to meters

        # Calculate BMI
        bmi = weight / (height * height)

        # Render result template with BMI value
        return render(request, 'bmi_result.html', {'bmi': bmi})

    # Render BMI calculator form template for GET request
    return render(request, 'bmi_form.html')
