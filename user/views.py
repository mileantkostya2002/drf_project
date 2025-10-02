from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

class CreatUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated)

    def get_object(self):
        return self.request.user