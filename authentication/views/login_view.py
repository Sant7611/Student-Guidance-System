# from rest_framework_simplejwt.views import TokenObtainPairView
# from authentication.serializers.login_serializer import LoginSerializer

# class LoginView(TokenObtainPairView):

#     serializer_class = LoginSerializer



from authentication.serializers.login_serializer import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from utils.response_helpers import error_response, success_response
from rest_framework.permissions import AllowAny
from rest_framework import generics

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request':request})
        if not serializer.is_valid():
            return error_response(errors=serializer.errors,status_code=400 )
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        print(user.role)
        print(user.id)
        print(user.username)
        data={
            'user':{
                'user_id':user.id,
                'username':user.username,
                'email':user.email,
                'role':user.role
            },
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
        
        return success_response(message="Successfully logged in" ,data=data, status_code=200)