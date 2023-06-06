from django.contrib import admin
from .models import Post


#嘗試自定義ADMIN 模組

class ArticleAdmin(admin.ModelAdmin):

    '''设置列表可显示的字段'''
    list_display = ('title', 'user', )

    # # '''设置过滤选项'''
    # list_filter = ('user', 'date_created', )

    '''每页显示条目数'''
    list_per_page = 10

    # '''设置可编辑字段'''
    # list_editable = ('status',)

    # '''按日期月份筛选'''
    # date_hierarchy = 'pub_date'

    # '''按发布日期排序'''
    # ordering = ('-mod_date',)

admin.site.register(Post, ArticleAdmin)

# Register your models here.
# admin.site.register(Post)
