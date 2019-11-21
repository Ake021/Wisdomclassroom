from django.shortcuts import render, HttpResponse, redirect
from WC_app import models
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os


# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        user_obj = models.User.objects.filter(name=name, pwd=pwd).first()
        if user_obj:
            return HttpResponse('index.html')
        else:
            return HttpResponse('用户名或密码错误')


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        img = request.FILES.get('img')
        path = settings.MEDIA_ROOT
        file = 'pictures'
        pic_path = path + '/' + file
        print(pic_path)
        isExists = os.path.exists(pic_path)
        if isExists:
            print("目录已经存在")
        else:
            os.mkdir(pic_path)
            print("创建成功")
        img_url = pic_path + '/' + img.name
        print(img_url)
        with open(img_url, 'wb') as f:
            for data in img.chunks():
                f.write(data)

    return HttpResponse('图片未上传')
