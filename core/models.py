from django.db import models
from datetime import datetime
import hashlib

class Block(models.Model):
    _saved = False
    previous_block = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    previous_hash = models.CharField(max_length=512)
    block_type = models.IntegerField()
    date = models.DateTimeField()
    user = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    data = models.TextField(default="")

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
        prev = self.get_previous_hash()
        return {
            'previous_hash': prev,
            'block_type': self.block_type,
            'date': str(self.date),
            'user': self.user.username,
            'data': self.data,
        }

    
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)

    