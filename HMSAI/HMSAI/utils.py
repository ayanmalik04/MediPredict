def check_authentication(request):
    return 'user_id' in request.session