from django.shortcuts import render, redirect, HttpResponse
from loginsys.forms import UserloginForm , LoginForm
from loginsys.models import Userlogin
from loginsys.forms import PointaDataForm
from loginsys.models import PointaData11
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string
from django.template import Context
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from .models import Userlogin, ContactMessages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PointaDataForm
from .models import PointaData11

from .forms import ContactForm 

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the data to the ContactMessage model
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')  # Redirect to a thank you page or the same contact page
    else:
        form = ContactForm()

    return render(request, 'index.html', {'form': form})
# View for the home page
def home(request):
    return render(request, 'index.html')

# View for the login form
def LogForm(request):
    if 'user_id' in request.session: return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = Userlogin.objects.filter(username=username).first()
            if user and password == user.password:
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username  # Store the username in the session
                    return redirect('test')  # Redirect to the testing page upon successful login
            else:
                    messages.error(request, "Invalid Username or Password. Try again.")
                    return redirect('loginform')
    else:
        form = LoginForm()
    return render(request, 'loginform.html', {'form': form})


def sign_up(request):
    if 'user_id' in request.session:
        return redirect('home')

    if request.method == 'POST':
        form = UserloginForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('loginform')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserloginForm()
    return render(request, 'signup.html', {'form': form})

# View for logout
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('home')  # Redirect to the login page after logging out

def home(request):
    return render(request, 'index.html')


def testing(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Userlogin.objects.get(id=user_id)
        return render(request, 'test.html', {'user': user})
    else:
        messages.error(request, "Unauthorized access. Please log in first.")
        return redirect('loginform')

def bookingappoinment(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Userlogin.objects.get(id=user_id)
        return render(request, 'booking.html', {'user': user})  # Adjust template name as per your project
    else:
        messages.error(request, "Unauthorized access. Please log in first.")
        return redirect('loginform') 

def view(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Userlogin.objects.get(id=user_id)
        return render(request, 'viewappoint.html', {'user': user})  # Adjust template name as per your project
    else:
        messages.error(request, "Unauthorized access. Please log in first.")
        return redirect('loginform')


def bookingappoinment(request):
    if request.method == 'POST':
        form = PointaDataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment scheduled successfully!')
            return redirect('booking')  # Redirect to a success page
        else:
            messages.error(request, 'There was an error scheduling your appointment. Please try again.')
    else:
        form = PointaDataForm()

    # Filter out already booked time slots
    booked_slots = PointaData11.objects.values_list('time_slot', flat=True)
    form.fields['time_slot'].choices = [(slot, label) for slot, label in form.fields['time_slot'].choices if slot not in booked_slots]

    return render(request, 'booking.html', {'form': form})





def view(request):
    vee = PointaData11.objects.all()
    return render(request, 'viewappoint.html', {'vee': vee})

def generate_pdf(request):
    vee = PointaData11.objects.all()
    context = {'vee': vee}
    pdf = render_to_pdf('viewappoint.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="user_table.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=400)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



def download(request, id):
    # Fetch the newly inserted data using the ID passed from the form submission
    new_data = PointaData11.objects.get(pk=id)  # Replace PointaData with your actual model
    eee_list = [new_data]
    return render(request, 'download.html', {'eee': eee_list})


def generate_pdf_down(request, id):
    # Fetch the data based on the provided ID
    instance = PointaData11.objects.get(pk=id)
    context = {'eee': [instance]}
    
    pdf = render_to_pdf_down('download.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="AppointmentData.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=400)

def render_to_pdf_down(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)  # Pass context_dict instead of Context(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def mldl(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Userlogin.objects.get(id=user_id)
        return render(request, 'AI.html', {'user': user})  # Adjust template name as per your project
    else:
        messages.error(request, "Unauthorized access. Please log in first.")
        return redirect('loginform')