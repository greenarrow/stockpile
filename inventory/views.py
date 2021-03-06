from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test


# need to find out about this
from django.template import RequestContext 
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

import stockpile.inventory.models as models
import stockpile.inventory.forms as forms


# Get parameters used for all views (data used in base.html e.g. sidebar)
def get_base_params(request):
	# see if we have an request for basic html content (for ajax) or the full page
	ajax = ("ajax" in request.GET and request.GET["ajax"] == "1")
	
	# fetch data for sidebar
	categories = list( models.Category.objects.all() )
	categories.sort()
	categories.reverse()
	newest_items = models.Item.objects.filter().order_by('-id')[ :5 ]
	
	# If sidebar position is not set then default to visible
	if not 'sidebar_visible' in request.session.keys():
		request.session['sidebar_visible'] = True
	
	sidebar_visible = request.session.get('sidebar_visible', False)
	
	return { 'ajax':ajax, 'sidebar_visible':sidebar_visible, 'sidebar':{'newest_items':newest_items, 'categories':categories} }



@login_required
def index(request):
	#print request.user.get_all_permissions()
	
	categories = models.Category.objects.all()
	
	newest_items = models.Item.objects.filter().order_by('-id')[ :5 ]
	
	cats_lens = []
	for cat in categories:
		cats_lens.append( ( len( cat.get_items() ), cat ) )
	
	cats_lens.sort()
	cats_lens.reverse()
	
	params = get_base_params(request)
	params.update( {'categories':cats_lens, 'newest_items':newest_items, 'category_admin':True} )
	
	return render_to_response( 'inventory/index.html', params, context_instance=RequestContext(request) )

@login_required
def category_view(request, category_id):
	cat = models.Category.objects.get(id=category_id)
	items = models.Item.objects.filter(category=cat)
	rows = []
	
	params = get_base_params(request)
	params.update( {'category':cat, 'items':items} )
	# TODO table vales should be smart depending on fieldtype (e.g. bool should not just show 1/0) should value have a function to format nicely?
	return render_to_response( 'inventory/category.html', params, context_instance=RequestContext(request) )


#TODO new category with option to duplicate
@login_required
@user_passes_test( lambda u: u.has_perm('inventory.change_category') )
def category_edit(request, category_id):
	if request.method == "POST":
		if category_id == '0':
			cat = models.Category()
		else:
			cat = models.Category.objects.get(id=category_id)
		
		
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
			cat = models.Category()
		else:
			cat = models.Category.objects.get(id=category_id)
		
		
		form = forms.CategoryEditForm(instance=cat)
		form.set_category(cat.id)
		
		params = get_base_params(request)
		params.update( {'category':cat, 'form':form} )
	
	return render_to_response( 'inventory/category_edit.html', params, context_instance=RequestContext(request) )


@login_required
@user_passes_test( lambda u: u.has_perm('inventory.delete_category') )
def category_delete(request, category_id):
	
	cat = models.Category.objects.get(id=category_id)
	
	params = get_base_params(request)
	params.update( {'category':cat} )
	# TODO
	return render_to_response( 'inventory/category_delete.html', params, context_instance=RequestContext(request) )




@login_required
@user_passes_test( lambda u: u.has_perm('inventory.add_item') )
def item_new(request, category_id):
	return item_edit(request, item_id='new', category_id=category_id)


@login_required
@user_passes_test( lambda u: u.has_perm('inventory.change_item') )
def item_edit(request, item_id, category_id=None):
	#print request.user.get_all_permissions()
	#print request.user.has_perm('inventory.change_item')
	new_item = (item_id == 'new')
	
	if request.method == "POST":
		if new_item:
			cat = models.Category.objects.get(id=category_id)
			item = models.Item(category=cat)
		else:
			item = models.Item.objects.get(id=item_id)
			cat = item.category
		
		form = forms.ItemForm(request.POST, instance=item)
		
		if form.is_valid():
			form.save()
			# TODO need to review this once ajax submit complete
			return HttpResponseRedirect( reverse( 'stockpile.inventory.views.category_view', args=[cat.id] ) )
		else:
			# TODO display for with errors
			return HttpResponse(form.errors)
		
	else:
		if new_item:
			cat = models.Category.objects.get(id=category_id)
			item = models.Item(category=cat)
			form = forms.ItemForm(instance=item)
		else:
			item = models.Item.objects.get(id=item_id)
			cat = item.category
			form = forms.ItemForm(instance=item)
		
		params = get_base_params(request)
		params.update( {'item':item, 'category':cat, 'form':form, 'new_item':new_item} )
		return render_to_response( 'inventory/item.html', params, context_instance=RequestContext(request) )


@login_required
@user_passes_test( lambda u: u.has_perm('inventory.delete_item') )
def item_delete(request, item_id):
	params = get_base_params(request)
	params.update( {'item':item, 'form':form} )
	return render_to_response( 'inventory/item_delete.html', params, context_instance=RequestContext(request) )


@login_required
def choice(request, value):
	if request.method == "POST":
		pass
	else:
		form = forms.AddChoiceForm(instance=value)
	
		params = get_base_params(request)
		params.update( {'value':value, 'form':form} )
		return render_to_response( 'inventory/choice.html', params, context_instance=RequestContext(request) )


@login_required
@user_passes_test( lambda u: u.has_perm('inventory.add_choice') )
def choice_new(request, field_id):
	field = models.Field.objects.get(id=field_id)
	value = models.Value(field=field)
	
	return choice(request, value)


@login_required
@user_passes_test( lambda u: u.has_perm('inventory.change_choice') )
def choice_edit(request, item_id):
	value = models.Value.objects.get(item_id)
	return choice(request, value)


@login_required
@user_passes_test( lambda u: u.has_perm('inventory.change_field') )
def field(request, field_id):
	
	if request.method == "POST":
		if field_id == '0':
			field = models.Field()
		else:
			field = models.Field.objects.get(id=field_id)
		
		form = forms.FieldForm(request.POST, instance=field)

		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect( form.cleaned_data["return_page"] )
		
		else:
			return HttpResponse("ERRORS:" + form.errors)
		
	else:
		
		if field_id == '0':
			field = models.Field()
		else:
			field = models.Field.objects.get(id=field_id)
		
		form = forms.FieldForm(instance=field)
		
		# If we have a return page set this to hidden form item
		if "return" in request.GET:
			form.fields["return_page"].initial = request.GET["return"]
		
		params = get_base_params(request)
		params.update( {'field':field, 'form':form} )
		
		return render_to_response( 'inventory/field.html', params, context_instance=RequestContext(request) )



def toggle_sidebar(request):
	request.session['sidebar_visible'] = not request.session.get('sidebar_visible', False)
	#print request.session.get('sidebar_visible', False)
	return HttpResponse("ok")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect( reverse( 'stockpile.inventory.views.index') )
	
