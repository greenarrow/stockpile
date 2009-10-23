from django import forms
from django.forms import ModelForm
from stockpile.inventory.models import Category, Value, Field, Item
from stockpile.inventory.widgets import CustomCheckboxSelectMultiple, EditColumn
from django.forms.widgets import HiddenInput 



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
	class Meta:
		model = Item
	
	def __init__(self, instance=None, empty=False, data=None, *args, **kwargs):
		forms.Form.__init__(self, *args, **kwargs)
		
		#if type(instance) == django.http.QueryDict:
		#	print "have post"
		#else:
		
		#print data
		
		self.instance = instance
		#print "go"
		# Run though all the fields with their curren values
		if empty:
			for field in self.instance.category.fields.all():
		
				if field.field_type.name == 'choice':
					form_field = forms.ChoiceField( initial=0, choices=[ (0, '-') ] + [ (v.id, v.value) for v in Value.objects.filter(field=field) ] )
				elif field.field_type.name == 'text':
					form_field = forms.CharField(max_length=100, initial="")
				elif field.field_type.name == 'boolean':
					form_field = forms.BooleanField( required=False, initial=False )
		
				else:
					raise TypeError

				self.fields[field.name] = form_field
				#setattr(self, str(field.name), form_field)
		else:
			#self.fields = {}
			for field, value in self.instance.get_field_values():
				#print "loop", field, value
				# create the form field#
				#print Value.objects.filter(field=field)
				print "###", field, type(field), value, type(value)
				if field.field_type.name == 'choice':
					print [ (v.id, v.value) for v in Value.objects.filter(field=field) ]
					print value, type(value)
					if value == None:
						value_id = 0
					else:
						value_id = value.id
					form_field = forms.ChoiceField( initial=value_id, choices=[ (0, '-') ] + [ (v.id, v.value) for v in Value.objects.filter(field=field) ] )
				elif field.field_type.name == 'text':
					form_field = forms.CharField(max_length=100, initial=value)
				elif field.field_type.name == 'boolean':
					if value == None:
						checked = False
					else:
						checked = (value.value == "1")
					form_field = forms.BooleanField( required=False, initial=checked )
		
				else:
					raise TypeError
		
				#print "ff", form_field
				# add it to this object's dictionary so django finds it as normal
				
				#print '"' + str(field.id)  + "'"
				self.fields[field.name] = form_field
				#setattr(self, str(field.name), form_field)
		
	def save():
		pass
	
	


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


