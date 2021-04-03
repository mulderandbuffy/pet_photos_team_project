from django.shortcuts import render, redirect
from django.http import HttpResponse
from PetPhotos.models import Category
from PetPhotos.forms import CategoryForm, UserForm, UserProfileForm
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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


#@login_required    add back when login done
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

#@login_required
class LikePictureView(View):
    #@method_decorator(login_required)
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
          profile = profile_form.save(commit= False)
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
 
   return render(request,  'PetPhotos/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered })

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
def restricted(request):
   return HttpResponse("Enjoy uploading pictures of your pets!")


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('PetPhotos:index'))
