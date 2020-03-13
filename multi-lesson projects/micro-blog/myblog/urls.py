from django.conf.urls import url
from .views import post_form_view
from .views import list_view
from .views import detail_view

urlpatterns = [
    url(r'^$', list_view, name="blog_index"),
    url(r'^post-form/', post_form_view, name="post_form"),
    url(r'^posts/(?P<post_id>\w+)/', detail_view, name="blog_detail")
]
