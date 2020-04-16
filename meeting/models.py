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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Meeting(models.Model):
    title = models.CharField(max_length=200, default='None')
    location = models.CharField(max_length=200, default=0)
    optional_members = models.CharField(max_length=200, default='None')
    description = models.CharField(max_length=200, default='No description available')
    start_date = models.DateField(default = '1970-01-01')
    end_date = models.DateField(default = '1970-01-01')

    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)

    class VoteState(models.IntegerChoices):
        CLOSE = 0 # not ready to vote  
        OPEN = 1 # ready to vote
        DONE = 2 # vote is done and meeting time is available
        REVIEW = 3 # no meeting time option is generated and resubmit their availability
        REVOTE = 4 # equal votes and start vote again
        NO_VOTE = 5

    state = models.IntegerField(choices=VoteState.choices, default=1)
    
''' Time availability '''
class TimeAvailability(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return "[meeting_timeavailability] ID: " + str(self.id) + " | Meeting: " + str(self.meeting.id) + " | User: " + self.user.display_name + " | Start Time: " + str(self.start_time) + " | End Time: " + str(self.end_time)
    
class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=200, default="")
    link = models.CharField(max_length=200, default="")

class MeetingTimeOption(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)

    # user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    
class Vote(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    meeting_time_option = models.ForeignKey(MeetingTimeOption, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    

class MeetingTime(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    # user = models.ForeignKey(Profile, on_delete=models.CASCADE)
