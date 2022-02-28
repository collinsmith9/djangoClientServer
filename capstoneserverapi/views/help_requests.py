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
from capstoneserverapi.models import HelpRequest


class HelpRequestView(ViewSet):
    def retrieve(self, request, pk):
        try:
            help_request = HelpRequest.objects.get(pk=pk)
            serializer = HelpRequestSerializer(help_request)
            return Response(serializer.data)
        except HelpRequest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        help_requests = HelpRequest.objects.all()
        user = request.query_params.get('user', None)
        if user is not None:
            help_requests = help_requests.filter(user_id=user)
        serializer = HelpRequestSerializer(help_requests, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = CreateHelpRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            help_request = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        help_request = HelpRequest.objects.get(pk=pk)
        help_request.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        try: 
            help_request = HelpRequest.objects.get(pk=pk)
            serializer = CreateHelpRequestSerializer(help_request, request.data)
            serializer.is_valid(raise_exception=True)
            help_request = serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class HelpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = 'id', 'user', 'employee', 'problem', 'problemDescription'
        depth = 2

class CreateHelpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = 'id', 'user', 'employee', 'problem', 'problemDescription'