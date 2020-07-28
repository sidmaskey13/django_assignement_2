from django.urls import path
from .views import CreateBlogView, ListBlogView, DetailBlogView, UpdateBlogView, DeleteBlogView

app_name = 'blog'
urlpatterns = [
    path('', ListBlogView.as_view(), name='list'),
    path('create/', CreateBlogView.as_view(), name='create'),
    path('<int:pk>/', DetailBlogView.as_view(), name='detail'),
    path('update/<int:pk>', UpdateBlogView.as_view(), name='update'),
    path('delete/<int:pk>', DeleteBlogView.as_view(), name='delete'),
]
