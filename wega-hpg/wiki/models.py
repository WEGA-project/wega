

from django.db import models
from django.utils import timezone

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from django.contrib.auth.models import User

class Wiki(Page):
    # class meta:
    template = 'wiki/page.html'
    
    author = models.CharField(max_length=255)
    user  = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateField("Post date")
    main_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, blank=True,
    )
 
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('gallery', blocks.ListBlock(ImageChooserBlock())),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        
        FieldPanel('main_image'),
        FieldPanel('author'),
        FieldPanel('date'),
        FieldPanel('body'),
    ]

class WikiStatistic(models.Model):
    

    page = models.ForeignKey(Wiki, on_delete=models.CASCADE, related_name='statistics')  # внешний ключ на статью
    date = models.DateField('Дата', default=timezone.now)  # дата
    views = models.IntegerField('Просмотры', default=0)  # количество просмотров в эту дату

    def __str__(self):
        return self.page