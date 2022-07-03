from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy,reverse
from . import models
from django.views import generic
from django.contrib.auth.decorators import login_required

from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from . import forms
from django.contrib.auth import get_user_model

from django.http import HttpResponseRedirect
User = get_user_model()
# Create your views here.

class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class MyProfileView(generic.TemplateView):
    template_name = 'accounts/my_profile_page.html'

class users_list(generic.ListView):
    model = models.Profile
    template_name = 'accounts/user_list.html'

    def get_queryset(self):
        return models.Profile.objects.exclude(user=self.request.user)

class friend_list(generic.ListView):
    model = models.Profile
    template_name = 'accounts/friend_list.html'

    def get_queryset(self):
        user = get_object_or_404(models.Profile, slug = self.kwargs.get('slug'))
        # print("user : {}".format(user))
        return user.friends.all()
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['list_user_profile'] = get_object_or_404(models.Profile, slug = self.kwargs.get('slug'))
        return context

class user_profile(generic.DetailView):
    template_name = 'accounts/profile_detail.html'
    queryset = models.Profile.objects.all()
    # print("hello")
    # print(queryset)

    def get_object(self):
        # print("hello 1")
        # print(self.kwargs.get('slug'))
        return get_object_or_404(models.Profile, slug=self.kwargs.get('slug'))

    def get_context_data(self,*args,**kwargs):
        context = super(user_profile, self).get_context_data(*args,**kwargs)

        p = models.Profile.objects.filter(slug = self.kwargs.get('slug')).first()
        u = p.user

        friends = p.friends.all()

        sent_friend_request = models.FriendRequest.objects.filter(from_user = u)
        rec_friend_request = models.FriendRequest.objects.filter(to_user = u)
        # user_posts = Post.objects.filter(user_name=u)
        button_status = 'none'
        # print(self.request.user)
        # print(User.objects.first())
        # print(p)
        # print("user friends {}".format(u.profile.friends.all()))
        if self.request.user.profile not in u.profile.friends.all():
            button_status = 'not_friend'
        else :
            button_status = 'friend'

        # if we have sent him a friend request
        if len(models.FriendRequest.objects.filter(
        from_user = self.request.user).filter(to_user = p.user))==1:
            button_status = 'friend_request_sent'
        # if len(models.FriendRequest.objects.filter(from_user=self.request.user).filter(to_user=p.user)) == 1:
		# 	button_status = 'friend_request_sent'

		# if we have recieved a friend request
        if len(models.FriendRequest.objects.filter(
        from_user=p.user).filter(to_user=self.request.user))==1:
            button_status = 'friend_request_received'
		# if len(models.FriendRequest.objects.filter(
        # from_user=p.user).filter(to_user=self.request.user)) == 1:
		# 		button_status = 'friend_request_received'

        context['u']=u
        context['button_status'] = button_status
        context['friends'] = friends
        context['sent_friend_request'] = sent_friend_request
        context['rec_friend_request'] = rec_friend_request
        # context['post_count'] = user.posts.count

        return context

class ProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin,generic.UpdateView):
    model = models.Profile
    # fields = ['image','bio']
    form_class = forms.ProfileUpdateForm
    template_name = 'accounts/profile_update_page.html'
    def test_func(self):
        curr_user = get_object_or_404(User, username = self.request.user.username)
        profile = self.get_object()
        if profile.user == curr_user:
            return True
        return False

    def get_success_url(self):
        user = get_object_or_404(User, username__iexact  = self.request.user.username)
        print(user.username)
        return reverse_lazy('accounts:profile_page')

@login_required
def send_friend_request(request, id):
    t_user = get_object_or_404(User, id=id)
    f_user = User.objects.first()
    frequest = models.FriendRequest.objects.get_or_create(
        from_user = f_user,
        to_user = t_user
    )
    return HttpResponseRedirect('/accounts/profile_page/')

@login_required
def cancel_friend_request(request,id):
    t_user = get_object_or_404(User, id=id)
    frequest = models.FriendRequest.objects.filter(
        from_user = request.user,
        to_user = t_user
    )
    frequest.delete()
    return HttpResponseRedirect('/accounts/profile_page/')

@login_required
def accept_friend_request(request, id):
    f_user = get_object_or_404(User, id=id) # from_user
    frequest = models.FriendRequest.objects.filter(
        from_user = f_user,
        to_user = request.user
    ).first()
    user1 = frequest.to_user
    user2 = f_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if(models.FriendRequest.objects.filter(from_user=request.user, to_user=f_user).first()):
        reverse_req = models.FriendRequest.objects.filter(f_user=request.user,to_user=f_user).first()
        reverse_req.delete()
    frequest.delete()
    return HttpResponseRedirect('/accounts/profile_page')

@login_required
def decline_friend_request(request,id):
    f_user = get_object_or_404(User, id=id)
    frequest = models.FriendRequest.objects.filter(
        from_user = f_user,
        to_user = request.user
    ).first()
    frequest.delete()

def delete_friend(request, id):
    f_user = get_object_or_404(User, id=id)
    print("user is {}".format(f_user))
    f_user.profile.friends.remove(request.user.profile)
    request.user.profile.friends.remove(f_user.profile)
    return HttpResponseRedirect('/accounts/profile_page')

# @login_required
# def search_users(request):
#     query = request.GET.get('q')
#     object_list = User.objects.filter(username__icontains=query)
#     context = {
#         'users':object_list
#     }
#     return render(request,'accounts/users/search_users.html',context)

class search_users(generic.ListView):
    model = User
    template_name = 'accounts/search_users.html'
    # print("hello")
    def get_queryset(self,**kwargs):
        query = self.request.GET.get('user_name')
        # print('hello{}'.format(query))
        object_list = User.objects.filter(username__icontains=query)
        return object_list
        # context = super().get_context_data(**kwargs)
        # print(self.request.GET.get('user_name'))
        # name = self.request.GET.get('user_name')
        # context['search_results']=User.objects.filter(username__icontains=name)
        # return context
# TODO : edit profile
