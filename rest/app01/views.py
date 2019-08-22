import json
import view as view
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers


# Create your views here.
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *

from rest_framework import serializers
# 为queryset做序列化
class PublishSerializers(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()

# class BookSerializers(serializers.Serializer):
#     title = serializers.CharField()
#     price = serializers.IntegerField()
#     pub_date = serializers.DateField()
#     publish = serializers.CharField(source='publish.name')#一对多
#     # authors = serializers.CharField(source='authors.all') #多对多
#     authors = serializers.SerializerMethodField() #多对多
#     def get_authors(self,obj):
#         temp=[]
#         for obj in obj.authors.all():
#             temp.append(obj.name)
#         return temp

class BookModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    publish = serializers.CharField(source='publish.pk')
    # authors = serializers.SerializerMethodField()  # 多对多
    # def get_authors(self, obj):
    #      temp=[]
    #      for obj in obj.authors.all():
    #          temp.append(obj.name)
    #      return temp
    def create(self, validated_data):
        print(validated_data)
        # book=Book.objects.create(title=validated_data['title'],price=validated_data['price'],pub_date=validated_data['pub_date'],publish=validated_data['publish']['pk'])
        # book.authors.add(validated_data['authors'])
        # return book
        authors = validated_data.pop('authors')
        obj = Book.objects.create(title=validated_data['title'],price=validated_data['price'],pub_date=validated_data['pub_date'], publish_id=validated_data['publish']['pk'])
        obj.authors.add(*authors)
        return obj

class PublashView(APIView):
    def get(self, requset):
        # 方法一
        # publish_list= list(Publish.objects.all().values('name','email'))
        # 方法二
        # temp=[]
        # for publish in Publish.objects.all():
        #     temp.append({
        #         'name':publish.name,
        #         'email':publish.email
        #     })
        # return  HttpResponse(json.dumps(temp))
        # 方法三
        # temp=[]
        # for publish in Publish.objects.all():
        #     temp.append(model_to_dict(publish))
        # return  HttpResponse(json.dumps(temp))
        # 方法四
        # ret = serializers.serialize('json',Publish.objects.all())
        # return HttpResponse(ret)
        # 方式四：restframework
        print(requset.GET)
        return HttpResponse(requset.GET)
    def post(self,request):
        print(request.POST)

        print(request.data)
        #
        return HttpResponse('POST')


class BookView(APIView):
    def get(self,request):
        book_list = Book.objects.all()
        bs = BookModelSerializers(book_list,many=True)
        return Response(bs.data)



    def post(self,request):
        # POST请求的数据
        bs = BookModelSerializers(data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)




