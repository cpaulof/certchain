import hashlib
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True,  null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

class Block(models.Model):
    _saved = False
    previous_block = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    previous_hash = models.CharField(max_length=512, null=True)
    block_type = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    data = models.TextField()

    def get_previous_hash(self):
        prev = ''
        if hasattr(self, 'previous_block'):
            if self.previous_block:
                prev = self.previous_block.block_hash
        return prev

    def _hash(self):
        prev = self.previous_hash    
        content = (prev + str(self.block_type) + self.date.ctime() + self.user.username + self.data).encode('utf-8')
        return hashlib.sha256(content).hexdigest()
    
    def get_block_hash(self):
        return self._hash()
    
    @staticmethod
    def verify():
        #implementar ainda
        block = Block.objects.last()

        current_block = block
        previous_block = block.previous_block
        while current_block and previous_block:
            if previous_block.get_block_hash() != current_block.previous_hash:
                return False
            current_block = previous_block
            previous_block = current_block.previous_block
        return True
    
    def save(self, *args, **kwargs):
        assert self.pk is None, "Update not permited"
        self.previous_block = Block.objects.last()
        previous_hash = ''
        if self.previous_block:
            previous_hash = self.previous_block.get_block_hash()
        self.previous_hash = previous_hash
        self.date = datetime.now()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        #raise(Exception('not permited'))
        super().delete(*args, **kwargs)
        
    
    def get_content(self):
        return {
            'previous_hash': self.previous_hash,
            'block_type': self.block_type,
            'date': str(self.date),
            'user': self.user.username,
            'data': self.data,
        }

    
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)



