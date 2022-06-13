from core.models import User, Block
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', ]

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['previous_hash', 'user', 'date', 'block_type', 'data']
    

    

        
    
    
    
