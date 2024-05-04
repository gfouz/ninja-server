from ninja import Router
from ninja.responses import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from posts.models import Post
from ninja.security import HttpBearer
from django.conf import settings
from posts.schemas import PostSchema, PostUpdateSchema, UserSchema
from posts.schemas import PostFullSchema, PostCreateSchema
import jwt

import os
from django.http import FileResponse
from ninja.errors import HttpError
from django.conf.urls.static import static
from django.shortcuts import render


router = Router()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            # print("this is the token :" + token)
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except:
            raise HttpError(401, "Not authorarized, invalid token!")


@router.get("/bearer", auth=AuthBearer())
def bearer(request):
    return {"payload": request.auth}


@router.get("/{slug}")
def render_markdown(request, slug):
    allposts = Post.objects.all()
    markdown_content = get_object_or_404(Post, slug=slug)
    context = {"post": markdown_content, "links": allposts}
    return render(request, "index.html", context=context)


@router.get("/get/post/{post_id}", response={200: PostFullSchema})
def get_one_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return post


@router.get("/get/single/post/{post_id}", response={200: PostFullSchema})
def get_post(request, post_id: int):
    try:
        post = Post.objects.get(id=post_id)
        return post
    except Post.DoesNotExist:
        raise HttpError(404, "Not found!.")


@router.get("/postlist/", response={200: list[PostFullSchema]})
def get_all_posts(request):
    return Post.objects.all()


@router.post("/create/newpost", response=PostSchema, auth=AuthBearer())
def create_post(request, payload: PostCreateSchema):
    if Post.objects.filter(title=payload.title).exists():
        return {"message": "title already exists"}
    else:
        post = Post.objects.create(**payload.dict())
        return post


@router.put("/update/post/{post_id}", response=PostSchema)
def update_post(request, post_id: int, payload: PostUpdateSchema):
    post = get_object_or_404(Post, id=post_id)
    for attr, value in payload.dict().items():
        setattr(post, attr, value)
    post.save()
    return post


@router.delete("/delete/post/{post_id}", auth=AuthBearer())
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return {"message": "post deleted successfully"}
