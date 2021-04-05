from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from PetPhotos.models import Category, Picture, Pet, Comment
from PetPhotos.forms import CategoryForm, UserForm, PetForm, PictureForm, CommentForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Max

def index(request):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results
    return render(request, 'PetPhotos/index.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results
    try:
        category = Category.objects.get(slug=category_name_slug)
        pictures = Picture.objects.filter(category=category)
        context_dict['pictures'] = pictures
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pictures'] = None

    return render(request, 'PetPhotos/category.html', context=context_dict)


def categories(request):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results
    show_categories = Category.objects.all()
    context_dict['categories'] = show_categories

    return render(request, 'PetPhotos/categories.html', context=context_dict)


def user_profiles(request):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results
    profiles = User.objects.order_by('username')
    context_dict['profiles'] = profiles

    return render(request, 'PetPhotos/user_profiles.html', context=context_dict)


def user_profile(request, username):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results
    user = User.objects.get(username=username)
    pets = Pet.objects.filter(owner=User.objects.get(username=user.username))
    context_dict['user'] = user
    context_dict['pets'] = pets
    return render(request, 'PetPhotos/user_profile.html', context=context_dict)


def view_pet_profile(request, pet_slug):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results
    pet = Pet.objects.get(slug=pet_slug)
    context_dict['pet'] = pet
    return render(request, 'PetPhotos/view_pet_profile.html', context=context_dict)


@login_required
def add_category(request):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results

    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/PetPhotos/')

        else:
            print(form.errors)

    context_dict['form'] = form

    return render(request, 'PetPhotos/add_category.html', context=context_dict)


@login_required
class LikePictureView(View):
    @method_decorator(login_required)
    def get(self, request):
        picture_id = request.GET['picture_id']
        try:
            picture = Picture.objects.get(id=int(picture_id))
        except Picture.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        picture.rating = picture.rating + 1
        picture.save()

        return HttpResponse(picture.rating)


def register(request):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    context_dict['user_form'] = user_form
    context_dict['registered'] = registered

    return render(request, 'PetPhotos/register.html', context=context_dict)


def user_login(request):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('PetPhotos:index'))
            else:
                return HttpResponse("Your account is disabled!")
        else:
            print("Invalid username or password. Please check the details again!")
            return HttpResponse("Invalid details entered.")
    else:
        return render(request, 'PetPhotos/login.html', context=context_dict)


@login_required
def add_pet(request):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results

    form = PetForm()

    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():

            pet = form.save(commit=False)
            pet.owner = request.user

            if 'picture' in request.FILES:
                pet.picture = request.FILES['picture']

            pet.save()

            return redirect('/PetPhotos/')

        else:
            print(form.errors)

    context_dict['form'] = form
    return render(request, 'PetPhotos/add_pet.html', context=context_dict)


@login_required
def add_picture(request):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results

    form = PictureForm()

    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():

            picture = form.save(commit=False)

            picture.creator = request.user

            if 'picture' in request.FILES:
                picture.picture = request.FILES['picture']

            picture.save()

            return redirect('/PetPhotos/')

        else:
            print(form.errors)

    context_dict['form'] = form
    return render(request, 'PetPhotos/add_picture.html', context=context_dict)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('PetPhotos:index'))
  

def view_picture(request, id):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results
    context_dict = {}
    picture = Picture.objects.get(id=id)

    liked = False
    if picture.likes.filter(id=request.user.id).exists():
        liked = True

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.creator = request.user
            comment.picture = picture
            comment.comment = request.POST.get('comment')
            comment.save()
            return HttpResponseRedirect(reverse('PetPhotos:view_picture', args=[str(id)]))
    else:
        comment_form = CommentForm()

    comments = Comment.objects.filter(picture=picture).order_by('-id')
    context_dict['comment_form'] = comment_form
    context_dict['picture'] = picture
    context_dict['likes'] = picture.number_of_likes()
    context_dict['liked'] = liked
    context_dict['comments'] = comments
    return render(request, 'PetPhotos/view_picture.html', context=context_dict)


@login_required
def like_view(request, id):
    picture = get_object_or_404(Picture, id=request.POST.get('post_id'))
    liked = False
    if picture.likes.filter(id=request.user.id).exists():
        picture.likes.remove(request.user)
        liked = False
    else:
        picture.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('PetPhotos:view_picture', args=[str(id)]))


def search_category(request):
    context_dict = {}
    results = Category.objects.all()
    context_dict['results'] = results
    if request.method == "POST":
        searched = request.POST.get('searched')
        categories_sug = Category.objects.filter(name__contains=searched)
        context_dict['searched'] = searched
        context_dict['categories_sug'] = categories_sug
        return render(request, 'PetPhotos/search_category.html', context=context_dict)
    else:
        return render(request, 'PetPhotos/search_category.html', context=context_dict)

def trending(request):
    most_liked = Picture.objects.annotate(max_likes=Max('likes')).order_by('-max_likes')[:3]
    new_pictures = Picture.objects.order_by('-creation_date')[:3]
    new_categories = Category.objects.order_by('-creation_date')[:5]

    context_dict = {}
    context_dict['liked'] = most_liked
    context_dict['newpics'] = new_pictures
    context_dict['cats'] = new_categories

    return render(request, 'PetPhotos/trending.html', context=context_dict)
