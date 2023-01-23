from django.contrib import admin
from .models import Post, Code, SubContent,Contact, Subscriber, UpdateWork, Recommendation, About, Service, Skill
from django.contrib import messages
#newsletter send method
def send_newsletter(modelAdmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)
        messages.success(request, "You have successfully sent newsletter to subscribers")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug' : ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('-status', '-publish')
    actions = [send_newsletter]

admin.site.register(SubContent)
admin.site.register(Code)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website' , 'location', 'subject', 'message')
    list_filter = ('subject', 'location', 'publish')
    date_hierarchy = 'publish'
    ordering = ('publish', 'location')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmed')


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'role', 'message', 'publish', 'created', 'updated']
    list_filter = ['publish', 'updated' ,'name', 'company' ,'role']
    ordering = ('publish',)

@admin.register(UpdateWork)
class UpdateworkAdmin(admin.ModelAdmin):
    list_display = ('name_project', 'url', 'duration','cost', 'description', 'date')
    search_fields = ('name_project', 'url', 'duration','cost', 'description', 'date')
    list_filter = ('name_project', 'url', 'duration','cost', 'description', 'date')


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('visible', 'description', 'date')
    list_filter = ('visible', 'date')
    search_fields = ('visible',)

admin.site.register(Skill)
admin.site.register(Service)
