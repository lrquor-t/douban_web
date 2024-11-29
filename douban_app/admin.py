from django.contrib import admin

from douban_app.models import Movie,Person,Comments,Ratings,Genres


admin.site.site_header = '可视化系统管理后台'  # 设置header
admin.site.site_title = '可视化系统管理后台'   # 设置title
admin.site.index_title = '可视化系统管理后台'
# Register your models here.



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('movie_id','name','genres','release_year','mins','score','storyline')
    
    # 每页显示多少条记录
    list_per_page = 50
    
    # 按哪个字段排序
    ordering = ('movie_id',)
    
    # 设置默认可编辑字段
    list_editable = []
    
    # 设置哪些字段可进入编辑页面
    list_display_links = ()
    
    # 可以模糊搜索的字段
    search_fields = ('name','genres','release_year')
    
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('person_id','name','sex')
    
    # 每页显示多少条记录
    list_per_page = 50
    
    # 按哪个字段排序
    ordering = ('person_id',)
    
    # 设置默认可编辑字段
    list_editable = []
    
    # 设置哪些字段可进入编辑页面
    list_display_links = ()
    
    # 可以模糊搜索的字段
    search_fields = ('name',)
    
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('comment_id','movie_id','content')
    
    # 每页显示多少条记录
    list_per_page = 50
    
    # 按哪个字段排序
    ordering = ('comment_id',)
    
    # 设置默认可编辑字段
    list_editable = []
    
    # 设置哪些字段可进入编辑页面
    list_display_links = ()
    
    
    
@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('user_id','movie_id','rating')
    
    # 每页显示多少条记录
    list_per_page = 50
    
    # 按哪个字段排序
    ordering = ('user_id',)
    
    # 设置默认可编辑字段
    list_editable = []
    
    # 设置哪些字段可进入编辑页面
    list_display_links = ()
    
    # 可以模糊搜索的字段
    search_fields = ('user_id','movie_id')
    
@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('id','movie_id','movie_name','genre')
    
    # 每页显示多少条记录
    list_per_page = 50
    
    # 按哪个字段排序
    ordering = ()
    
    # 设置默认可编辑字段
    list_editable = []
    
    # 设置哪些字段可进入编辑页面
    list_display_links = ()
    
    # 可以模糊搜索的字段
    search_fields = ('movie_id','movie_name','genre')