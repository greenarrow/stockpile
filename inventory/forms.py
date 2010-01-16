from django import forms
import django.http
from django.forms import ModelForm
from stockpile.inventory.models import Category, Value, Field, Item
import stockpile.inventory.models as models
from stockpile.inventory.widgets import CustomCheckboxSelectMultiple, EditColumn
from django.forms.widgets import HiddenInput 
import datetime
import stockpile.inventory.fieldtypes as fieldtypes

class CategoryEditForm(forms.ModelForm):
	extra_column = EditColumn()
	
	#fields = forms.MultipleChoiceField( widget=forms.widgets.CheckboxSelectMultiple() )
	fields = forms.ModelChoiceField( Field.objects.all(), widget=CustomCheckboxSelectMultiple( table_id="category_fields", extra_columns=[extra_column] ) )
	#
	
	def set_category(self, category_id):
		self.extra_column.set_category(category_id)
	
	#CheckboxSelectMultiple
	
	
	
	class Meta:
		model = Category


class FieldForm(forms.ModelForm):
	
	return_page = forms.CharField( widget=HiddenInput(), initial="", required=False )
	
	#def __init__(self, return_page="/", *args, **kwargs):
	#	forms.ModelForm.__init__(self, *args, **kwargs)
	
	#	
	
	class Meta:
		model = Field



class DynamicModelForm(forms.Form):
	pass


# Dynamic model form replacement. TODO make this in sub class
class ItemForm(DynamicModelForm):
	
	def __init__(self, data=None, instance=None, *args, **kwargs):
		forms.Form.__init__(self, data, *args, **kwargs)
		
		self.instance = instance
		
		# we can't run this func on an instance that is not save, we need to bypass this for a new form and shove the data into the instance not out!
		null_values = bool(self.instance.id == None)
		
		for field, value in self.instance.get_field_values(null_values):
			if field.field_type == fieldtypes.CHOICE:
				if value == None:
					value_id = 0
				else:
					value_id = value.id
				form_field = forms.ChoiceField( initial=value_id, choices=[ (0, '-') ] + [ (v.id, v.value) for v in Value.objects.filter(field=field) ] )
				form_field.is_choice = True
				form_field.current_field = field
				
			elif field.field_type == fieldtypes.STRING:
				form_field = forms.CharField(max_length=100, initial=value)
				form_field.is_choice = False
			
			elif field.field_type == fieldtypes.BOOLEAN:
				if value == None:
					checked = False
				else:
					checked = (value.value == "1")
				form_field = forms.BooleanField( required=False, initial=checked )
				form_field.is_choice = False
			
			else:
				raise TypeError
			
			self.fields[field.name] = form_field
		
		
		if data != None:
			#print "do clean"
			self.full_clean()
		
	
	def save(self):
		
		#instance_in_database = bool(self.instance.id != None)
		# we are going to want to link many to manys so we have to save instance before we can do that
		
		if self.instance.id == None:
			# new item needs to have an id
			self.instance.created = datetime.datetime.now()
			self.instance.updated = datetime.datetime.now()
			self.instance.history = ""
			print "save"
			self.instance.save()
		

		
		for field, value_old in self.instance.get_field_values():
			
			print field.name, field.name in self.cleaned_data
			if field.name in self.cleaned_data:
				
				# move some of this into model so it just takes a 'take this data function'?
				
				# now we need to do different stuff for each field type
				if field.field_type == fieldtypes.CHOICE:
					form_value = int( self.cleaned_data[field.name] )
					print "fv", form_value
					if value_old != None and form_value == value_old.id:
						print "nothing changed"
					else:
						# handle error here
						
						self.instance.values.remove(value_old)
						
						# if we have a new one selected
						if form_value > 0:
							value_new = models.Value.objects.get(id=form_value)
							self.instance.values.add(value_new)
				
				elif field.field_type == fieldtypes.STRING:
					form_value = self.cleaned_data[field.name]
					if value_old != None:
						if form_value == value_old.value:
							print "nothings changed"
						else:
							value_old.value = form_value
							value_old.save()
					else:
						value = models.Value(field=field, value=form_value)
						value.save()
						self.instance.values.add(value)
				
				elif field.field_type == fieldtypes.BOOLEAN:
					form_value = ["1", "0"][ self.cleaned_data[field.name] == "on" ]
					if value_old != None:
						if form_value == value_old.value:
							print "nothings changed"
						else:
							value_old.value = form_value
							value_old.save()
					else:
						value = models.Value(field=field, value=form_value)
						value.save()
						self.instance.values.add(value)
				
				else:
					raise TypeError
				
		
		# do another update here and fill history		
		
		self.instance.updated = datetime.datetime.now()
		# TODO
		self.instance.history = ""
		print "save"
		self.instance.save()
		
		
		# todo either clean vals and put new ones on item or update existing ones
	


class AddChoiceForm(forms.ModelForm):
	field = forms.CharField( widget=HiddenInput() )
	
	class Meta:
		model = models.Value
		
	

"""class CategoryEditForm(forms.Form):
	
	name = 
	code = 
	
	def __init__(self, instance, *args, **kwargs):
		forms.Form.__init__(self, *args, **kwargs)
		
		self.instance = instance
		
		self.fields["fields"] = forms.MultipleChoiceField( widget=forms.widgets.CheckboxSelectMultiple(), initial=[ f.id for f in instance.fields.all() ], choices=[ (f.id, f.name) for f in Field.objects.all() ] )
		
"""
"""class ItemForm(ModelForm):
	class Meta:
		model = Item
"""


