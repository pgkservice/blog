import random

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Contact, Subscriber, UpdateWork, Recommendation, About
from taggit.models import Tag
from django.db.models import Count
from .forms import ContactForm, SubscriberForm
from django.contrib import messages
from django.core.mail import send_mail, mail_admins, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    template_name = 'blog/post/index.html'
    context = {
        'posts': posts,
        'tags': tag,
        'subscriberForm': SubscriberForm()
    }
    return render(request, template_name, context)


def detail_post(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='publish',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    template_name = 'blog/post/single.html'
    context = {
        'post': post,
        'similar_posts': similar_posts,
        'subscriberForm' : SubscriberForm()
    }
    return render(request, template_name, context)


def about(request):

    obj = About.objects.filter(visible=True)
    context = {'subscriberForm': SubscriberForm(),
                'user': request.user,
                'about':obj}
    template_name = 'blog/about/about.html'
    return render(request, template_name, context)


def work(request):
    object_list = UpdateWork.objects.all()
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try :
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    context = {'subscriberForm': SubscriberForm(), 'projects': projects}
    template_name = 'blog/work/work.html'
    return render(request, template_name, context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            users_admin = User.objects.filter(is_superuser=True, is_active=True, is_staff=True)
            for user in users_admin :
                send_mail(
                f"{form.cleaned_data['subject']}",
                'Hi. My name is '+form.cleaned_data['name']+\
                ' and my email is '+form.cleaned_data['email']+'. '+form.cleaned_data['message']+\
                '.\n The rest of the details you will find them in your admin site.'+\
                " \nI AM NAKED AS A TEMPLATES I NEED BEAUTY CLOTHES !! BEFORE PUBLISH PLEASE COVER WITH ME ",
                "",
                [user.email],
                fail_silently=False,)
            form.save()
            messages.success(request, "Your contact has been successfully received.")
        else:
            messages.error(request, "Your contact has been unsuccessfully received")
        return redirect('blog:contact')
    obj = Recommendation.objects.filter(visible=True)
    form = ContactForm()
    template_name = 'blog/contact/contact.html'
    context = {'form': form,
               'subscriberForm':SubscriberForm(),
               'recommendations' : obj,
               'user': request.user}
    return render(request, template_name, context)


def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)


# This is a newsletter view that sends mail to be confirmed
def new(request):
    if request.method == 'POST':

        data = Subscriber(email=request.POST['email'], conf_num=random_digits())
        html_content = render_to_string(
            'blog/email/confirm.html',
            {'confirm': request.build_absolute_uri('confirm'),
             'email': data.email,
             'conf_num': data.conf_num}
        )
        text_content = strip_tags(html_content)
        email  = EmailMultiAlternatives(
            'Newsletter email confirmation',
            text_content,
            "",
            [data.email]
        )
        email.attach_alternative(html_content, 'text/html')
        email.send()
        data.save()
        messages.success(request, "Congratulations on your first step." + \
                 "Your email " + data.email + " has been added." + \
                 "Please go to your email box and confirm your email address so that" + \
                 " so that you will receive the newsletters"
                 )

        return render(request, 'blog/post/confirmationMessage.html')
    else:
        render(request, 'blog/post/index.html', {'subscriberForm': SubscriberForm()})

from django.core.exceptions import MultipleObjectsReturned

    
def confirm(request):
    try :
        sub = Subscriber.objects.get(email=request.GET['email'], conf_num=request.GET['conf_num'])
        if sub.confirmed:
            return render(request, 'blog/errors/404.html')
        else:
            sub.confirmed = True
            messages.success(request, "Congratulations!!! You have confirmed your email. Check your email box.")

            # We must send an email to a user confirming subscription, welcome him for the nice ride
            html_content = render_to_string('blog/email/welcome.html',
                                            {'link' : request.build_absolute_uri('blog:post_list')})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                f"Welcoming message",
                "",
                "",
                [sub.email,],
            )
            email.attach_alternative(html_content, 'text/html')
            email.send()
            sub.save()
            return render(request, "blog/post/confirmationMessage.html")
    except Subscriber.DoesNotExist :
        return render(request, 'blog/errors/404.html')
    except MultipleObjectsReturned :
        return render(request, 'blog/errors/404.html')


def delete(request, email, conf_num):

    try :
        obj = get_object_or_404(Subscriber,
                                email=email,
                                conf_num=conf_num,
                                confirmed=True)
        if obj :
            obj.delete()
            messages.success(request, "You have successfully unsubscribed to our email newsletters.")
            return render(request, 'blog/post/confirmationMessage.html')
    except Subscriber.DoesNotExist :      
        return render(request, 'blog/errors/404.html')