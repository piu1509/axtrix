import uuid
from django.db import models
from django.template.defaultfilters import slugify


class CrudConstraint(models.Model):
	"""
	CrudConstraint model containing common fields.
	"""
	created_at = models.DateTimeField(
		auto_now_add=True)
	updated_at = models.DateTimeField(
		auto_now=True)
	deleted_at = models.DateTimeField(
		null=True, blank=True)

	class Meta:
		abstract = True


# Path for storing the image files of products and vehicles instances.
def gst_media_path(instance, filename):
    if instance.__class__.__name__ == "Products":
        return 'media/product/product_{}/images/{}'.format(
        	instance.pk, filename)
    elif instance.__class__.__name__ == "Vehicles":
        return 'media/vehicle/vehicle_{}/images/{}'.format(
        	instance.pk, filename)
    else:
        return 'media/images/{}'.format(filename)


class Category(CrudConstraint):
	"""
	Model representing Categories of a product.
	"""

	gid = models.UUIDField(
		max_length=32, unique=True, 
		default=uuid.uuid4, editable=False)
	slug = models.SlugField(
		max_length=200, db_index=True, unique=True)
	name = models.CharField(
		max_length=200, db_index=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def __str__(self):
		"""
		Returns a string represent of a category.
		"""
		return self.name

	def _get_unique_slug(self):
		"""
		Generates unique slug for every category.
		"""
		slug = slugify(self.name)
		unique_slug = slug
		num = 1
		while Category.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num = num + 1
		return unique_slug

	def save(self, *args, **kwargs):
		"""
		Overrides the save method to set the slug field.
		"""
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Category, self).save(*args, **kwargs)


class Products(CrudConstraint):	
	"""
	Model representing a products in an organization.
	"""

	gid = models.UUIDField(
		unique=True, 
		default=uuid.uuid4, editable=False)
	slug = models.SlugField(
		unique=True)
	employee = models.UUIDField(
		blank=True, null=True)
	product_name = models.CharField(
		max_length=200, blank=True, null=True)
	image = models.ImageField(
		upload_to=gst_media_path, blank=True)
	image_url = models.URLField(
		null=True, blank=True)
	description = models.TextField(
		blank=True)
	gst_price = models.DecimalField(
		max_digits=10, decimal_places=2, 
		blank=True, null=True)
	gst_percentage = models.DecimalField(
		max_digits=5, decimal_places=2, 
		blank=True, null=True)
	hsn_sac = models.CharField(
		max_length=200, db_index=True, 
		blank=True, null=True)
	category = models.UUIDField(
		blank=True, null=True)
	stock = models.PositiveIntegerField(
		blank=True, null=True)

	def _get_unique_slug(self):
		"""
		Generates a unique slug for the product.
		"""
		slug = slugify(self.product_name[:40 - 2])
		unique_slug = slug
		num = 1
		while Products.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		"""
		Overrides the save method to set the slug field.
		"""
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Products, self).save(*args, **kwargs)

	def __str__(self):
		"""
		Returns a string representation of the product.
		"""
		return f"{self.product_name}"

	def get_product_price(self):
		"""
		Returns the price of a product without gst.
		"""
		price = (self.gst_price*100)/(100+self.gst_percentage)
		return price


class Customers(CrudConstraint):
	"""
	Model representing a customer.
	"""

	gid = models.UUIDField(
		unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField(
		unique=True)
	customer_name = models.CharField(
		max_length=200, blank=True, null=True)
	address = models.CharField(
		max_length=200, blank=True, null=True)
	phone_number = models.CharField(
		max_length=14, blank=True, null=True)
	customer_gst = models.CharField(
		max_length=200, blank=True, null=True)

	def _get_unique_slug(self):
		"""
		Generates a unique slug for the customers.
		"""
		slug = slugify(self.customer_name[:40 - 2])
		unique_slug = slug
		num = 1
		while Customers.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		"""
		Overrides the save method to set the slug field.
		"""
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Customers, self).save(*args, **kwargs)

	def __str__(self):
		"""
		Returns a string representation of the Customers.
		"""
		return f"{self.customer_name}"


class Vehicles(CrudConstraint):
	"""
	Model representing a vehicle.
	"""

	gid = models.UUIDField(
		unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField(
		unique=True)
	vehicle_name = models.CharField(
		max_length=200, blank=True, null=True)
	vehicle_number = models.CharField(
		max_length=200, unique=True)
	owner = models.UUIDField(
		blank=True, null=True)
	driver = models.UUIDField(
		blank=True, null=True)
	image = models.ImageField(
		upload_to=gst_media_path, blank=True)
	image_url = models.URLField(
		null=True, blank=True)

	def _get_unique_slug(self):
		"""
		Generates a unique slug for the vehicles.
		"""
		slug = slugify(self.vehicle_name[:40 - 2])
		unique_slug = slug
		num = 1
		while Vehicles.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		"""
		Overrides the save method to set the slug field.
		"""
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Vehicles, self).save(*args, **kwargs)

	def __str__(self):
		"""
		Returns a string representation of the Vehicles.
		"""
		return f"{self.vehicle_name}"


class Invoices(CrudConstraint):
	"""
	Model representing a invoice.
	"""

	gid = models.UUIDField(
		unique=True, default=uuid.uuid4, editable=False)
	slug = models.SlugField(
		unique=True)
	invoice_name = models.CharField(
		max_length=200, blank=True, null=True)
	invoice_number = models.CharField(
		max_length=200, unique=True)
	customer = models.UUIDField(
		blank=True, null=True)
	product = models.UUIDField(
		blank=True, null=True)
	vehicle = models.UUIDField(
		blank=True, null=True)

	def _get_unique_slug(self):
		"""
		Generates a unique slug for the invoices.
		"""
		slug = slugify(self.invoice_number[:40 - 2])
		unique_slug = slug
		num = 1
		while Invoices.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		"""
		Overrides the save method to set the slug field.
		"""
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Invoices, self).save(*args, **kwargs)

	def __str__(self):
		"""
		Returns a string representation of the Invoices.
		"""
		return f"{self.invoice_number}"