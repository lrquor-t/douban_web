import random
import re
from django.db import IntegrityError
from django.shortcuts import render,redirect,HttpResponse
from douban_app.models import Movie,Person,Comments,Ratings,Collect
from django.db.models import Count, Min, Max, Sum
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.cache import cache_page
import json
from bs4 import BeautifulSoup
import time
import jieba
import wordcloud
from imageio import imread
from django.core.mail import send_mail
from django.core.cache import cache
import pymysql
import requests
from fake_useragent import UserAgent
from django.utils.safestring import mark_safe
from verify_email import verify_email

# Create your views here.

@cache_page(60 * 15)
def index(request):
    if request.user.is_authenticated:
        print(request.session.get('_auth_user_id'))
        total = Movie.objects.count()
        total_23 = Movie.objects.filter(release_year="2023").count()
        person_total = Person.objects.count()
        score = Movie.objects.all().aggregate(Max("score"))
        url="https://m.maoyan.com/ajax/movieOnInfoList" # 正在热映
        dic_h = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            }
        data = ''
        try:
            r = requests.get(url=url,headers = dic_h).text
            data = json.loads(r)
        except:
            with open('douban_app\\data\\正在热映.txt','r',encoding='utf8') as f:
                data_str = f.read()
                data = json.loads(data_str)
        movieList = data["movieList"]
        url2 = "https://m.maoyan.com/ajax/comingList?ci=10&token=&limit=12" # 即将上映
        r2 = requests.get(url=url2,headers = dic_h).text
        data_2 = ''
        try:
            data_2 = json.loads(r2)
        except:
            with open('douban_app\\data\\即将上映.txt','r',encoding='utf8') as f:
                data_str = f.read()
                data_2 = json.loads(data_str)
        movie_j = data_2["coming"]
        return render(request,'index.html',{"total":total,"total_23":total_23,"person_total":person_total,"max_score":score["score__max"],"movieList":movieList,"movie_j":movie_j})
    else:
        return redirect("/")

# @csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        message = ''
        active = ''
        if not User.objects.filter(username=username).exists():
            message = '该用户不存在'
            return render(request, 'login.html', locals())
        user = authenticate(username=username,password=password)
        if user:
            if not user.is_active:
                request.session["email"] = username
                active = '邮箱暂未激活，请前往<a href="/mail/active/" >激活</a>。'
                active = mark_safe(active)
                return render(request, 'login.html', locals())
            else:
                login(request,user)
                return redirect("/index/")
        else:
            message = '账号或密码不正确'
            return render(request, 'login.html', locals())
    else:
        if request.user.is_authenticated:
            return redirect("/index/")
        return render(request, 'login.html')

def checkloginname(request):
    '''检查登录页面邮箱'''
    username = request.GET.get('username')
    user = User.objects.filter(username=username)
    if user:
        return HttpResponse('')
    else:
        return HttpResponse('邮箱未注册!')

def checkusername(request):
    '''检查注册页面邮箱'''
    username = request.GET.get('username')
    user = User.objects.filter(username=username)
    if user:
        return HttpResponse('邮箱已被注册!')
    else:
        return HttpResponse('')
        # if verify_email(username):
        #     return HttpResponse('')
        # else:
        #     return HttpResponse('邮箱格式错误！')  

def checkpasswd(request):
    '''检查注册页面密码'''
    password = request.GET.get('password')
    againpasswd = request.GET.get('againpassword')
    if password != againpasswd:
        return HttpResponse('两次密码不一致!')
    else:
        return HttpResponse('')

def checkPasswdStrength(request):
    '''检查注册页面密码强度'''
    password = request.GET.get('password')
    if len(password) < 8:
        return HttpResponse('密码长度太短！')
    elif len(password) > 19:
        return HttpResponse('密码长度太长！')
    else:
        if re.findall(r'[a-z]',password) and re.findall(r'[A-Z]',password) and re.findall(r'\d',password):
            return HttpResponse('')
        else:
            return HttpResponse('密码强度不够，请包含大小写字母以及数字!')
      
def signup(request):
    if request.method == "POST":
        message = ''
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('email')
        password = request.POST.get('password')
        again_password = request.POST.get('again_password')
        # 判断两次密码是否一样
        if password != again_password:
            message = '密码输入不一致'
            return render(request,'signup.html',locals())
        User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,is_active=0)
        return redirect("/")
    else:
        return render(request,"signup.html")

def logout_user(request):
    logout(request)
    cache.clear()
    return redirect("/")

def reset_password(request):
    username = request.GET.get("reg-email")
    print(username)
    return render(request,"reset-password.html")

@cache_page(60 * 15)
def top10(request):
    if request.user.is_authenticated:
        url = 'https://api.wmdb.tv/api/v1/top?type=Douban&skip=0&limit=10&lang=Cn'
        # url1 = 'https://api.wmdb.tv/api/v1/top?type=Imdb&skip=0&limit=10&lang=Cn'
        USER_AGENT = UserAgent().random
        headers = {
            'User-Agent':USER_AGENT
        }
        data = requests.get(url,headers=headers).json()
        top10_data = [ {
                "doubanId":movie["doubanId"],
                "name":movie["data"][0]["name"]+'/'+movie["originalName"],
                "cover":movie["data"][0]["poster"],
                "genre":movie["data"][0]["genre"],
                "language":movie["data"][0]["language"],
                "country":movie["data"][0]["country"],
                "year":movie["year"],
                "doubanRating":movie["doubanRating"]
            } for movie in data ]
        return render(request,"top10.html",{"movietop10":top10_data})
    else:
        return redirect("/")

# @cache_page(60 * 15)
def search(request):
    if request.user.is_authenticated:
        movie_name = request.GET.get("search")
        if movie_name:
            url = "https://api.wmdb.tv/api/v1/movie/search?q="+movie_name+"&limit=10&skip=0&lang=Cn"
            data = requests.get(url).json()
            search_data = [ {
                    "name":movie["data"][0].get("name",""),
                    "cover":movie["data"][0].get("poster",""),
                    "genre":movie["data"][0].get("genre","未知"),
                    "language":movie["data"][0].get("language","未知"),
                    "country":movie["data"][0].get("country","未知"),
                    "year":movie.get("year","未知"),
                    "doubanRating":movie.get("doubanRating","未知"),
                    "doubanId":movie.get("doubanId"),
                } for movie in data ]
        else:
            search_data = ""
        return render(request,"search.html",{"search_data":search_data})
    else:
        return redirect("/")

def settings(request):
    id = request.session.get('_auth_user_id')
    user = User.objects.filter(id=id).first()
    data = {
        "username": user.username,
        "last_name": user.last_name,
        "first_name": user.first_name
    }
    return render(request,"settings.html",data)

def user_score(request,doubanId):
    return render(request,"pf.html",{"doubanId":doubanId})

def user_score_submit(request,doubanId):
    message = ""
    starNum = request.POST.get("starNum")
    customerEvaluationComment = request.POST.get("customerEvaluationComment")
    user_id = request.session.get('_auth_user_id')
    try:
        Ratings.objects.create(user_id=user_id,movie_id=doubanId,rating=starNum)
    except IntegrityError:
        message = "请勿重复评价!!!"
    return render(request,"pf.html",{"message":message})

def display(request):
    total = Movie.objects.count()
    # total_23 = Movie.objects.filter(release_year="2023").count()
    # person_total = Person.objects.count()
    # score = Movie.objects.all().aggregate(Max("score"))
    
    # 分类(按类型)
    db = pymysql.connect(host='123.60.184.157',
                        user='root',passwd='qQ147258@',db='db_douban',charset='utf8')
    cursor = db.cursor()
    cursor.execute("select genre,count(*) from douban_app_genres group by genre having genre!=''")
    genres = cursor.fetchall()
    genres_data = [{'value':v,'name':k} for k,v in genres]
    genres_data_tmp = sorted(genres_data,key=lambda i:i['value'],reverse=True)
    genres_data_5 = genres_data_tmp[:5]
    
    # 分类2(按时长)
    duration = []
    cursor.execute("select count(*) from douban_app_movie where mins>0 and mins<=60")
    movie_d = cursor.fetchall()
    duration.append({'value':movie_d[0][0],'name':"短片"})
    cursor.execute("select count(*) from douban_app_movie where mins>60 and mins<=90")
    movie_t = cursor.fetchall()
    duration.append({'value':movie_t[0][0],'name':"特殊影片"})
    cursor.execute("select count(*) from douban_app_movie where mins>90 and mins<=120")
    movie_y = cursor.fetchall()
    duration.append({'value':movie_y[0][0],'name':"一般电影"})
    cursor.execute("select count(*) from douban_app_movie where mins>120")
    movie_l = cursor.fetchall()
    duration.append({'value':movie_l[0][0],'name':"超长电影"})
    
    # 2023类型
    cursor.execute("select genre,count(*) from douban_app_genres where movie_id in (select movie_id from douban_app_movie where release_year='2023') group by genre having genre!=''")
    genres_2023 = cursor.fetchall()
    genres_2023_name = [ i[0] for i in genres_2023]
    genres_2023_num = [ i[1] for i in genres_2023]
    
    # 平均分
    cursor.execute("select release_year,sum(score)/count(*) from douban_app_movie where release_year!='' and release_year!='0' and score!=0  group by release_year")
    data = cursor.fetchall()
    avg_score_data = sorted(data,key=lambda i:i[0])
    avg_score_year = [i[0] for i in avg_score_data][-9:]
    avg_score = [round(i[1],2) for i in avg_score_data][-9:]
    avg_score_show = [i*10 for i in avg_score]
    
    # 电影总数
    res = Movie.objects.values("release_year").annotate(total=Count("release_year")).order_by("release_year").exclude(release_year="").exclude(release_year='0')
    year_data = [ i["release_year"] for i in res][:-11]
    year_total = [ i["total"] for i in res][:-11]
    # year = ['2023','2022','2021','2020','2019','2018','2017','2016','2015','2014']
    # year_data_10 = [ i["release_year"] for i in res if i["release_year"] in year]
    # year_total_10 = [ i["total"] for i in res if i["release_year"] in year]
    year_data_4 = year_data[-4:]
    year_total_4 = year_total[-4:]
    year_total_4_all = sum(year_total_4)
    year_total_avg = [round(i/year_total_4_all*100,1) for i in year_total_4]
    
    # douban_top
    url = 'https://api.wmdb.tv/api/v1/top?type=Douban&skip=0&limit=4&lang=Cn'
    # url1 = 'https://api.wmdb.tv/api/v1/top?type=Imdb&skip=0&limit=10&lang=Cn'
    USER_AGENT = UserAgent().random
    headers = {
        'User-Agent':USER_AGENT
    }
    res = requests.get(url,headers=headers).text
    data = json.loads(res)
    top4_data = []
    for movie in data:
        name = movie["data"][0]["name"]
        cover = movie["data"][0]["poster"]
        genre = movie["data"][0]["genre"]
        year = movie["year"]
        doubanRating = movie["doubanRating"]
        movie_data = {
            "name":name,
            "cover":cover,
            "genre":genre,
            "year":year,
            "doubanRating":doubanRating
        }
        top4_data.append(movie_data)
    # 演员
    actors_data_9 = [('曾志伟', 211), ('申星一', 188), ('任达华', 167), ('午马', 166), ('林雪', 163), ('尹静姬', 154), ('谷峰', 146), ('柯俊雄', 145), ('黄秋生', 141)]
    actors_data_name = [ i[0] for i in actors_data_9]
    actors_data_num = [ i[1] for i in actors_data_9]
    
    # 2023语种
    cursor.execute("select language,count(*) from douban_app_languages where movie_id in (select movie_id from douban_app_movie where release_year='2023') group by language having language!=''")
    language_2023 = cursor.fetchall()
    language_2023_name = [ i[0] for i in language_2023][:6]
    language_2023_num = [ i[1] for i in language_2023][:6]
    return render(request,"display.html",locals())

def help(request):
    return render(request,"help.html")

def account(request):
    return render(request,"account.html")

def comments(request,doubanId):
    # coding=utf8mb4
    if Comments.objects.filter(movie_id=doubanId).count():
        comments_data = Comments.objects.filter(movie_id=doubanId).values("content")
        s = ''
        for comment in comments_data:
            s += comment["content"]
    else:
        urls=['https://movie.douban.com/subject/{}/comments?start={}&limit=20&status=P&sort=new_score'.format(doubanId,str(i)) for i in range(0, 200, 20)] #通过观察的url翻页的规律，使用for循环得到10个链接，保存到urls列表中
        dic_h = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        comments_list = [] #初始化用于保存短评的列表
        for url in urls: #使用for循环分别获取每个页面的数据，保存到comments_list列表
            r = requests.get(url=url,headers = dic_h).text
            r = r.encode('utf8')
            soup = BeautifulSoup(r, 'lxml')
            ul = soup.find('div',id="comments")
            lis= ul.find_all('p')
            list2 =[]
            for li in lis:
                list2.append(li.find('span').string)
            # print(list2)
            comments_list.extend(list2)
            for k in comments_list:
                try:
                    Comments.objects.create(movie_id=doubanId,content=k)
                except:
                    pass
            time.sleep(random.randint(0,3)) # 暂停0~3秒
        s = ''
        for i in comments_list:
            s += i
    ls = jieba.lcut(s) # 生成分词列表
    text = ' '.join(ls) # 连接成字符串
    tag = random.randint(1,13)
    mask_image = imread("douban_app\\static\\img\\ciyun\\"+str(tag)+".png")
    wc = wordcloud.WordCloud(font_path="douban_app\\static\\font\\msyh.ttc",
                            width = 1000,
                            height = 700,
                            background_color='white',
                            max_words=100,stopwords=s,
                            mask=mask_image)
    wc.generate(text) # 加载词云文本
    wc.to_file("douban_app\\static\\img\\tmp\\1.png") # 保存词云文件
    return HttpResponse('成功')

def send_sms_code(request):
    """
    发送邮箱验证码
    :param to_mail: 发到这个邮箱
    :return: 成功 0 失败 -1
    """
    # 生成邮箱验证码
    sms_code = '%06d' % random.randint(0, 999999)
    EMAIL_FROM = "visualizatin@163.com"  # 邮箱来自
    to_email = request.session["email"]
    request.session["code"] = sms_code
    print(request.session["code"])
    email_title = '邮箱激活'
    email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
    send_status = send_mail(email_title,email_body,EMAIL_FROM,[to_email])
    if send_status == 1:
        return render(request, 'mail.html')
    else:
        return render(request, 'login.html')

def sms_active(request):
    message = ''
    if request.session["code"] == request.POST.get("code"):
        user = User.objects.get(username=request.session["email"])
        user.is_active = 1
        user.save()
        return redirect('/')
    else:
        message = "验证码输入错误！"
        return render(request, 'mail.html',{"message":message})

@cache_page(60 * 15)
def type_proportion(request):
    if request.user.is_authenticated:
        # coding=utf-8
        db = pymysql.connect(host='123.60.184.157',
                        user='root',passwd='qQ147258@',db='db_douban',charset='utf8')
        cursor = db.cursor()
        cursor.execute("select genre,count(*) from douban_app_genres group by genre having genre!=''")
        genres = cursor.fetchall()
        genres_data = [{'value':v,'name':k} for k,v in genres]
        genres_data_name = [i[0] for i in genres]
        genres_data_num = [i[1] for i in genres]
        genres_data_tmp = sorted(genres_data,key=lambda i:i['value'],reverse=True)
        genres_data_10 = genres_data_tmp[:5]
        genres_data_year = ['',]
        year = ['2023','2022','2021','2020','2019','2018','2017']
        for y in year:
            cursor.execute("select genre,count(*) from douban_app_genres where movie_id in (select movie_id from douban_app_movie where release_year=%s) group by genre having genre!=''",(y,))
            genres_year = cursor.fetchall()
            genres_data_year.append([{'value':v,'name':k} for k,v in genres_year])
        db.close()
        return render(request,"genres.html",{"genres_data":genres_data,"genres_data_10":genres_data_10,'genres_data_year':genres_data_year,'genres_data_name':genres_data_name,'genres_data_num':genres_data_num})
    else:
        return redirect("/")

@cache_page(60 * 15)
def avg_score(request):
    if request.user.is_authenticated:
        db = pymysql.connect(host='123.60.184.157',
                        user='root',passwd='qQ147258@',db='db_douban',charset='utf8')
        cursor = db.cursor()
        cursor.execute("select release_year,sum(score)/count(*) from douban_app_movie where release_year!='' and release_year!='0' and score!=0  group by release_year")
        data = cursor.fetchall()
        avg_score_data = sorted(data,key=lambda i:i[0])
        avg_score_year = [i[0] for i in avg_score_data]
        avg_score = [round(i[1],2) for i in avg_score_data]
        
        score_interval = []
        cursor.execute('select count(*) from douban_app_movie where score>0 and score<6')
        score_interval.append({'value':cursor.fetchall()[0][0],'name':'D:0~6'})
        cursor.execute('select count(*) from douban_app_movie where score>=6 and score<6.5')
        score_interval.append({'value':cursor.fetchall()[0][0],'name':'C:6~6.5'})
        cursor.execute('select count(*) from douban_app_movie where score>=6.5 and score<8.5')
        score_interval.append({'value':cursor.fetchall()[0][0],'name':'B:6.5~8.5'})
        cursor.execute('select count(*) from douban_app_movie where score>=8.5 and score<=10')
        score_interval.append({'value':cursor.fetchall()[0][0],'name':'A:8.5~10'})
        
        cursor.execute('select release_year,score from douban_app_movie where release_year!="" and score!=0 and release_year!="0"')
        allscore = [ [int(i[0]),i[1]] for i in cursor.fetchall() ]
        return render(request,"avg_score.html",{"avg_score_year":avg_score_year,"avg_score":avg_score,"score_interval":score_interval,"allscore":allscore})
    else:
        return redirect("/")

@cache_page(60 * 15)
def actor(request):
    if request.user.is_authenticated:
        # db = pymysql.connect(host='123.60.184.157',
        #                 user='root',passwd='qQ147258@',db='db_douban',charset='utf8')
        # cursor = db.cursor()
        # cursor.execute("select actors from douban_app_movie")
        # actors = cursor.fetchall()
        # db.close()
        # data = {}
        # for actor in actors:
        #     ls = actor[0].split('|')
        #     for i in ls:
        #         if data.get(i):
        #             data[i] += 1
        #         else:
        #             data[i] = 1
        # data.pop('')
        # actors_data = sorted(data.items(),key=lambda i:i[1],reverse=True)
        # actors_data_5 = actors_data[:10]
        actors_data_10 = [('曾志伟', 211), ('申星一', 188), ('任达华', 167), ('午马', 166), ('林雪', 163), ('尹静姬', 154), ('谷峰', 146), ('柯俊雄', 145), ('黄秋生', 141), ('张瑛', 136)]
        db = pymysql.connect(host='123.60.184.157',
                        user='root',passwd='qQ147258@',db='db_douban',charset='utf8')
        cursor = db.cursor()
        cursor.execute("select directors,count(*) from douban_app_movie group by directors having directors != ''")
        directors = cursor.fetchall()
        db.close()
        directors = list(directors)
        directors_sort = sorted(directors,key=lambda x:x[1],reverse=True)
        return render(request,"actor.html",{"actors_name":[i[0] for i in actors_data_10],"actors_num":[i[1] for i in actors_data_10],'directors_10_name':[i[0] for i in directors_sort[:10]],'directors_10_num':[i[1] for i in directors_sort[:10]]})
    else:
        return redirect("/")

@cache_page(60 * 15)
def film_total(request):
    if request.user.is_authenticated:
        res = Movie.objects.values("release_year").annotate(total=Count("release_year")).order_by("release_year").exclude(release_year="").exclude(release_year='0')
        year_data = [ i["release_year"] for i in res][:-11]
        year_total = [ i["total"] for i in res][:-11]
        # year = ['2023','2022','2021','2020','2019','2018','2017','2016','2015','2014']
        # year_data_10 = [ i["release_year"] for i in res if i["release_year"] in year]
        # year_total_10 = [ i["total"] for i in res if i["release_year"] in year]
        year_data_10 = year_data[-10:]
        year_total_10 = year_total[-10:]
        return render(request,"film_total.html",{"year_data":year_data,"year_total":year_total,"year_data_10":year_data_10,"year_total_10":year_total_10})
    else:
        return redirect("/")

def film_details(request,doubanId):
    film_details = Movie.objects.filter(movie_id=doubanId).first()
    film_details_json = {
        'doubanId':doubanId,
        'name': film_details.name,
        'year': film_details.release_year,
        'regions': film_details.regions,
        'genres': film_details.genres,
        'directors': film_details.directors,
        'actors': film_details.actors,
        'storyline': film_details.storyline,
        'score': film_details.score,
        'cover': film_details.cover,
        'languages': film_details.languages,
        'mins': film_details.mins,
    }
    return render(request,'film-details.html',film_details_json)

def film_collect(request,doubanId):
    user_id = request.session.get('_auth_user_id')
    if Collect.objects.filter(user_id=user_id).filter(movie_id=doubanId):
        Collect.objects.filter(user_id=user_id).filter(movie_id=doubanId).delete()
        return HttpResponse('取消收藏') 
    else:
        Collect.objects.create(user_id=user_id,movie_id=doubanId,is_collect=True)
        return HttpResponse('收藏成功')

def init_collect(request,doubanId):
    user_id = request.session.get('_auth_user_id')
    if Collect.objects.filter(user_id=user_id).filter(movie_id=doubanId):
        return HttpResponse('已收藏') 
    else:
        return HttpResponse('未收藏')

def mycollect(request):
    user_id = request.session.get('_auth_user_id')
    movie_ids = [i.movie_id for i in Collect.objects.filter(user_id=user_id).all()]
    movie_list = Movie.objects.filter(movie_id__in=movie_ids).all()
    return render(request,'collect.html',{'movielist':movie_list})
