from django.db import models


class Person(models.Model):
    name = models.CharField('Name', max_length=50)
    lastname = models.CharField('Last name', max_length=50)
    dob = models.DateField('Date of birth', db_index=True)
    bio = models.TextField('Bio', null=1, blank=1)
    email = models.EmailField('Email')
    jabber = models.EmailField('Jabber ID')
    skype = models.CharField('Skype ID', max_length=50, null=1, blank=1)
    othercontacts = models.TextField('Other contacts', null=1, blank=1)

    def __unicode__(self):
        return self.name + ' ' + self.lastname
