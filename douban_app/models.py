from django.db import models

# Create your models here.
# 建表命令
# python manage.py makemigrations
# python manage.py migrate


# class User(models.Model):
#     name = models.CharField(max_length=30,unique=True)
#     username = models.CharField(max_length=20,unique=True)
#     password = models.CharField(max_length=20)
    
    
class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True,verbose_name="电影ID")  
    name = models.CharField(max_length=110,verbose_name="电影名")   # 电影名
    alias = models.CharField(max_length=200,verbose_name="别名")  # 别名
    actors = models.TextField(verbose_name="主演")   # 主演
    cover = models.CharField(max_length=150,verbose_name="封面地址")  # 封面地址
    directors = models.CharField(max_length=150,verbose_name="导演")  # 导演
    genres = models.CharField(max_length=50,verbose_name="类型")  # 类型
    regions = models.CharField(max_length=100,verbose_name="制片国家/地区")  # 制片国家/地区
    languages = models.CharField(max_length=60,verbose_name="语言")  # 语言
    release_year = models.CharField(max_length=4,verbose_name="上映年份")  # 上映年份
    mins = models.IntegerField(verbose_name="片长") # 片长
    score = models.FloatField(verbose_name="豆瓣评分")  # 豆瓣评分
    storyline = models.TextField(verbose_name="电影描述")  # 电影描述
    
    
    
    class Meta:
        verbose_name = '电影信息管理'
        verbose_name_plural = verbose_name
    

    
    

class Person(models.Model):
    person_id = models.IntegerField(primary_key=True,verbose_name="演员ID")
    name = models.CharField(max_length=50,verbose_name="演员姓名")
    sex = models.CharField(max_length=4,verbose_name="演员性别")
    
    class Meta:
        verbose_name = '演员信息管理'
        verbose_name_plural = verbose_name
    
    
    
class Comments(models.Model):
    comment_id = models.IntegerField(primary_key=True,verbose_name="评论ID")  # 评论id
    movie_id = models.IntegerField(verbose_name="电影ID")  # 电影编号
    content = models.TextField(verbose_name="评论内容")  # 评论内容
    
    class Meta:
        verbose_name = '评论信息管理'
        verbose_name_plural = verbose_name
    
    

class Ratings(models.Model):
    user_id = models.IntegerField(verbose_name="用户ID")
    movie_id = models.IntegerField(verbose_name="电影ID")
    rating = models.IntegerField(verbose_name="评分等级")
    
    class Meta:
        verbose_name = '评分信息管理'
        verbose_name_plural = verbose_name
        unique_together=("user_id","movie_id")
    

class Genres(models.Model):
    movie_id = models.IntegerField(verbose_name="电影ID")
    movie_name = models.CharField(max_length=110,verbose_name="电影名")
    genre = models.CharField(max_length=15,verbose_name="类型")
    
    class Meta:
        verbose_name = '类型信息管理'
        verbose_name_plural = verbose_name
    
class Subject(models.Model):
    movie_id = models.IntegerField(unique=True,verbose_name="电影ID")
    
class Languages(models.Model):
    movie_id = models.IntegerField(verbose_name="电影ID")
    movie_name = models.CharField(max_length=110,verbose_name="电影名")
    language = models.CharField(max_length=50,verbose_name="语种")
    
    class Meta:
        verbose_name = '语种信息管理'
        verbose_name_plural = verbose_name
        
class Collect(models.Model):
    user_id = models.IntegerField(verbose_name="用户ID")
    movie_id = models.IntegerField(verbose_name="电影ID")
    is_collect = models.BooleanField(verbose_name="是否收藏")
    
    class Meta:
        verbose_name = '收藏信息管理'
        verbose_name_plural = verbose_name