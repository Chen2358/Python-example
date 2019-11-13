from django.contrib import admin
from sign.models import Event, Guest

# Register your models here.

class EventAdmin(admin.ModelAdmin):

	list_display = ['id', 'name', 'status', 'address', 'start_time']

	search_fields = ['name']			#搜索栏
	list_filter = ['status']			#过滤器


class GuestAdmin(admin.ModelAdmin):

	list_display = ['realname', 'phone', 'email', 'sign',  'create_time', 'event']

	search_fields =  ['realname', 'phone']
	list_filter = ['sign']


# #通知Admin管理工具提供界面
# admin.site.register(Event)
# admin.site.register(Guest)

#用EventAdmin、GuestAdmin选项注册Event、Guest
admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
