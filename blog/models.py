from django.db import models
from accounts.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# Create your models here.



class Code(models.Model):
    name = models.CharField(max_length=300,null=True, blank=True, help_text="Tell what the code does")
    code = models.TextField()

    def __str__(self):
        return self.name


class SubContent(models.Model):
    sub_title = models.CharField(max_length=300, null=True, blank=True)
    sub_content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="content/images", null=True, blank=True)
    code = models.ManyToManyField(Code,blank=True, related_name="code_sub_content")

    def __str__(self):
        return self.sub_title


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='publish')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    content = models.ManyToManyField(SubContent, related_name="post_content")
    tutorial_link = models.CharField(max_length=1000, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30,
                              choices=STATUS_CHOICES,
                              default='draft')
    object = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])

    def send(self, request):
        subscribers = Subscriber.objects.filter(confirmed=True)
        for subscriber in subscribers:
            html_content = render_to_string('blog/email/fluid.html',
                                            {'title': self.title,
                                             'body': self.body,
                                             'get_absolute_url': request.build_absolute_uri(self.get_absolute_url()),
                                             'delete': request.build_absolute_uri(subscriber.get_absolute_url())})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                self.title,
                text_content,
                settings.EMAIL_HOST_USER,
                [subscriber]

            )
            email.attach_alternative(html_content, 'text/html')
            email.send()
            


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    website = models.CharField(blank=True, max_length=400)
    location = models.CharField(blank=True, max_length=500)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    publish = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "SUBJECT : " + self.subject


class Subscriber(models.Model):
    email = models.EmailField()
    conf_num = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + "(" + ("not " if not self.confirmed else "") + "confirmed)"

    def get_absolute_url(self):
        return reverse('blog:delete', args=[
            self.email,
            self.conf_num
        ])



class Recommendation(models.Model):

    name = models.CharField(max_length=100)

    company = models.CharField(max_length=350, blank=True)

    role = models.CharField(max_length=350, blank=True)

    message = models.TextField()

    publish = models.DateTimeField(default=timezone.now)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now = True)

    visible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


    class Meta :
        ordering = ['-publish',]

class UpdateWork(models.Model):
    
    name_project = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to="projects/images", null=True, blank=True )
    skills = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=1000, null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    description = models.TextField( null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_project 


class Skill(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class About(models.Model):
    
    description = models.TextField()
    skills = models.ManyToManyField(Skill, related_name="skills")
    youtube_link = models.CharField(max_length=500, null=True, blank=True)
    services = models.ManyToManyField(Service, related_name="services")
    date = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=False, help_text="Please make sure the previous about object is not visible before making this one visible.")

    def __str__(self):
        return str(self.visible)