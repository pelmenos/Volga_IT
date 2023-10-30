from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import CustomUser


class UserSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},
                        'is_active': {'read_only': True},
                        'isAdmin': {'read_only': True},
                        }


class TokenObtainPairResponseSerializer(Serializer):
    access = CharField()
    refresh = CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(Serializer):
    access = CharField()
    refresh = CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
