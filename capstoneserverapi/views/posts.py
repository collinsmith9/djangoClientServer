from socketserver import ThreadingUDPServer
from wsgiref.util import setup_testing_defaults
from django.forms import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
from datetime import datetime
from rest_framework.decorators import action
from capstoneserverapi.models import Post


class PostView(ViewSet):
    def retrieve(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = CreatePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        try: 
            post = Post.objects.get(pk=pk)
            serializer = CreatePostSerializer(post, request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)







    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = 'id', 'user', 'problem', 'problemDescription'
        depth = 2

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = 'id', 'user', 'problem', 'problemDescription'


        
