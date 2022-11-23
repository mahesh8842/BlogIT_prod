from django.shortcuts import render,redirect,get_object_or_404
from .form import *
from .models import *
from datetime import datetime
# Create your views here.
from django.contrib.auth import logout

def likepost(request,id):
    try:
        obj = BlogModel.objects.get(id=id)
        print(request.user)
        obj.likes.add(request.user)
        obj.save()
        redirect_url='/blog_detail/'+obj.slug
        return redirect(redirect_url)
    except Exception as e:
        print(e)


def home(request):
    from random import choice
    pks = BlogModel.objects.values_list('pk', flat=True)
    random_pk = choice(pks)
    random_obj = BlogModel.objects.get(pk=random_pk)
    # return HttpResponse('home')
    blogs = BlogModel.objects.all().order_by('-created_at')
    return render(request,'home.html',{'blogs':blogs,'random':random_obj})


def category_view(request,name):
    categories=BlogModel.objects.all()
    filtered=categories.filter(category=name)
    return render(request,'category.html',{'categories':categories,'selected_category':filtered,'current':name})

def login_view(request):
    return render(request,'login.html',{})

def logout_view(request):
    logout(request)
    return redirect('/')

def register_view(request):
    return render(request,'register.html',{})

def blog_detail(request,slug):
    try:
        blog = BlogModel.objects.filter(slug=slug)
        print(blog[0].liked_by(),'-----------------------')
    except Exception as e:
        print(e)
    return render(request,'blog_detail.html',{'blog_obj':blog[0]})

def view_blog(request):
    try:
        blogs=BlogModel.objects.filter(user=request.user)
    except Exception as e:
        print(e)
    return render(request,'view_blog.html',{'blog_objs':blogs})

def delete_blog(request,id):
    try:
        blog_obj=BlogModel.objects.get(id=id)
        if blog_obj.user==request.user:
            blog_obj.delete()
    except Exception as e:
        print(e)
    return redirect('/')

def blog_update(request, slug):
    print('not post request')
    context = {}
    try:

        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': blog_obj.content,'summary':blog_obj.summary}

        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            print('form submitted')
            form = BlogForm(request.POST)
            # print(request.FILES)
            image = request.FILES.get('image','')
            title = request.POST.get('title')
            category = request.POST.get('category')
            user = request.user
            summary= request.POST.get('summary')
            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj.title = title if title!=None else blog_obj.title
            blog_obj.content = content if content!=None else blog_obj.content
            blog_obj.summary = summary if summary!=None else blog_obj.summary
            blog_obj.category = category if category!=None else blog_obj.category
            blog_obj.cover_image = image if image!='' else blog_obj.cover_image
            blog_obj.updated_at=datetime.now()
            blog_obj.save()

            redirect_url='/blog_detail/'+blog_obj.slug
            return redirect(redirect_url)
            #  add snack bar here
        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)
    print(context)
    return render(request, 'update_blog.html', context)


def add_blog(request):
    message = ''
    try:
        if request.method=='POST':
            form = BlogForm(request.POST)
            image = request.FILES.get('image','')
            title=request.POST.get('title')
            category=request.POST.get('category')
            user = request.user
            summary=request.POST.get('summary','')

            if form.is_valid():
                content = form.cleaned_data['content']
                # summary = form.cleaned_data['summary']
                obj = BlogModel.objects.create(
                    title=title,
                    content=content,
                    cover_image=image,
                    user=user,
                    summary=summary,
                    category=category
                )
            redirect_url='/blog_detail/'+obj.slug
            return redirect(redirect_url)
    except Exception as e:
        message = e

    return render(request,'add_blog.html',{'form':BlogForm,'message':message})

def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e:
        print(e)

    return redirect('/')

