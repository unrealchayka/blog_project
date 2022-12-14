from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import PostForm, ContactForm, TaskForm
from .models import Category, City, CustomUser, Follow, Post, Task
from .service import Weather, send_message


class HomeView(View):
    def get(self, request):
        city = City.objects.all()
        paginator = Paginator(city, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', locals())

    def post(self, request):
        w = Weather(request.POST.get('city').title())
        if not w:
            return redirect('home')
        try: 
            detail_city = City.objects.get(
            Q(title_ru=request.POST.get('city').title())|
            Q(title_eng=request.POST.get('city').title())
                )
        except:
            detail_city = None
        
        return render(request, 'index.html', locals())


class DetailCityView(View):
    def get(self, request, slug):
        city =  get_object_or_404(City, slug=slug)
        w  = Weather(city.title_ru)

        return render(request, 'detail_city.html', locals())
    

class BlogView(View):
    def get(self, request):
        blog = Post.objects.select_related('category', 'author')
        if request.GET.get('date') == 'newest':
            newest = datetime.now() - timedelta(minutes=60 * 24 * 7)
            blog = blog.filter(date_create__gte=newest)
        elif request.GET.get('slug'):
            blog = blog.filter(category__slug=request.GET.get('slug'))   
        category = Category.objects.all()
        paginator = Paginator(blog, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog.html', locals())


class DetailPostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        return render(request, 'detail.html', locals())


@method_decorator(login_required, name='dispatch')
class CreatePostView(View):

    def get(self, request):
        form = PostForm
        post = Post.objects.filter(author__username=request.user)
        post = post.filter(date_create__gte=datetime.now()-timedelta(minutes=60*24)).last()
        limit=False
        if post: 
            limit = post.date_create + timedelta(minutes=60*27)
            if request.user.is_staff:
                limit=False

        return render(request, 'create.html', locals())

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(
                title = request.POST.get('title'),
                image = request.FILES.get('image'),
                author_id = request.user.id,
                category_id = request.POST.get('category'),
                text = request.POST.get('text'),
            )
            return redirect('detail_post', post.id)
        else:
            form = PostForm()
        return redirect('create-post')
        

class DeleteBlogView(View):
    def post(self, request):
        post = get_object_or_404(Post, id = request.POST.get('slug'), user = request.POST.get('user'))
        post.delete()
        return redirect('')


class AboutView(View):
    def get(self, request):
        user = CustomUser.objects.filter(is_superuser=True)
        return render(request, 'about.html', locals())


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html', locals())

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            send_message(form.cleaned_data['name'], form.cleaned_data['text'],
                     form.cleaned_data['email'], form.cleaned_data['message']) 
        return render(request, 'contact.html', locals())


class AuthorView(View):
    def get(self, request, username):
        if username == request.user.username:
            return redirect('profile')
        user = get_object_or_404(CustomUser, username=username)
        post = Post.objects.filter(author=user).select_related('category')
        try:
            follow = Follow.objects.select_related('user', 'follower').get(follower = request.user, user = user)
        except:
            follow = None
        return render(request, 'user.html', locals())
    
    def post(self, request, username):
        post = Post.objects.filter(author__username=username).select_related('category')
        user = get_object_or_404(CustomUser, username=username)

        if not request.POST['a']:
            follow = Follow.objects.filter(user_id=request.POST['user'], follower=request.user)
            follow.delete()
        else:
            follow = Follow.objects.create(user_id=request.POST['user'], follower=request.user)
        return render(request, 'user.html', locals())


class CreateTaskView(View):
    def post(self, request):
        form = TaskForm(request.POST)   
        if form.is_valid():
            Task.objects.create(
                user = request.user, 
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description']
            )
        return redirect('profile')

class DelTaskView(View):
    def post(self, request):
        task = Task.objects.filter(user = request.user, id = request.POST['id'])
        task.delete()
        return redirect('profile')