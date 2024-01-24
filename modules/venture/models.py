import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class CrudConstrained(models.Model):
    """
    	Abstract model that provides CRUD constrains 
    	for model objects.
    """
    date_created = models.DateTimeField(
        _("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(
        _("Date updated"), auto_now=True)
    date_deleted = models.DateTimeField(
        _("Date deleted"), auto_now=True)

    class Meta:
        abstract = True


# Path for storing the image files of organisation instances.
def organisation_media_path(instance, filename):
    if instance.__class__.__name__ == "Organisation":
        return 'media/organisation/organisation_{}/images/{}'.format(
        	instance.pk, filename)
    else:
        return 'media/images/{}'.format(filename)


class Organisation(CrudConstrained):
	"""
		Organisation model description.
	"""
	gid = models.UUIDField(
		max_length=32, unique=True,
		default=uuid.uuid4, editable=False)
	slug = models.SlugField(
		max_length=100, unique=True)
	name = models.CharField(
		max_length=250, null=True, blank=True)
	image = models.ImageField(
		upload_to=organisation_media_path, null=True, blank=True)	
	website = models.CharField(
		max_length=250, unique=True)
	founder = models.UUIDField(
		max_length=32, default=uuid.uuid4, blank=True, null=True)
	founded_on = models.DateField(
		blank=True, null=True)
	address	= models.CharField(
		max_length=500, blank=True, null=True)
	contact_no = models.CharField(
		max_length=14, blank=True, null=True)
	headquarter = models.CharField(
		max_length=250, null=True, blank=True)
	organisation_type = models.CharField(
		max_length=50, blank=True, null=True)	
	area_served = models.CharField(
		max_length=50, blank=True, null=True)	
	description = models.TextField(
		blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Organisations'
		ordering = ('founded_on',)

	def _get_unique_slug(self):
		"""
			Generates unique slug for each organisation instance and 
			used by the save method.
		"""
		slug = slugify(self.name)
		unique_slug = slug
		num = 1
		while Organisation.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num = num + 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super(Organisation, self).save(*args, **kwargs)