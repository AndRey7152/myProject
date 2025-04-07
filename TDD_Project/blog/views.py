from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView

from .models import Post

# Create your views here.
class CreatePostView(PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_post'
    model = Post
    fields = ('name', 'content')
    template_name = 'post.html'