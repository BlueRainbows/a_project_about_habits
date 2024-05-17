from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from users.models import User
from users.serializers.user import UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data['password'])
        user.save()


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
