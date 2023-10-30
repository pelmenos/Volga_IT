from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .consts import UP_BALANCE

User = get_user_model()


class IncreaseBalance(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user(self, pk):
        try:
            return User.objects.get(id=pk)
        except Exception:
            raise NotFound()

    def post(self, request, pk):
        if request.user.isAdmin:
            user = self.get_user(pk)
        elif request.user.id == pk:
            user = request.user
        else:
            raise PermissionDenied()

        user.balance += UP_BALANCE
        user.save()
        return Response({'message': 'Balance increased'}, status=status.HTTP_200_OK)

