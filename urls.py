from django.conf.urls.defaults import *

import stockpile.inventory.views
import stockpile.settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

generic_patterns = patterns( '', (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}), )

stockpile_patterns = patterns('stockpile.inventory.views',
	(r'^category:(\d+)/view', 'category_view'),
	(r'^category:(\d+)/edit$', 'category_edit'),
	(r'^category:(\d+)/delete', 'category_delete'),
	
	(r'^item:(\d+)/edit$', 'item_edit'),
	(r'^item/new:(\d+)$', 'item_new'),
	(r'^item:(\d+)/delete$', 'item_delete'),
	
	
	(r'^field:(\d+)$', 'field'),
	
	(r'^choice/new:(\d+)$', 'choice_new'),
	(r'^choice:(\d+)/edit$', 'choice_edit'),
	
	(r'^logout/$', 'user_logout'),
	
	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	( r'^admin/doc/', include('django.contrib.admindocs.urls') ),
	
	# Uncomment the next line to enable the admin:
	(r'^admin/(.*)', admin.site.root),

	(r'^$', 'index'),
)

if True:#if stockpile.settings.DEBUG:
	stockpile_patterns += patterns('', ( r'^stockpile_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/stef/projects/stockpile/stockpile/site_media', 'show_indexes': True} ) )
	site_url_base = r''
else:
	site_url_base = r'/stockpile/'

urlpatterns = patterns('',
	( site_url_base, include(stockpile_patterns + generic_patterns) ),
)

#print stockpile.settings.DEBUG
#if True:#stockpile.settings.DEBUG:
urlpatterns = stockpile_patterns + generic_patterns


