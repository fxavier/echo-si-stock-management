from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.db.models.signals import pre_save, post_save

from core.utils import user_image_path


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.name
    
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    image = models.ImageField(upload_to=user_image_path, null=True, blank=True)
   
    def __str__(self):
        return self.user.email

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    # def save(self, *args,**kwargs):
    #     super(Profile, self).save(*args,**kwargs)
    #     img = Image.open(self.image)
    #     if img.height > 200 or img.width > 200 :
    #         new_size = (200,200)
    #         img.thumbnail(new_size)
    #         img.save(self.image.path)

def post_save_user_signal(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()
        
post_save.connect(post_save_user_signal, sender=User)
