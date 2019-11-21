from django.shortcuts import render, HttpResponse, redirect
from WC_app import models
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from aip import AipFace
import json
import base64

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

        APP_ID = '17815113'
        API_KEY = '05mBey1pCfocw0F4QlpG6qEK'
        SECRET_KEY = 'wYnGQaNV7exLZvitmUtlzM4lzKs9odjd'
        client = AipFace(APP_ID, API_KEY, SECRET_KEY)

        with open(img_url, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            print('data:image/jpeg;base64,%s' % s)

        image = s

        imageType = "BASE64"

        """ 调用人脸检测 """
        client.detect(image, imageType);

        """ 如果有可选参数 """
        options = {}
        options["face_field"] = "age,emotion,expression,gender,race,glasses,beauty,face_shape"
        options["max_face_num"] = 2
        options["face_type"] = "LIVE"
        options["liveness_control"] = "LOW"

        """ 带参数调用人脸检测 """
        result = client.detect(image, imageType, options)
        temp = {}
        temp['emotion'] = result['result']['face_list'][0]['emotion']
        temp['age'] = result['result']['face_list'][0]['age']
        temp['gender'] = result['result']['face_list'][0]['gender']
        temp['race'] = result['result']['face_list'][0]['race']
        temp['glasses'] = result['result']['face_list'][0]['glasses']
        temp['beauty'] = result['result']['face_list'][0]['beauty']
        temp['face_shape'] = result['result']['face_list'][0]['face_shape']
        stus = json.dumps(temp)
        print(stus)
        return render(request, 'home.html', {'stus':stus})
        #myjson = json.dumps(result['result']['face_list'][0])
        #print(myjson)

    return HttpResponse('图片未上传')