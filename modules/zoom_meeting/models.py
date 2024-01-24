import uuid
from django.db import models
from django.template.defaultfilters import slugify


class CrudConstraint(models.Model):
    """
    CrudConstraint model containing common fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class ZoomMeeting(CrudConstraint):
    """
    Model representing a ZoomMeeting.
    """
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    meeting_title = models.CharField(max_length=255, blank=True, null=True)
    meeting_description = models.TextField(max_length=600, blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    meeting_time = models.TimeField(blank=True, null=True)
    meeting_duration = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    zoom_meeting_link = models.CharField(max_length=150, blank=True, null=True)
    zoom_meeting_password = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    job = models.UUIDField(default=uuid.uuid4, blank=True, null=True)

    def _get_unique_slug(self):
        """
        Generates a unique slug for the ZoomMeeting.
        """
        slug = slugify(self.meeting_title[:40 - 2])
        unique_slug = slug
        num = 1
        while ZoomMeeting.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        """
        Overrides the save method to set the slug field.
        """
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the ZoomMeeting.
        """
        return self.meeting_title
