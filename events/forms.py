import logging

from django import forms
from django.utils.timezone import now

from date.functions import slugify_max
from events import models
from events.models import Event
from django.contrib.admin import widgets
import re
from datetime import datetime

logger = logging.getLogger('date')

slug_transtable = str.maketrans("åäö ","aao_")


class EventCreationForm(forms.ModelForm):
    user = None
    event_date_start = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    event_date_end = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    sign_up_others = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    sign_up_members = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    sign_up_deadline = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    sign_up_cancelling_deadline = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())

    class Meta:
        model = Event
        fields = (
            'title',
            'event_date_start',
            'event_date_end',
            'content',
            'sign_up',
            'sign_up_max_participants',
            'sign_up_others',
            'sign_up_members',
            'sign_up_deadline',
            'sign_up_cancelling',
            'sign_up_cancelling_deadline',
            'published',
            'slug'
        )

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery,
            'js/eventform.js',)

    def clean_slug(self):
        slug = self.cleaned_data['slug']

        if slug.strip() == "":
            base_slug = self.cleaned_data['title'].lower().translate(slug_transtable)
            base_slug = re.sub("[^a-zA-Z0-9_]*",'',base_slug)
            base_slug = re.sub("__+",'_',base_slug)
            slug = base_slug

            collisions = Event.objects.filter(slug = slug)
            suffix = 1
            while collisions:
                slug = base_slug+"_"+str(suffix)
                collisions = Event.objects.filter(slug = slug)
                suffix += 1
        #slugify_max actually does a trim down to the size of the underlying database column
        slug = slugify_max(slug, max_length=models.POST_SLUG_MAX_LENGTH)

        return slug

    def save(self, commit=True):
        post = super(EventCreationForm, self).save(commit=False)

        if self.user is None:
            return None
        post.author = self.user

        if post.published:
            post.published_time = now()

        if not post.sign_up:
            post.sign_up_max_participants = 0
            post.sign_up_others = None
            post.sign_up_members = None
            post.sign_up_deadline = None
            post.sign_up_cancelling = False
            post.sign_up_cancelling_deadline = None

        if commit:
            post.update_or_create(pk=post.pk)
        return post


class EventEditForm(forms.ModelForm):
    user = None
    event_date_start = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    event_date_end = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    sign_up_others = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    sign_up_members = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    sign_up_deadline = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    sign_up_cancelling = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())
    sign_up_cancelling_deadline = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime(), initial=datetime.now())

    class Meta:
        model = Event
        fields = (
            'title',
            'event_date_start',
            'event_date_end',
            'content',
            'sign_up',
            'sign_up_max_participants',
            'sign_up_others',
            'sign_up_members',
            'sign_up_deadline',
            'sign_up_cancelling',
            'sign_up_cancelling_deadline',
            'published',
            'slug'
        )

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery,
            'js/eventform.js',)

    def save(self, commit=True):
        post = super(EventEditForm, self).save(commit=False)
        if self.user is None:
            return None

        post.modified_time = now()

        if not post.sign_up:
            post.sign_up_max_participants = 0
            post.sign_up_others = None
            post.sign_up_members = None
            post.sign_up_deadline = None
            post.sign_up_cancelling = False
            post.sign_up_cancelling_deadline = None

        if commit:
            post.update_or_create(pk=post.pk)
        return post
