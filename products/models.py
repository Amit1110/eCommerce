from django.db import models
import random
import os
# Create your models here.

def get_file_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name,ext

def upload_image_path(instance, filename):
	print(instance)
	print(filename)
	new_filename = random.randint(1,200000000000)
	name,ext = get_file_ext(filename)
	final_name = '{new_filename}{ext}'.format(new_filename = new_filename,ext=ext)
	return "products/{new_filename}/{final_name}".format(new_filename = new_filename,final_name=final_name)


class ProductManger(models.Manager):

	def feature(self):
		return self.get_queryset().filter(featured=True)
	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None
		


class Product(models.Model):
	title = models.CharField(max_length = 120)
	slug = models.SlugField(blank=True,unique = True)
	description = models.TextField()
	price = models.DecimalField(decimal_places = 2,max_digits = 20,default = 39.99)
	image = models.ImageField(upload_to=upload_image_path,null=True,blank =True)#slash upront causes issues
	featured = models.BooleanField(default=False)


	objects = ProductManger()

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title
		