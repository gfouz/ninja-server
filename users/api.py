from ninja import Router, Form
from ninja.responses import Response
from ninja import Schema
from posts.schemas import UserSchema
from users.schemas import UserFullSchema
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render
import jwt
from ninja.security import HttpBearer
from ninja.errors import HttpError


# token for RobinHood user
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6IlJvYmluSG9vZCJ9.Vk-799HIsCsO4bsuitXoXYvHfUhffLxgBSZN5ZLFG-g

router = Router()


class UserRegister(Schema):
    username: str
    email: str
    password: str


class UserLogin(Schema):
    username: str
    password: str


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except:
            raise HttpError(401, "Not authorarized, invalid token!")


@router.get("/bearer", auth=AuthBearer())
def bearer(request):
    return {"payload": request.auth}


@router.get("/get/users", response={200: list[UserFullSchema]})
def get_user_list(request):
    users = User.objects.all()
    return users


@router.get("/allusers", response={200: list[UserSchema]})
def get_users(request):
    users = User.objects.all()
    return users


@router.post("/register")
def register_user(request, data: UserRegister):
    if User.objects.filter(username=data.username).exists():
        return {"message": "Username already exists"}
    user = User(username=data.username, email=data.email)
    user.set_password(data.password)
    user.save()

    return {"message": "User created successfully"}


@router.post("/login")
def login(request, data: UserLogin):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None:
        # Create JWT token
        payload = {
            "user_id": user.id,
            "username": user.username,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        # response = Response({"token": token})
        # response.set_cookie("access_token", token, httponly=True)
        return {"user_id": user.id, "token": token}
    else:
        return {"error": "Invalid credentials"}


@router.get("/hello")
def hello(request):
    return render(request, "users.html")
