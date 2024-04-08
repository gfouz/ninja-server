from ninja import Router
from ninja.responses import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from posts.models import Post
from ninja.security import HttpBearer
from django.conf import settings
from posts.schemas import PostSchema, PostUpdateSchema, UserSchema
from posts.schemas import PostAuthorSchema, PostCreateSchema
import jwt

import os
from django.http import FileResponse
from django.conf.urls.static import static
from django.shortcuts import render


router = Router()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == _token:
            return token


@router.get("/{slug}")
def render_markdown(request, slug):
    allposts = Post.objects.all()
    markdown_content = get_object_or_404(Post, slug=slug)
    context = {"post": markdown_content, "links": allposts}
    return render(request, "index.html", context=context)


@router.get("/get/post/{post_id}", response={200: PostAuthorSchema})
def get_one_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return post


@router.get(
    "/postlist/",
    response={200: list[PostAuthorSchema]},
    description="this returns a list of all posts",
)
def get_all_posts(request):
    return Post.objects.all()


@router.post(
    "/create/newpost", response=PostSchema, description="this creates one post"
)
def create_post(request, payload: PostCreateSchema):
    if Post.objects.filter(title=payload.title).exists():
        return {"message": "title already exists"}
    else:
        post = Post.objects.create(**payload.dict())
        return post


@router.put("/update/post/{post_id}", description="this updates one post")
def update_post(request, post_id: int, payload: PostUpdateSchema):  # <===
    post = get_object_or_404(Post, id=post_id)
    for attr, value in payload.dict().items():
        setattr(post, attr, value)
        post.save()
        return {"updated": True}


@router.delete("/delete/post/{post_id}", description="this delete one post")
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return {"message": "post deleted successfully"}
