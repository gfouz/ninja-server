from ninja import ModelSchema, Schema
from posts.models import Post, Category
from django.contrib.auth.models import User


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "username"]

    # exclude = ["last_login", "user_permissions"]


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = ["name", "description"]


class PostSchema(ModelSchema):
    author: UserSchema

    # categories: CategorySchema
    class Meta:
        model = Post
        fields = ["id", "title", "slug", "content"]


class PostCreateSchema(Schema):
    title: str
    content: str
    author_id: int = None


class PostAuthorSchema(Schema):
    id: int
    title: str
    slug: str
    content: str
    author: UserSchema


class PostUpdateSchema(Schema):
    title: str
    content: str
