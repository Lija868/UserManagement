from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from api_v0.serializers import UserSerializer, RegisterSerializer

from api_v0.utils import validate_email, validate_password, validate_null_or_empty


class RegisterViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):

        name = request.data.get("first_name")
        email = request.data.get("email")
        password = request.data.get("password")

        # display what are the fields which tent to empty.
        validations = []
        validations = validate_null_or_empty(name, 702, "First Name", validations)
        validations = validate_null_or_empty(email, 705, "Email", validations)
        validations = validate_null_or_empty(password, 706, "Password", validations)

        if len(validations) > 0:
            resp = {}
            resp["code"] = 600
            resp["validations"] = validations
            return Response(resp)

        if not validate_email(email):
            return Response({"code": 708, "message": "Email is not valid"})
        if not validate_password(password):
            return Response({"code": 709, "message": "Email is not valid"})
        request.data["username"] = request.data.get("email")

        user_obj = get_user_model().objects.filter(email=email).count()
        if user_obj >= 1:
            return Response({"code": 710, "message": "Email is already registered, try another Email."})

        RegisterSerializer.create(self, request.data)
        return Response({"code": 200, "message": "ok"})


class LoginViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        user_name = request.data.get("email")
        password = request.data.get("password")
        try:
            user = get_user_model().objects.get(email = user_name)
            valid = user.check_password(password)
            if not valid:
                return Response(status=status.HTTP_204_NO_CONTENT)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request)



