from django.db import models
from datetime import datetime
import hashlib

class Block(models.Model):
    _saved = False
    previous_block = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    block_type = models.IntegerField()
    date = models.DateTimeField()
    user = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    data = models.TextField(default="")
    block_hash = models.CharField(max_length=512)

    # def __init__(self, block_type, data, user, *args, **kwargs):
    #     self.block_type = block_type
    #     self.data = data
    #     self.user = user
    #     super().__init__(self, *args, **kwargs)

    def get_previous_hash(self):
        prev = ''
        if hasattr(self, 'previous_block'):
            if self.previous_block:
                prev = self.previous_block.block_hash
        return prev

    def _hash(self):
        prev = self.get_previous_hash()        
        content = (prev + str(self.block_type) + self.date.ctime() + self.user.username + self.data).encode('utf-8')
        return hashlib.sha256(content).hexdigest()
    
    def get_current_block_hash(self):
        return self._hash()
    
    def verify(self, block_id, data):
        #implementar ainda
        return True
    
    def save(self, *args, **kwargs):
        assert self.pk is None, "Update not permited"
        self.previous_block = Block.objects.last()
        self.date = datetime.now()
        self.block_hash = self._hash()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise(Exception('not permited'))
        
    
    def get_content(self):
        prev = self.get_previous_hash()
        return {
            'previous_hash': prev,
            'block_type': self.block_type,
            'date': str(self.date),
            'user': self.user.username,
            'data': self.data,
            '_block_hash': self.get_current_block_hash()
        }

    
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)

    