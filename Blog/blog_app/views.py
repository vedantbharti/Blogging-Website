from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from blog_app.models import Post,Comment
from blog_app.forms import PostForm,CommentForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,
                                    UpdateView,DeleteView)
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate,get_user_model
from braces.views import SelectRelatedMixin

User = get_user_model()
class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(SelectRelatedMixin,ListView):
    model = Post
    select_related = ('author')

    def get_queryset(self):
        return Post.objects.filter(publish_date__lte = timezone.now()).order_by('-publish_date')


class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'blog_app/post_detail.html'
    form_class = PostForm
    model = Post

class UpdatePostView(LoginRequiredMixin,UpdateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'blog_app/post_detail.html'
    form_class = PostForm
    model = Post

class DraftListView(LoginRequiredMixin,ListView):
    login_url = 'accounts/login/'
    redirect_field_name = 'blog_app/post_draft_list.html'
    model = Post


    def get_queryset(self):
        return Post.objects.filter(publish_date__isnull=True).order_by('-create_date')

class DeletePostView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('blog_app:post_list')




####################################################
####################################################



@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog_app:post_detail',pk=pk)


def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog_app:post_detail',pk=post.pk)

    else:
        form = CommentForm()
    return render(request,'blog_app/comment_form.html',{'form':form})

# @login_required
# def post_remove(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.delete()
#     return redirect('post_list')


@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog_app:post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog_app:post_detail',pk=post_pk)
