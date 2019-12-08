from django.shortcuts import render, HttpResponse, redirect
from WC_app import models
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from aip import AipFace
import json
import base64
import cv2
import shutil
from aip import AipImageClassify


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
            return render(request, "index.html", )
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

        client = AipFace('17815113', '05mBey1pCfocw0F4QlpG6qEK', 'wYnGQaNV7exLZvitmUtlzM4lzKs9odjd')

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
        options["face_field"] = "emotion,face_shape,expression"
        options["max_face_num"] = 2
        options["face_type"] = "LIVE"
        options["liveness_control"] = "LOW"

        """ 带参数调用人脸检测 """
        result = client.detect(image, imageType, options)
        temp = {}
        fea = ['emotion', 'face_shape', 'expression']
        print(result)
        """for a in fea:
            temp[a] = result['result']['face_list'][0][a]
        stus = {'emotion': temp['emotion']}
        print(temp)"""
        stus = temp

        def sss(img_url):
            APP_ID = '17926029'
            API_KEY = 'dvzmdFFaMFidNass4pZcYals'
            SECRET_KEY = 'GTRmEpFHT1zXVNEhWX3rzzfLgXFkLREf'
            client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
            print(img_url)
            def get_file_content(img):
                with open(img, 'rb') as fp:
                    return fp.read()
            image = get_file_content(img_url)
            #	调用通用物体识别
            client.advancedGeneral(image)
            #	如果有可选参数
            options = {}
            options["baike_num"] = 5
            #	带参数调用通用物体识别
            result = client.advancedGeneral(image, options)
            return result
        print(sss(img_url))
        return render(request, 'playback.html', {'stus': stus})
        # myjson = json.dumps(result['result']['face_list'][0])
        # print(myjson)

    return HttpResponse('图片未上传')


@csrf_exempt
def video(request):
    if request.method == 'GET':

        path = settings.MEDIA_ROOT
        file = 'pictures'
        pic_path = path + '/' + file
        # 视频文件名字
        filename = 'test.mov'

        # 保存图片的路径
        savedpath = pic_path + '/' + filename.split('.')[0] + '/'
        isExists = os.path.exists(savedpath)
        if not isExists:
            os.makedirs(savedpath)
            print('path of %s is build' % (savedpath))
        else:
            shutil.rmtree(savedpath)

        # 视频帧率12
        fps = 12
        # 保存图片的帧率间隔
        count = 10

        # 开始读视频
        videoCapture = cv2.VideoCapture('media/' + filename)
        i = 0
        j = 0

        while True:
            success, frame = videoCapture.read()
            i += 1
            if i % count == 0:
                # 保存图片
                j += 1
                savedname = filename.split('.')[0] + '_' + str(j) + '_' + str(i) + '.jpg'
                cv2.imwrite(savedpath + savedname, frame)
                print('image of %s is saved' % (savedname))
            if not success:
                print('video is all read')
                break
    return HttpResponse('成功')
