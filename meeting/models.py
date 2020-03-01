from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

''' The user profile. Tied to a User account and created when a user is saved or created '''
class Profile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=30, blank=False)

''' Denotes a single project. '''
class Project(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

''' Denotes users related to a project. '''
class Member(models.Model):
    class UserProjectRole(models.IntegerChoices):
        INVITED = 0
        ACTIVE = 1
        OWNER = 2
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.IntegerField(choices=UserProjectRole.choices)

''' Denotes a single meeting. '''
class ProjectMeeting(models.Model): 
    date = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    optional_members = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    