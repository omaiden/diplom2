from django.db import models
import os
import datetime
from django.contrib.auth.models import User
from uuid import uuid4
from django.conf import settings
from django.utils.deconstruct import deconstructible



@deconstructible
class PathAndRename(object):
	def __init__(self, sub_path):
		self.path = sub_path

	def __call__(self, instance, filename):
		ext = filename.split('.')[-1]
		# set filename as random string
		filename = '{}.{}'.format(instance.id, ext)
		# return the whole path to the file
		return os.path.join(self.path, filename)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')
path_and_rename_missing = PathAndRename(os.path.join(BASE_DIR, 'images/missing'))
path_and_rename_victim = PathAndRename(os.path.join(BASE_DIR, 'images/victim'))


class Post_type(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name

    class Admin: pass


class Relative(models.Model):
    fullname = models.CharField(max_length=50)
    address = models.CharField(max_length=100, null=True)
    telephone = models.CharField(max_length=12)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.fullname

    class Admin: pass


    
class Post(models.Model):
    text = models.TextField()
    time = models.DateTimeField(default = datetime.datetime.now())
    found = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    post_type = models.ForeignKey(Post_type, on_delete=models.CASCADE, default=None)
    relative = models.ForeignKey(Relative, on_delete=models.CASCADE, default=None)
    # missing_person_id = models.ForeignKey(Missing_person, on_delete=models.CASCADE, default=None)
    # victim_id = models.ForeignKey(Victim, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text

    class Admin: pass



class Missing_person(models.Model):
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20, null=True)
    birthday = models.DateField()
    missing_place = models.CharField(max_length=100)
    missing_time = models.DateField()
    status = models.CharField(max_length=20)
    image = models.ImageField(upload_to=path_and_rename_missing, default = 'images/non.png')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name='missing')


    def __str__(self):
        return self.name

    class Admin: pass



class Victim(models.Model):
    date = models.DateField()
    place = models.CharField(max_length=100)
    image = models.ImageField(upload_to=path_and_rename_victim, default = 'images/non.png')
    additional_information = models.CharField(max_length=50, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name='victim')

    def __str__(self):
        return str(self.id)

    class Admin: pass



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Match(models.Model):
   missing_person = models.ForeignKey(Missing_person, on_delete=models.CASCADE, related_name="missing_person")
   victim = models.ForeignKey(Victim, on_delete=models.CASCADE, related_name="victim_person")
   exactly = models.BooleanField(default=False)

   class Admin: pass



    
