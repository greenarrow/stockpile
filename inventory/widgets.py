from django import forms
import django.utils.encoding
from itertools import chain
from django.forms.widgets import CheckboxInput
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

class EditColumn:
	#def __init__(self, 
	
	def set_category(self, category_id):
		self.category_id = category_id
	
	def render(self, field_id):
		if self.category_id == None:
			return_page = ""
		else:
			return_page = "?return=/edit_category:%s" % self.category_id
		
		return '<a href="/field:%s%s" field_id="%s" class="ui-state-default ui-corner-all button edit_field"><span class="ui-icon ui-icon-pencil"></span></a>' % (field_id, return_page, field_id)


class CustomCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
	
	category_id = None
	
	def __init__(self, table_id="", extra_columns=[], *args, **kwargs):
		#print "cu args", args, kwargs
		
		self.extra_columns = extra_columns
		self.table_id = table_id
		forms.widgets.CheckboxSelectMultiple.__init__(self, *args, **kwargs)
		
		#print dir(self)
		
	
	def render(self, name, value, attrs=None, choices=()):
		print name, value, self.attrs, choices
		if value is None: value = []
		has_id = attrs and 'id' in attrs
		final_attrs = self.build_attrs(attrs, name=name)
		print final_attrs
		output = [u'<table id="%s">' % self.table_id]
		# Normalize to strings
		str_values = set([django.utils.encoding.force_unicode(v) for v in value])
		for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
			#print option_value, option_label
			# If an ID attribute was given, add a numeric index as a suffix,
			# so that the checkboxes don't all have the same ID attribute.
			if has_id:
				final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
				label_for = u' for="%s"' % final_attrs['id']
				extra_columns_rendered = "".join( [ "<td>%s</td>" % column.render(option_value) for column in self.extra_columns ] )
			else:
				label_for = u''
				extra_columns_rendered = u''

			cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
			option_value = django.utils.encoding.force_unicode(option_value)
			rendered_cb = cb.render(name, option_value)
			option_label = conditional_escape(django.utils.encoding.force_unicode(option_label))
			
			# render the extra columns
			
			
			output.append(u'<tr><td><label%s>%s</label></td><td>%s</td>%s</tr>' % (label_for, option_label, rendered_cb, extra_columns_rendered))
		output.append(u'</table>')
		return mark_safe(u'\n'.join(output))



