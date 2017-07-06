import os
from django.db import models
from fortytwo_test_task.settings import STATIC_URL


class Person(models.Model):
    name = models.CharField('Name', max_length=50)
    lastname = models.CharField('Last name', max_length=50)
    dob = models.DateField('Date of birth', db_index=True)
    bio = models.TextField('Bio', null=1, blank=1)
    email = models.EmailField('Email')
    jabber = models.EmailField('Jabber ID')
    skype = models.CharField('Skype ID', max_length=50, null=1, blank=1)
    othercontacts = models.TextField('Other contacts', null=1, blank=1)
    photo = models.ImageField(
        upload_to="img",
        default=os.path.join(STATIC_URL, "img/avatar.png")
    )

    def __unicode__(self):
        return self.name + ' ' + self.lastname

    def __getitem__(self, item):
        return getattr(self, item)


class Request(models.Model):
    link = models.URLField()
    time = models.DateTimeField(auto_now_add=True)
    priority = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % self.link

    class Meta:
        ordering = ["priority", "time"]


class Change(models.Model):
    STATUS_CHOICES = (
        ('U', 'Updated'),
        ('C', 'Created'),
        ('D', 'Deleted'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    object = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["time"]
