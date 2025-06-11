from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib import messages  # Ensure this import is here
from loginsys import views as log1  # Adjust import as per your project
from bmi_calculator import views as bi
from AIDB import views as ml
from deep import views as covid
from django.conf import settings
from django.conf.urls.static import static

def check_authentication(request):
    return 'user_id' in request.session

def authenticated_view_wrapper(view_func):
    def wrapper(request, *args, **kwargs):
        if check_authentication(request):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Unauthorized access. Please log in first.")
            return redirect('loginform')  # Adjust 'loginform' to your login URL
    return wrapper

urlpatterns = [
    path('', log1.home, name='home'),
    path('login/', log1.LogForm, name='loginform'),
    path('signup/', log1.sign_up, name='signup'),
    path('test', authenticated_view_wrapper(log1.testing), name='test'),
    path('booking/', authenticated_view_wrapper(log1.bookingappoinment), name='booking'),  # Protected view
    path('view', authenticated_view_wrapper(log1.view), name='view'),
    path('view/pdf', log1.generate_pdf, name='pdf'),
    path('AI', authenticated_view_wrapper(log1.mldl), name='AI'),
    path('daibetes', authenticated_view_wrapper(ml.dai), name='daibetes'),
    path('daibres', ml.daibres, name='daibres'),
    path('daibres/pdf', ml.generate_pdf_dia, name='pdf_dia'),
    path('covid', authenticated_view_wrapper(covid.covid), name='covid'),
    path('resultcov', covid.predict_image_covid, name='resultcov'),
    path('resultcov/pdfcov/', covid.pdf_covid, name='pdfcov'),
    path('download/<int:id>/', log1.download, name='download'),
    path('download/<int:id>/pdf', log1.generate_pdf_down, name='pdf_down'),
    path('logout/', log1.logout_view, name='logout'),
    path('bmi_calculator', authenticated_view_wrapper(bi.bmi_calculator), name='bmi_calculate'),  # Include BMI calculator app URLs
    path('contact/', log1.contact_view, name='contact_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
