from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from blog_app.models import Post,Comment
from blog_app.forms import PostForm,CommentForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,
                                    )
from django.views.generic.edit import UpdateView,DeleteView
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate,get_user_model
from braces.views import SelectRelatedMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()
class AboutView(TemplateView):
    template_name = 'about.html'



class PostListView(ListView):
    model = Post
    template_name = 'blog_app/post_list.html'
    paginate_by = 4
    def get_queryset(self):
        return Post.objects.filter(publish_date__lte = timezone.now()).order_by('-publish_date')

class SearchResultView(ListView):
    model = Post
    template_name = 'blog_app/search_results.html'
    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(Q(title__icontains=query) | Q(text__icontains=query)).distinct().order_by('-publish_date')
        if not query:
            queryset_list = Post.objects.none()
        return queryset_list


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

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class DraftListView(LoginRequiredMixin,ListView):
    login_url = 'accounts/login/'
    redirect_field_name = 'blog_app/post_draft_list.html'
    model = Post
    #template_name = 'blog_app/post_draft_list.html'
    paginate_by = 4
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user,publish_date__isnull=True).order_by('-create_date')

class DeletePostView(LoginRequiredMixin,DeleteView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
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

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    item = Post.objects.get(pk=comment.post.pk)
    if request.user == item.author:
        comment.approve()
        return redirect('blog_app:post_detail',pk=comment.post.pk)
    raise Http404


@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    item = Post.objects.get(pk=comment.post.pk)
    if request.user == item.author:
        comment.delete()
        return redirect('blog_app:post_detail',pk=comment.post.pk)
    raise Http404
