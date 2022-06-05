from django.shortcuts import render,get_object_or_404
from django.views import generic
from .models import Post, Comment, Like
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.urls import reverse_lazy,reverse
from braces.views import SelectRelatedMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
import json


User = get_user_model()
# Create your views here.

class PostListView(generic.ListView):
    model = Post
    template_name = 'feed/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-date_posted']
    def get_context_data(self,**kwargs):
        context = super(PostListView,self).get_context_data(**kwargs)
        if(self.request.user.is_authenticated):
            # find the list of liked posts
            liked = [i for i in Post.objects.all() if Like.objects.filter(Post=i, user=self.request.user)]
            context['liked_posts'] = liked
        return context

    def get_queryset(self,**kwargs):
        return Post.objects.exclude(user=self.request.user)

class UserPostListView(LoginRequiredMixin,generic.ListView):
    model = Post
    template_name = 'feed/UserPosts.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-date_posted']

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, slug=self.kwargs.get('slug'))
        user = profile.user
        liked = [i for i in Post.objects.all() if Like.objects.filter(Post=i, user=user)]
        context['liked_posts'] = liked
        context['by_user']=user
        return context

    def get_queryset(self,**kwargs):
        profile = get_object_or_404(Profile, slug=self.kwargs.get('slug'))
        user = profile.user
        return Post.objects.filter(user=user)

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'feed/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))
        # post = Post.objects.filter(pk=self.kwargs.get('pk')).first()
        # return post
    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        post = get_object_or_404(Post,pk=self.kwargs.get('pk'))
        is_liked = Like.objects.filter(user=self.request.user,Post=post)
        liked_by = Like.objects.filter(Post=post)
        context['is_liked'] = is_liked
        context['liked_by'] = liked_by
        return context

class CreatePost(LoginRequiredMixin,generic.CreateView):
    model = Post
    form_class = forms.NewPostForm
    template_name = 'feed/create_post.html'
    success_url = reverse_lazy('feed:post_list_view')

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('feed:post_list_view')


# note below that the order LoginRequiredMixin, UserPassesTestMixin, UpdateView
# is important as if we put generic.UpdateView at first position, any user(even not logged in)
# will be allowed to update a post by any other user which we don't want
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,generic.UpdateView):

    model = Post
    fields = ['description','pic','tags']
    template_name = 'feed/update_post.html'
    # success_url = reverse_lazy('feed:user_posts', kwargs={'slug':user.profile.slug})

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # user has to pass the below test function to be able to update a post
    # this comes with UserPassesTestMixin
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def get_success_url(self):
        user = get_object_or_404(User,username__iexact=self.request.user.username)
        return reverse_lazy('feed:user_posts',kwargs={'slug':user.profile.slug})

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
    model = Post
    success_url = reverse_lazy('feed:post_list_view')
    # template_name = 'feed/post_confirm_delete.html'

    # def get_object(slef,*args,**kwargs):
    #     return get_object_or_404(Post,pk=kwargs.get('pk'))

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset()
        # print(self.kwargs)
        # print(kwargs)
        return queryset.filter(pk=self.kwargs.get('pk'))

    # user has to pass the below test function to be able to update a post
    # this comes with UserPassesTestMixin
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

@login_required
def like(request,pk):
    # post_pk = request.GET.get('likeId','')
    # print(request.GET)
    # print("pk is {}".format(post_pk))
    user = request.user
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(Post=post).filter(user=request.user)
    liked = False
    if like:
        like.delete()
    else:
        liked = True
        Like.objects.create(Post=post, user=request.user)
    resp = {'liked':liked}
    response = json.dumps(resp)

    # request.META['HTTP_REFERER'] will keep the user on the same page
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

class SearchPosts(generic.ListView):
    model = Post
    template_name = 'feed/search_posts.html'
    paginate_by = 10
    ordering = ['-date_posted']
    def get_queryset(self):
        query = self.request.GET.get('post_tags')
        list = Post.objects.filter(tags__icontains=query).order_by('-date_posted')
        return list
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        c = self.request.GET.get('post_tags')
        context['tags']=c
        return context

class CommentView(LoginRequiredMixin,generic.CreateView):
    model = Comment
    form_class = forms.NewCommentForm
    template_name = 'feed/comment_form.html'
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.Post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        print(self.object)
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('feed:post_detail_view',kwargs={'pk':self.kwargs.get('pk')})
        # return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

class PostCommentList(generic.ListView):
    model = Comment
    paginate_by = 10
    template_name = 'feed/post_comments.html'

    def get_queryset(self,**kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        # return ['test']
        return post.comments.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        context['post'] = post
        return context
