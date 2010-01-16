from django.conf.urls.defaults import *

import stockpile.inventory.views
import stockpile.settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

stockpile_patterns = patterns('stockpile.inventory.views',
	(r'^category:(\d+)', 'category'),
	
	(r'^edit_category:(\d+)$', 'category_edit'),
	#(r'^edit_category:(new)$', 'category_edit'),
	
	
	(r'^delete_category:(\d+)', 'category_delete'),
	
	(r'^item:(\d+)$', 'item'),
	#(r'^item:0:(\d+)$', 'item'),
	
	(r'^delete_item:(\d+)$', 'item_delete'),
	
	#(r'^item:(?P<item_id>[0-9|new]+):?(?P<category_id>\d*)', 'item'),
	
	(r'^field:(\d+)$', 'field'),
	#(r'^field:(new)$', 'field'),
	
	(r'^sidebar', 'sidebar'),
	
	(r'^choice:new:(\d+)$', 'choice_new'),
	(r'^choice:(\d+)$', 'choice_edit'),
	
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
	( site_url_base, include(stockpile_patterns) ),
)

#print stockpile.settings.DEBUG
#if True:#stockpile.settings.DEBUG:
urlpatterns = stockpile_patterns


