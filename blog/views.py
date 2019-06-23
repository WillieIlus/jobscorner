from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from hitcount.views import HitCountDetailView

from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form, )


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'form.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('Post_list')
    template_name = 'delete.html'


class PostList(ListView):
    queryset = Post.published.all()
    context_object_name = 'post'
    template_name = 'Blog/list.html'


class PostDetail(HitCountDetailView):
    queryset = Post.published.all()
    context_object_name = 'post'
    template_name = 'Blog/detail.html'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        # context['meta'] = self.get_object().as_meta(self.request)
        # context['related'] = self.object.tags.similar_objects()[:4]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        body = form.cleaned_data['body']
        comment = Comment()
        comment.post = post
        comment.user = request.user
        comment.body = body
        comment.save()
        '''
        Always return an HttpResponseRedirect after successfully dealing
        with POST data. This prevents data from being posted twice if a
        user hits the Back button.
        '''
        return HttpResponseRedirect(reverse('blog:detail', args=(post.slug,)))
    return render(request, 'blog/detail.html', {'post': post, 'form': form})
