from django.db import models

import stockpile.inventory.fieldtypes as fieldtypes

"""
class FieldType(models.Model):
	name = models.CharField(max_length=10)

	def __unicode__(self):
		return self.name
"""

class Field(models.Model):
	name = models.CharField(max_length=30)
	field_type = models.IntegerField()
	
	class Meta:
		ordering = ('name',)
	
	def is_choice(self):
		print "IC", self.field_type == fieldtypes.CHOICE
		return self.field_type == fieldtypes.CHOICE
	
	def __unicode__(self):
		return self.name


class Value(models.Model):
	value = models.CharField(max_length=30)
	field = models.ForeignKey(Field)
	
	def __unicode__(self):
		return self.value


"""class Catalogue(models.Model):
	name = models.CharField(max_length=30)
	
	def __unicode__(self):
			return self.name
"""

class Category(models.Model):
	#catalogue= models.ForeignKey(Catalogue)
	name = models.CharField(max_length=30)
	code = models.CharField(max_length=10)
	fields = models.ManyToManyField(Field, blank=True)
	
	#primary_field= models.ForeignKey(Field)
	
	def get_fields(self):
		#print "gf", self.fields.all()
		return self.fields.all()
	
	def get_items(self):
		return Item.objects.filter(category=self)
	
	def num_items(self):
		return len( Item.objects.filter(category=self) )
	
	def __unicode__(self):
		return self.name
	
	def __cmp__(self, other):
		return cmp( self.num_items(), other.num_items() )
	class Meta:
		permissions = (
			("can_modify", "Can modify"),
		)



class Item(models.Model):
	category = models.ForeignKey(Category)
	values = models.ManyToManyField(Value, blank=True)
	created = models.DateTimeField()
	updated = models.DateTimeField()
	history = models.TextField(blank=True)
	
	def get_code(self):
		#print "ik"
		#print u'rc"%s%d"' % (self.category.code, self.id)
		return u'%s%s' % ( self.category.code, str(self.id).zfill(4) )
	
	def get_field_values(self, null_values=False):
		fields = self.category.fields.all()
		result = []
		
		for field in fields:
			
			if null_values:
				values = []
			else:
				values = self.values.filter(field=field)
			
			if len(values):
				value = self.values.filter(field=field)[0]
			else:
				value = None
			result.append( (field, value) )
		return result
	
	def __unicode__(self):
		return self.get_code()










