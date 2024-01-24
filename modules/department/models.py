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


class Department(CrudConstraint):
    """
    Model representing a department in an organization.
    """
    department_choices = (
        ('hr', 'Hr'),
        ('backoffice', 'Backoffice'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('business_development', 'Business_Development'),
        ('admin', 'Admin')
    )
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    department_name = models.CharField(
        max_length=250, choices=department_choices, default='hr')
    employee = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    organization = models.UUIDField(default=uuid.uuid4, blank=True, null=True)

    def _get_unique_slug(self):
        """
        Generates a unique slug for the department.
        """
        slug = slugify(self.department_name[:40 - 2])
        unique_slug = slug
        num = 1
        while Department.objects.filter(slug=unique_slug).exists():
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
        Returns a string representation of the department.
        """
        return f"{self.employee} ({self.department_name})"


class Job(CrudConstraint):
    """
    Model representing a Job in an organization.
    """
    gid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    organization = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    job_poster = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    experience = models.CharField(max_length=255, blank=True, null=True)
    salary = models.CharField(max_length=255, blank=True, null=True)
    skills_required = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=400, blank=True, null=True)
    vacancies = models.IntegerField(blank=True, null=True)
    qualifications = models.CharField(max_length=255, blank=True, null=True)

    def _get_unique_slug(self):
        """
        Generates a unique slug for the Job model.
        """
        slug = slugify(self.title[:40 - 2])
        unique_slug = slug
        num = 1
        while Job.objects.filter(slug=unique_slug).exists():
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
        Returns a string representation of the Job model.
        """
        return self.title


class AppliedJob(CrudConstraint):
    """
        Model description for applied jobs.
    """
    gid = models.UUIDField(
        max_length=32, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        max_length=100, unique=True)
    job = models.UUIDField(
        max_length=32, default=uuid.uuid4, blank=True, null=True)
    user = models.UUIDField(
        max_length=32, default=uuid.uuid4, blank=True, null=True)
    user_profile = models.UUIDField(
        max_length=32, default=uuid.uuid4, blank=True, null=True)
    shortlisted = models.BooleanField(default=False)
    interview_status = models.CharField(
        max_length=30, blank=True, null=True)
    result = models.BooleanField(default=False)
    
    def __str__(self):
        """
            Represents the AppliedJob model by a string.
        """
        return '{}-{}'.format(self.user, self.job)
        
    class Meta:
        verbose_name_plural = 'AppliedJobs'
        ordering = ('created_at',)

    def _get_unique_slug(self):
        """
            Generates an unique slug for each AppliedJob instance.
        """
        slug = slugify(self.job)
        unique_slug = slug
        num = 1
        while AppliedJob.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self,*args,**kwargs):
        """
            Sets the slug field for each applied job and saves the instance.
        """
        if not self.slug:
            self.slug=self._get_unique_slug()
        super(AppliedJob,self).save(*args,**kwargs)
    
