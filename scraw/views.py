import os
import re
import time
import urllib
from io import BytesIO

import numpy as np
import pandas as pd
import xlwt
from django.db import connection
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render
from results import models
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Create your views here.


def gen_Urls(mov):
    urls = []
    rows = len(mov)
    for i in range(rows):
        name = urllib.parse.quote(mov[i])
        url = 'https://search.douban.com/movie/subject_search?search_text=' + name
        urls.append(url)
    return urls


def get_detail(url):
    browser = webdriver.PhantomJS()
    try:
        browser.get(url)
        time.sleep(2)
        input = browser.find_element_by_class_name('detail').text
        return input
    except Exception as e:
        print(e)
    finally:
        browser.quit()


def match_info(text):
    k1 = text.splitlines()
    k2 = re.search('(.*)[(]([0-9]{4}).*', k1[0])
    k3 = re.search('([0-9]?\.[0-9]?)[()]([0-9]*).*[()]', k1[1])
    return (k2[1], k2[2], k3[1], k3[2])


def insertdb():
    movlist = list(models.Lists.objects.values_list('name', flat=True))
    urls = gen_Urls(movlist)
    file = []
    row = 1
    cursor = connection.cursor()
    cursor.execute('TRUNCATE table results_final_lists;')
    for url in urls:
        try:
            detail = get_detail(url)
            info = match_info(detail)
            cursor.execute('INSERT INTO results_final_lists values (%s, %s, %s, %s, %s);', [
                           int(row), info[0], int(info[1]), info[2], int(info[3])])
        except Exception as e:
            print(str(row))
            print(e)
        finally:
            row = row + 1


def resultview(request):
    # return HttpResponse('查询中，请稍候!')
    insertdb()
    playlist1 = models.Final_Lists.objects.all().order_by('id')
    context = {'playlist2': playlist1}
    print(context)
    return render(request, 'import_data.html', context)


def exportexcel(request):
    resultdb = models.Final_Lists.objects.all().order_by('id')
    print(resultdb)
    temp = []
    for i in resultdb:
        t = [i.id, i.name, i.year, i.score, i.ratenum]
        temp.append(t)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=resluts.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('查询结果')
    sheet.write(0, 0, '序号')
    sheet.write(0, 1, '节目名称')
    sheet.write(0, 2, '年份')
    sheet.write(0, 3, '节目评分')
    sheet.write(0, 4, '评价人数')
    row = 1
    for m in temp:
        for j in range(len(m)):
            sheet.write(row,j,m[j])
        row = row + 1
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response
