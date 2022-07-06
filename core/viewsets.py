import hashlib
from core.serializers import UserSerializer, BlockSerializer, DocSerializer
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from core.models import User, Block, Document
from wsgiref.util import FileWrapper
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['last_login']
    ordering = ['-last_login']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        obj = User.objects.get(lookup_field_value)
        self.check_object_permissions(self.request, obj)
        return obj

class BlockViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = BlockSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date']
    ordering = ['date']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        vdata = serializer.validated_data
        user = request.user
        try:
            file = request.data['file']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        
        md5 = hashlib.md5()
        if file.multiple_chunks():
            for chunk in file.chunks():
                md5.update(chunk)
        else:
            md5.update(file.read())
        
        file_hash = md5.hexdigest()

        doc = Document()
        doc.file = file
        doc.user = user
        doc.hash = file_hash
        doc.save()

        block_type = vdata['block_type']
        block = Block()
        block.user = user
        block.data = file_hash
        block.block_type = block_type
        block.save()
        
        return Response(BlockSerializer(block).data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Block.objects.all()
        else:
            return Block.objects.filter(user=self.request.user)
    
    def retrieve(self, request, pk=None):
        return BlockSerializer(Block.objects.get(pk=pk))

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        obj = Block.objects.get(lookup_field_value)
        self.check_object_permissions(self.request, obj)
        return obj

class DocumentViewSet(viewsets.ViewSet):
    http_method_names = ['get']
    permission_classes = (IsAuthenticated,)
    lookup_field = 'hash'

    
    def retrieve(self, request, hash=None):
        print('!@#!@#!@#')
        try:
            doc = Document.objects.get(hash=hash)
            if self.request.user.is_superuser or doc.user.username == self.request.user.username:
                #return Response(DocSerializer(doc).data, status=status.HTTP_200_OK)
                file_handle = doc.file.path
                document = open(file_handle, 'rb')
                response = HttpResponse(FileWrapper(document), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="%s"' % doc.file.name
                return response
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
