from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Block


def do_login(request):
    print(request.headers)
    query = request.GET
    username = query['username']
    password = query['password']
    user = authenticate(request, username=username, password=password)
    response = {'login':'failed'}
    if user is not None:
        login(request, user)
        response['login'] = 'success'

    return JsonResponse(response)

def do_logout(request):
    print(request.headers)
    response = {'logout':'success'}
    logout(request)
    return JsonResponse(response)

#@login_required(redirect_field_name="", login_url="login/")
def create_block(request):
    response = {}
    if not request.user.is_authenticated:
        response['error'] = 'Not authenticated'
        return JsonResponse(response)

    query = request.GET
    try:
        block = Block()
        block.data = query['data']
        block.user = request.user
        block.block_type = query['block_type']
        block.save()
        response['block'] = block.get_content()
    except Exception as e:
        response['error'] = str(e)
    
    return JsonResponse(response)
    
    
#@login_required(redirect_field_name="", login_url="/login/")
def get_chain(request):
    print(request.headers)
    response = {
        'user': None,
        'chain': None
    }
    if request.user.is_authenticated:
        user = request.user
        objs = Block.objects.all()
        objs = [i.get_content() for i in objs]
        response['user'] = user.username
        response['chain'] =  objs

    return JsonResponse(response)

def verify(request):
    response = {}
    if request.user.is_authenticated:
        response['verified'] = Block.verify()
    return JsonResponse(response)