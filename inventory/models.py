from django.db import models

class FieldType(models.Model):
	name = models.CharField(max_length=10)

	def __unicode__(self):
		return self.name

class Field(models.Model):
	name = models.CharField(max_length=30)
	field_type = models.ForeignKey(FieldType)
	
	class Meta:
		ordering = ('name',)
	
	def is_choice(self):
		print self.field_type.name == 'choice'
		return self.field_type.name == 'choice'
	
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
	
	def get_field_values(self):
		fields = self.category.fields.all()
		result = []
		print "===ff", fields
		for field in fields:
			print "====field", field
			values = self.values.filter(field=field)
			print "===vals", values
			if len(values):
				value = self.values.filter(field=field)[0]
			else:
				value = None	
			result.append( (field, value) )
		return result
	
	def __unicode__(self):
		return self.get_code()










