from django.shortcuts import render, redirect
from django.http import HttpResponse
from PetPhotos.models import Category, Picture, UserProfile, Pet
from PetPhotos.forms import CategoryForm, UserForm, UserProfileForm, PetForm, PictureForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User

def index(request):
    response = render(request, 'PetPhotos/index.html')
    return response


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)

        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None

        pictures = Picture.objects.filter(category=category)
        context_dict['pictures'] = pictures
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pictures'] = None

    return render(request, 'PetPhotos/category.html', context=context_dict)


def categories(request):
    context_dict = {}
    show_categories = Category.objects.all()
    context_dict['categories'] = show_categories

    return render(request, 'PetPhotos/categories.html', context=context_dict)


def user_profiles(request):
    context_dict = {}
    profiles = UserProfile.objects.order_by('username')
    context_dict['profiles'] = profiles

    return render(request, 'PetPhotos/user_profiles.html', context=context_dict)


def user_profile(request, username):
    context_dict = {}
    user = UserProfile.objects.get(username=username)
    pets = Pet.objects.filter(owner=User.objects.get(username=user.username))
    context_dict['user'] = user
    context_dict['pets'] = pets
    return render(request, 'PetPhotos/user_profile.html', context=context_dict)


def viewpetprofile(request, pet_slug):
    context_dict = {}
    pet = Pet.objects.get(slug=pet_slug)
    context_dict['pet'] = pet
    return render(request, 'PetPhotos/viewpetprofile.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/PetPhotos/')

        else:
            print(form.errors)

    return render(request, 'PetPhotos/add_category.html', {'form': form})


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
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'PetPhotos/register.html', context={'user_form': user_form, 'profile_form': profile_form,
                                                               'registered': registered})


def user_login(request):
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
        return render(request, 'PetPhotos/login.html')


@login_required
def add_pet(request):
    form = PetForm()

    if request.method == 'POST':
        form = PetForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/PetPhotos/')

        else:
            print(form.errors)

    return render(request, 'PetPhotos/add_pet.html', {'form': form})


@login_required
def add_picture(request):
    form = PictureForm()

    if request.method == 'POST':
        form = PictureForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/PetPhotos/')

        else:
            print(form.errors)

    return render(request, 'PetPhotos/add_picture.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('PetPhotos:index'))
