from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.views.static import serve

from collection.sitemap import ThingSitemap, StaticSitemap, HomepageSitemap
from collection.backends import MyRegistrationView
from collection import views

sitemaps = {
	'things': ThingSitemap,
	'static': StaticSitemap,
	'homepage': HomepageSitemap,
	}

urlpatterns = [

	#Common URLs
	url(r'^$', views.index, name='home'),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
	#url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^sitemap.xml/$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
	
	#Things URLs
	url(r'^things/$', RedirectView.as_view(pattern_name='browse')),
	url(r'^things/(?P<slug>[-\w]+)/$', views.thing_detail, name='thing_detail'),
	url(r'^things/(?P<slug>[-\w]+)/edit/$', views.edit_thing, name='edit_thing'),
	url(r'^things/(?P<slug>[-\w]+)/edit/images/$', views.edit_thing_uploads, name='edit_thing_uploads'),
	url(r'^delete/(?P<id>[-\w]+)/$', views.delete_upload, name='delete_upload'),
	
	#Browse URLs
	url(r'^browse/$', RedirectView.as_view(pattern_name='browse')),
	url(r'^browse/name/$', views.browse_by_name, name='browse'),
	url(r'^browse/name/(?P<initial>[-\w]+)/$', views.browse_by_name, name='browse_by_name'),
	
	#Login/Logout/Registration/Password URLs
	url(r'^accounts/password/reset/$', password_reset, {'template_name':
		'registration/password_reset_form.html'}, name="password_reset"),
	url(r'^accounts/password/reset/done/$', password_reset_done, {'template_name':
		'registration/password_reset_done.html'}, name="password_reset_done"),
	url(r'^accounts/password/reset/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
		password_reset_confirm, {'template_name':'registration/password_reset_confirm.html'},
		name="password_reset_confirm"),
	url(r'^accounts/password/done/$', password_reset_complete, {'template_name':
		'registration/password_reset_complete.html'}, name="password_reset_complete"),
	url(r'^accounts/register/$', MyRegistrationView.as_view(),
		name='registration_register'),
	url(r'^accounts/create_thing/$', views.create_thing,
		name='registration_create_thing'),
	url(r'^accounts/', include('registration.backends.default.urls')),
	
	#Admin URLs
	url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
	urlpatterns += [
		url(r'^media/(?P<path>.*)$', serve,{
			'document_root': settings.MEDIA_ROOT,
		}),
	]