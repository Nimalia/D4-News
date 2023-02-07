from django.urls import path
from .views import PostList, PostDetail, PostSearchList, PostSearchDetail, PostCreate, PostUpdate, PostDelete, \
   CategoryListView, subscribe, unsubscribe

urlpatterns = [
   path('', PostList.as_view(), name="post_list"),
   path('<int:pk>', PostDetail.as_view(), name="post_detail"),
   path("search/", PostSearchList.as_view(), name="post_search"),
   path('<int:pk>', PostSearchDetail.as_view(), name="post_search_det"),
   path("create/", PostCreate.as_view(), name="post_create"),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
   # path('subscriptions/', subscriptions, name='subscriptions'),
]