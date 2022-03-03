
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
from datetime import datetime
from rest_framework.decorators import action
from capstoneserverapi.models import CodeUser
from django.contrib.auth.models import User


class CodeUserView(ViewSet):
    def retrieve(self, request, pk):
        try:
            code_user = CodeUser.objects.get(pk=pk)

            serializer = CodeUserSerializer(code_user)
            return Response(serializer.data)
        except CodeUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        code_users = CodeUser.objects.all()
        # is_staff = request.query_params.get('is_staff', None)
        # if is_staff is not None:
        #     code_users = code_users.filter(is_staff=is_staff)
        serializer = CodeUserSerializer(code_users, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def makeadmin(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_staff = 1
            user.save()
            return Response ({'message: User is now an admin'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class CodeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeUser
        fields = 'id', 'user', 'bio'
        depth = 2
        # exclude = ['password']

# class NestedSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = User
#             depth = 1
#             fields = 'username', 'is_staff', 'first_name', 'last_name' # Originally set to '__all__'