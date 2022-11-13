from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import PostForm
from .models import Category, City, CustomUser, Follow, Post
from .service import TelegrammMessage, Weather


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


class AboutView(View):
    def get(self, request):
        user = CustomUser.objects.filter(is_superuser=True)
        return render(request, 'about.html', locals())


class FollowView(View):
    def post(self, request):
        user = request.POST['user']
        user2 = request.user
        Follow.objects.create(user_id=user, follower=user2)
        return redirect('user', request.POST['username'])


class DelFollowView(View):
    def post(self, request):
        user = request.POST['user']
        user2 = request.user
        follow = Follow.objects.filter(user_id=user, follower=user2)
        follow.delete()
        return redirect('user', request.POST['username'])


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html', locals())

    def post(self, request):
        info = request.POST
        info = ('Имя: {} Номер: {} email: {}').format(info['name'], info['text'], info['email'])
        TelegrammMessage(message=info)
        if request.POST['message']:
            TelegrammMessage(message=request.POST['message'])
        return redirect('home')


class AuthorView(View):
    def get(self, request, username):
        if username == request.user.username:
            return redirect('profile')
        user = get_object_or_404(CustomUser, username=username)
        try:
            follow = Follow.objects.get(follower = request.user, user = user)
        except:
            follow = None
        post = Post.objects.filter(author=user)
        return render(request, 'user.html', locals())

