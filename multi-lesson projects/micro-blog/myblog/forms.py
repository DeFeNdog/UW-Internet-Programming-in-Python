from django.forms import ModelForm
from myblog.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'author']
