# douban_web
这是一个对豆瓣电影数据进行分析的Django项目

# python环境是3.9.7


# 首先下载依赖包
```
pip install -r requirements.txt
```

# 修改数据库配置
在douban_web目录下的settings.py中的100行左右修改

# 更新数据库元数据
```
python manage.py makemigrations 
python manage.py migrate
```

# 运行项目(需要在项目目录下运行)
```
python manage.py runserver
```

# 创建管理员
```
python manage.py createsuperuser
```
