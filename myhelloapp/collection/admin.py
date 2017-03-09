from django.contrib import admin
# Register your models here.
from collection.models import Thing, Social, Upload

#set up automated slug creation
class ThingAdmin(admin.ModelAdmin):
	model = Thing
	list_display = ('name', 'description',)
	prepopulated_fields = {'slug': ('name',)}

# and register it
admin.site.register(Thing, ThingAdmin)

class SocialAdmin(admin.ModelAdmin):
	model = Social
	list = ('network', 'username')
	
admin.site.register(Social, SocialAdmin)

class UploadAdmin(admin.ModelAdmin):
	list_display = ('thing', )
	list_display_links = ('thing',)
	
admin.site.register(Upload, UploadAdmin)