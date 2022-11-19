from django.shortcuts import redirect, render
from django.views import View
from app.models import CustomUser, Post, Follow, Task
from .forms import CustomUserForm, UserRegistrationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user 
        follow = Follow.objects.filter(follower=user)
        post = Post.objects.filter(author=user)
        task = Task.objects.filter(user = user)[:10]
        form = CustomUserForm(instance=user)
        return render(request, 'profile.html', locals())

    def post(self, request):
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if request.FILES.get('photo'):
                photo = request.FILES.get('photo')
            else:
                photo = form.instance.image
            user = CustomUser.objects.update_or_create(id=request.user.id,
            defaults={
                'description': request.POST.get('description'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'image': photo,
            })
        return redirect('profile')


class RegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', locals())


    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        else:
            form = UserRegistrationForm()
        
