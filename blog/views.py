from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from django.contrib import messages
from .forms import PostForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
# from urllib import quote_plus

# Create your views here.
def home(request):
    # qs = Post.objects.all().order_by('-made')
    # qs = Post.objects.all()
    if request.user.is_staff or request.user.is_superuser:
        qs = Post.objects.all()
    else:
        qs = Post.objects.active()

    query = request.GET.get('query')
    if query:
        qs = Post.objects.filter(
            Q(title__icontains = query) |
            Q(content__icontains = query) |
            Q(user__first_name__icontains = query) |
            Q(user__last_name__icontains = query) 
            ).distinct()

    paginator = Paginator(qs, 2) # Show 25 contacts per page.

    cur_page = 'page'
    page_number = request.GET.get(cur_page)
    page_obj = paginator.get_page(page_number)


    if request.user.is_authenticated:
        text = "swagat nhi karoge humara"
    else:
        text = "wait a minute! who are you?"

    data = {"text": text, 'page_obj': page_obj, "cur_page": cur_page}
    # data = {"text": text, 'page_obj': page_obj}
    return render(request, "blogHTML/allposts.html", data)

# def listing(request):
   
#     return render(request, 'list.html', {'page_obj': page_obj})

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    # if not request.user.is_authenticated():
    #     raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.url())
    context = {
        "form": form,
    }
    return render(request, "blogHTML/update.html", context)


def update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.url())
        
    context ={
        "title": instance.title,
        "instance": instance,
        "form":form
        }
    return render(request, "blogHTML/update.html", context)


def delete(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    return redirect( "posts:home")

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # share_string = quote_plus(instance.content)
    # post = Post.objects.get(id=id)
    # if request.user.is_authenticated:
    #     text = 'swagat nhi karoge humara'
    # else:
    #     text = 'wait a minute! who are you?'
    data = {"post": post}
    # data = {"post": post, 'share_string': share_string}
    return render(request, "blogHTML/detail.html", data)

