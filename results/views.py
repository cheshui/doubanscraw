import os
import time
from threading import Thread

import django_excel as excel
import xlrd
from django import forms
from django.db import connection
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import View
from douban import settings
from douban.settings import BASE_DIR

from . import models

# Create your views here.



def trun_tab():
    # 创建获取游标对象
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE results_lists')

def index_view(request):
    playlist = models.Lists.objects.all().order_by('id')
    return render(request, 'index.html', locals())


# 将excel数据写入mysql
def wrdb(filename):
    readboot = xlrd.open_workbook(settings.UPLOAD_ROOT + "/" + filename)
    sheet = readboot.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    print('wrdb')
    for row in range(1, rows):
        comic = models.Lists()
        comic.id = int(sheet.cell_value(row, 0))
        comic.name = sheet.cell_value(row, 1)
        comic.save()
    print('wrdb_finish')


@csrf_exempt
def upload(request):
    file = request.FILES.get('file')
    print('upload:%s' % file.name)
    if not os.path.exists(settings.UPLOAD_ROOT):
        os.makedirs(settings.UPLOAD_ROOT)
    try:
        if file is None:
            return HttpResponse('请选择要上传的文件')
        # 循环二进制写入
        with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)
        print('open_finish')

        # 写入 mysql
        trun_tab()
        wrdb(file.name)
    except Exception as e:
        return HttpResponse(e)

    return HttpResponseRedirect('http://localhost:8000/')
