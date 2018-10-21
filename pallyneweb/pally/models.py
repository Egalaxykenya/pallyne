from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from pally.fields import OrderPallyneFields

# Pallyne Models
class PallyneUser(AbstractUser):
    is_paid = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)

# Subject model
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Subject, self).save(*args, **kwargs)

    class Meta:
        ordering =['title']

    def __str__(self):
        return self.title

# Publisher user profile
class Publisher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    publisher_name = models.CharField(max_length=100, blank=True, help_text="Enter a publisher's name")
    website = models.URLField(max_length=100, blank=True, help_text="Enter publisher's website")
    publisher_logo = models.ImageField(upload_to = 'images/logos/%Y/%m/%d/', default='images/logos/none/none.jpg')
    slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.publisher_name)
        super(Publisher, self).save(*args, **kwargs)


    def __str__(self):
        return self.publisher_name

class LearnerProfile(models.Model):
    COUNTRY=(
    ('Kenya', 'Kenya'),
    ('Japan', 'Japan'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    facebook_link = models.URLField(max_length=100, blank=True)
    twitter_link = models.URLField(max_length=100, blank=True)
    institution = models.CharField(max_length=100, blank=True, help_text="Enter your University, College or Company name")
    country_name = models.CharField(max_length=100, choices=COUNTRY)
    profile_photo = models.ImageField(upload_to='images/profilephotos/%Y/%m/%d/', default='images/profilephotos/none.jpg')

    def __str__(self):
        return self.user.username

# Course model
class Course(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='courses_created')
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
# Module model

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    order = OrderPallyneFields(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Module, self).save(*args, **kwargs)


    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

class Authors(models.Model):
    first_name = models.CharField(max_length=100, blank=False, help_text="Enter author first name")
    last_name = models.CharField(max_length=100, blank=False, help_text="Enter author's last name")

    class Meta:
        verbose_name_plural = 'Authors'


    def __str__(self):
        return u'%s %s' %(self.first_name, self.last_name)

class ReferenceBook(models.Model):
    book_imageicon = models.ImageField(upload_to = 'images/contentIcons/', default = 'images/contentIcons/None/book.jpg')
    book_title = models.CharField(max_length=100, blank=False, help_text="Enter a title for the book ")
    book_preview_link = models.URLField(max_length=200, blank=False, help_text = "Enter book's preview link")
    book_authors = models.ManyToManyField(Authors,  verbose_name="Book Authors")
    buy_booklink = models.URLField(max_length=200, blank=True, help_text="Enter URL for Purchasing Book")
    book_description = models.CharField(max_length=1000, blank=False, help_text="Enter a description of the book")
    slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.book_title)
        super(ReferenceBook, self).save(*args, **kwargs)


    def __str__(self):
        return self.book_title

# Abstract class model bearing repeated fields in other models
class PallyneContent(models.Model):
    content_id = models.AutoField(primary_key=True)
    content_title = models.CharField(max_length=100, blank=False, help_text='Enter content title')
    content_publisher = models.OneToOneField(Publisher, on_delete = models.CASCADE)

    published_date = models.DateTimeField(auto_now_add=True)
    content_description = models.CharField(max_length=1000, blank=False, help_text='Enter content Description')
    content_views = models.PositiveIntegerField(blank=True)
    content_likes = models.PositiveIntegerField(blank=True)
    content_imageicon = models.ImageField(upload_to = 'images/contentIcons/', default = 'images/contentIcons/None/none.jpg')


    class Meta:
        abstract = True
        ordering = ('-published_date',)

#inherits from pallyne content
class AssociatedDatasets(PallyneContent):
    dataset_download = models.FileField(upload_to = 'static/datasets/%Y/%m/%d/')
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = 'AssociatedDatasets'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.content_title)
        super(AssociatedDatasets, self).save(*args, **kwargs)

    def __str__(self):
        return self.content_title

class PallyneVideo(PallyneContent):
    video_url = models.URLField(max_length=100, blank=False, help_text = "Enter Video URL")
    applicable_industrial_area = models.CharField(max_length=200, blank = True, help_text = " Enter Applicable Industry")
    video_script = models.TextField(blank=True, help_text="Enter a script for the video ")
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE)
    reference_books = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, verbose_name="Video Reference Books", null=True)
    associated_datasets = models.ForeignKey(AssociatedDatasets, on_delete=models.CASCADE, verbose_name="Associated Datasets", null=True)
    video_length = models.CharField(max_length=50, blank=True, help_text="Enter approximate length of the video")
    VIDEO_INTESITY = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    )

    v_intensity = models.CharField(max_length=15, choices=VIDEO_INTESITY)
    slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.content_title)
        super(PallyneVideo, self).save(*args, **kwargs)

    def __str__(self):
        return self.content_title

"""
This Content models represents the module\'s content and defines a generic relation
to associate any type of content
"""
class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete = models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE, limit_choices_to={'model__in':('PallyneVideo', 'AssociatedDatasets', 'ReferenceBook')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderPallyneFields(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']
