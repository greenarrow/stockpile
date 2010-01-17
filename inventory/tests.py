import unittest, datetime
import stockpile.inventory.models as models
import stockpile.inventory.forms as forms
import django.http

import stockpile.inventory.fieldtypes as fieldtypes

class ItemForm(unittest.TestCase):
	def setUp(self):
		
		#fts = models.FieldType(name="text")
		#fts.save()
		
		field1 = models.Field(name="test field 1", field_type=fieldtypes.STRING)
		field2 = models.Field(name="test choice 1", field_type=fieldtypes.CHOICE)
		field3 = models.Field(name="test bool 1", field_type=fieldtypes.BOOLEAN)
		
		field1.save()
		field2.save()
		field3.save()
		
		self.cat = models.Category(name="test cat 1", code="CT")
		self.cat.save()
		self.cat.fields.add(field1)
		self.cat.fields.add(field2)
		self.cat.fields.add(field3)
	
	def testItemData(self):
		
		i = models.Item(category=self.cat, created=datetime.datetime.now(), updated=datetime.datetime.now(), history="")
		i.save()
		
		field = self.cat.fields.get(id=1)
		
		val = models.Value(value="this is a test value", field=field)
		val.save()
		
		i.values.add(val)
		
		f = forms.ItemForm(instance=i)
		
		self.assertTrue( f.as_table().find('<tr><th><label for="id_test field 1">Test field 1:</label></th><td><input id="id_test field 1" type="text" name="test field 1" value="this is a test value" maxlength="100" /></td></tr>') >= 0 )
		self.assertTrue( f.as_table().find('<tr><th><label for="id_test bool 1">Test bool 1:</label></th><td><input type="checkbox" name="test bool 1" id="id_test bool 1" /></td></tr>') >= 0 )
		self.assertTrue( f.as_table().find('<tr><th><label for="id_test choice 1">Test choice 1:</label></th><td><select name="test choice 1" id="id_test choice 1">\n<option value="0" selected="selected">-</option>\n</select></td></tr>') >= 0 )
	
	def testItemPost(self):
		qd = django.http.QueryDict("")
		post = qd.copy()
		
		post.update( {u'test field 1': u'value is good', u'test choice 1':u'1', u'test bool 1':u'0'} )
		
		i = models.Item(category=self.cat)
		f = forms.ItemForm(post, instance=i)
		
		self.assertTrue(f.is_bound)
		
		self.assertTrue( f.is_valid() )
		print f.errors
		self.assertEquals(f.cleaned_data['test field 1'], u'value is good')
		
		f.save()
		
		self.assertNotEquals(i.id, None)
		
		for field, value in i.get_field_values():
			self.assertEquals(field.name, 'test field 1')
			self.assertEquals(value.value, u'value is good')

		# todo tests for other value types 



