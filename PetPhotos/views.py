from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from PetPhotos.models import Category, Picture, Pet, Comment
from PetPhotos.forms import CategoryForm, UserForm, PetForm, PictureForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User


"""
    index view displays the "Home Page"
"""


def index(request):
    context_dict = {'results': Category.objects.all()}

    return render(request, 'PetPhotos/index.html', context=context_dict)


"""
    show_category view displays a category name and all the pictures related to that particular category
"""


def show_category(request, category_name_slug):
    context_dict = {'results': Category.objects.all()}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pictures = Picture.objects.filter(category=category)
        context_dict['pictures'] = pictures
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pictures'] = None

    return render(request, 'PetPhotos/category.html', context=context_dict)


"""
    categories view displays a list of alphabetically ordered categories
"""


def categories(request):
    context_dict = {'results': Category.objects.all(), 'categories': Category.objects.order_by('name')}

    return render(request, 'PetPhotos/categories.html', context=context_dict)


"""
    user_profiles view displays a list of alphabetically ordered user profiles
"""


def user_profiles(request):
    context_dict = {'results': Category.objects.all(), 'profiles': User.objects.order_by('username')}

    return render(request, 'PetPhotos/user_profiles.html', context=context_dict)


"""
    user_profile view shows a profile of a particular user
"""


def user_profile(request, username):
    context_dict = {'results': Category.objects.all()}

    try:
        user = User.objects.get(username=username)
        pets = Pet.objects.filter(owner=User.objects.get(username=user.username))
        context_dict['user'] = user
        context_dict['pets'] = pets

    except User.DoesNotExist:
        context_dict['user'] = None
        context_dict['pets'] = None

    return render(request, 'PetPhotos/user_profile.html', context=context_dict)


"""
    view_pet_profile view serves as a page to view a pet profile of a particular user
"""


def view_pet_profile(request, pet_slug):
    context_dict = {'results': Category.objects.all()}

    try:
        context_dict['pet'] = Pet.objects.get(slug=pet_slug)

    except Pet.DoesNotExist:
        context_dict['pet'] = None

    return render(request, 'PetPhotos/view_pet_profile.html', context=context_dict)


"""
    add_category view serves as a page where user can add a category
"""


@login_required
def add_category(request):
    context_dict = {'results': Category.objects.all()}

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


"""
    register view serves as a page where user can register
"""


def register(request):
    context_dict = {'results': Category.objects.all()}

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect(reverse('PetPhotos:index'))
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    context_dict['user_form'] = user_form

    return render(request, 'PetPhotos/register.html', context=context_dict)


"""
    user_login view serves as a page where user can log in
"""


def user_login(request):
    context_dict = {'results': Category.objects.all()}

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


"""
    add_pet view is a page where you can as an owner add a pet to your collection of pets and the reference to 
    the owner for the owner field in the Pet model is essentially a request for the logged-in user
"""


@login_required
def add_pet(request):
    context_dict = {'results': Category.objects.all()}

    form = PetForm()

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)

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


"""
    add_picture view is a page where you can add an animal picture to a particular category and the reference to 
    the creator for the creator field in the Picture model is essentially a request for the logged-in user
"""


@login_required
def add_picture(request):
    context_dict = {'results': Category.objects.all()}

    form = PictureForm()

    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)

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


"""
    view_picture view is a page where you can see a particular animal from a particular category, its comments, like 
    button, and has a part (form) where a logged in user can add a comment
"""


def view_picture(request, id):
    context_dict = {'results': Category.objects.all()}

    try:
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

        context_dict['comment_form'] = comment_form
        context_dict['picture'] = picture
        context_dict['likes'] = picture.number_of_likes()
        context_dict['liked'] = liked
        context_dict['comments'] = Comment.objects.filter(picture=picture).order_by('-id')

    except Picture.DoesNotExist:
        context_dict['picture'] = None
        context_dict['comment_form'] = None
        context_dict['picture'] = None
        context_dict['likes'] = None
        context_dict['liked'] = None
        context_dict['comments'] = None

    return render(request, 'PetPhotos/view_picture.html', context=context_dict)


"""
    search_category view takes as an input the searched string from the search bar and displays all the categories that 
    contain the string anywhere. For instance, if we search for "sh" the list would display "shellfish" as well as 
    "jellyfish" if they both were in the category list.
"""


def search_category(request):
    context_dict = {'results': Category.objects.all()}

    if request.method == "POST":
        searched = request.POST.get('searched')
        context_dict['searched'] = searched
        context_dict['categories_sug'] = Category.objects.filter(name__contains=searched)
        return render(request, 'PetPhotos/search_category.html', context=context_dict)

    else:
        return render(request, 'PetPhotos/search_category.html', context=context_dict)


"""
    trending view displays 5 most liked pictures, 5 most recent pictures, and 5 most recent categories
"""


def trending(request):
    context_dict = {'results': Category.objects.all(),
                    'liked': Picture.objects.annotate(q_count=Count('likes')).order_by('-q_count')[:5],
                    'newpics': Picture.objects.order_by('-creation_date')[:5],
                    'cats': Category.objects.order_by('-creation_date')[:5]}

    return render(request, 'PetPhotos/trending.html', context=context_dict)


"""
    like_view view is a like button that also takes into account whether the user already liked the button, so he can 
    unlike the picture
"""


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


"""
    del_comment view is a delete button that is displayed next to every comment of a logged-in user, so he can delete
    the comment
"""


@login_required
def del_comment(request, pic_id, com_id):
    Comment.objects.filter(id=com_id).delete()
    return HttpResponseRedirect(reverse('PetPhotos:view_picture', args=[str(pic_id)]))
