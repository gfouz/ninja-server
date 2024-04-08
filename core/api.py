from ninja import NinjaAPI

# from posts.api import router as post_router

api = NinjaAPI()

# or by Python path
api.add_router("/posts/", "posts.api.router")
api.add_router("/users/", "users.api.router")
