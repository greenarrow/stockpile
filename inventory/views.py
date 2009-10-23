import django.http
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

# need to find out about this
from django.template import RequestContext 

from stockpile.inventory.models import Category, Value, Field, Item
import stockpile.inventory.forms as forms


def index(request):
	#catalogue = Catalogue.objects.all()[0]
	categories = Category.objects.all()
	
	newest_items = Item.objects.filter().order_by('-id')[ :5 ]
	
	cats_lens = []
	for cat in categories:
		cats_lens.append( ( len( cat.get_items() ), cat ) )
	
	cats_lens.sort()
	cats_lens.reverse()
	
	sidebar = Sidebar()
	
	return render_to_response( 'inventory/index.html', {'categories':cats_lens, 'newest_items':newest_items, 'category_admin':True, 'sidebar':sidebar}, context_instance=RequestContext(request) )

#TODO new category with option to duplicate


def category(request, category_id):
	cat = Category.objects.get(id=category_id)
	items = Item.objects.filter(category=cat)
	rows = []
	
	sidebar = Sidebar()
	
	return render_to_response( 'inventory/category.html', {'category':cat, 'items':items, 'item_edit':True, 'sidebar':sidebar}, context_instance=RequestContext(request) )


def category_edit(request, category_id):
	if request.method == "POST":
		if category_id == '0':
			cat = Category()
		else:
			cat = Category.objects.get(id=category_id)
		
		
		"""
		form = forms.FieldForm(request.POST, instance=field)
		
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect( form.cleaned_data["return_page"] )
		
		else:
			return HttpResponse("ERRORS:" + form.errors)
		
		"""

		
	else:
		
		if category_id == '0':
			cat = Category()
		else:
			cat = Category.objects.get(id=category_id)
		
		
		form = forms.CategoryEditForm(instance=cat)
		form.set_category(cat.id)
		ajax = ("ajax" in request.GET and request.GET["ajax"] == "1")
	
	return render_to_response( 'inventory/category_edit.html', {'category':cat, 'form':form, 'ajax':ajax}, context_instance=RequestContext(request) )


def category_delete(request, category_id):
	
	cat = Category.objects.get(id=category_id)
	
	return render_to_response( 'inventory/category_delete.html', {'category':cat}, context_instance=RequestContext(request) )


def item(request, item_id, category_id=None):
	
	if request.method == "POST":
		if item_id == '0':
			
			cat = Category.objects.get(id=category_id)
			item = Item(category=cat)
		else:
			item = Item.objects.get(id=item_id)
		#
		#
		#
		
		form = forms.ItemForm(instance=item, data=request.POST, empty=True)
		print form.is_valid()
		
	else:
		print "oo", item_id
		if item_id == '0':
			cat = Category.objects.get(id=category_id)
			item = Item(category=cat)
			form = forms.ItemForm(instance=item, empty=True)
		else:
			item = Item.objects.get(id=item_id)
			print "## item:", item
			form = forms.ItemForm(instance=item)
		
		
		sidebar = Sidebar()
		ajax = ("ajax" in request.GET and request.GET["ajax"] == "1")
		#print form
		return render_to_response( 'inventory/item.html', {'item':item, 'form':form, 'reply':'/item:%s' % item.id, 'ajax':ajax, 'sidebar':sidebar}, context_instance=RequestContext(request) )



def field(request, field_id):
	
	if request.method == "POST":
		if field_id == '0':
			field = Field()
			print "new"
		else:
			field = Field.objects.get(id=field_id)
		
		"""
		print field_id, field
		print request.POST
		
		if "return_page" in processed_post:
			return_page = processed_post["return_page"]
			del processed_post["return_page"]
		
		print processed_post
		"""
		form = forms.FieldForm(request.POST, instance=field)
		#print , form.errors
		#print form.cleaned_data
		#for field in form:
		#	print field
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect( form.cleaned_data["return_page"] )
		
		else:
			return HttpResponse("ERRORS:" + form.errors)
		# what do ajax?
		#return HttpResponseRedirect("/")
		
	else:
		
		if field_id == '0':
			field = Field()
		else:
			field = Field.objects.get(id=field_id)
		
		ajax = ("ajax" in request.GET and request.GET["ajax"] == "1")
		
		form = forms.FieldForm(instance=field)
		
		# If we have a return page set this to hidden form item
		if "return" in request.GET:
			form.fields["return_page"].initial = request.GET["return"]
		
		
		
		return render_to_response( 'inventory/field.html', {'field':field, 'form':form, 'ajax':ajax}, context_instance=RequestContext(request) )

"""
def sidebar(request):
	categories = list( Category.objects.all() )
	
	categories.sort()
	categories.reverse()
	
	newest_items = Item.objects.filter().order_by('-id')[ :5 ]
	
	return render_to_response( 'inventory/ajax_sidebar.html', {'categories':categories, 'newest_items':newest_items}, context_instance=RequestContext(request) )
"""


class Sidebar:
	
	def __init__(self):
		self.categories = list( Category.objects.all() )
		
		self.categories.sort()
		self.categories.reverse()
		
		self.newest_items = Item.objects.filter().order_by('-id')[ :5 ]
		
		#	self.items = [ ("Categories", categories), ("Newest Items", newest_items), ("Other Stuff", "todo - just pass one list to all views returns containing all sidebar module objects to render") ]
	

# I don't know why the hell DJango wants to call an object in this module called sidebar, but we will let it
def sidebar():
	return None




