from django.http import HttpResponse
from TestModle.models import Test
from TestModle.models import weathers
from TestModle.models import dontai
from django.shortcuts import render
import MySQLdb

#数据库操作
def testdb(request):
   
    allList = Test.objects.all()#获取top250电影
    weather = weathers.objects.all()#获取天
    dontais=dontai.objects.all()#获取动态信息
    
    Test.objects.order_by("id")

    
    return render(request,'base1.html',{'allList':allList,'weather':weather,'dontais':dontais})
       
