from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin
from AccountController.serializers import UserSerializer

User = get_user_model()


class AccountList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def get_queryset(self):
        queryset = self.queryset
        start = int(self.request.query_params.get('start') or 0)
        count = int(self.request.query_params.get('count') or 0)
        if start and count:
            query_set = queryset[start:start+count]
        elif start:
            query_set = queryset[start:]
        elif count:
            query_set = queryset[:count]
        else:
            query_set = queryset[:]
        return query_set


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
