from django.test import TestCase, SimpleTestCase, Client, TransactionTestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PetPhotos.models import *
from django.urls import reverse, resolve
from PetPhotos.views import *
from PetPhotos.models import Pet, UserProfile, Category, Picture, Comment
from PetPhotos.forms import CategoryForm, PetForm, PictureForm, UserForm, CommentForm

'''
The following tests were included for coverage but do not operate correctly and cause errors:

test_add_picture_GET, test_trending_GET, test_user_profile_GET, test_view_picture_GET

The following tests were included for coverage but do not operate correctly and cause failures:

test_pet_form_valid_data, test_picture_form_valid_data, test_add_category_GET, test_add_pet_GET
'''
# Models Tests
class TestModels(TestCase):
    def setUp(self):
        #datetimefield?
        self.category1 = Category.objects.create(name='Category 1')
    #Alternative to test_slug_creation
    def test_category_is_assigned_slug(self):
        self.assertEquals(self.category1.slug, 'category-1')


class CategoryMethodTests(TestCase):
    def test_slug_creation(self):
        # Tests that a slug is properly constructed
        category = Category(name='Random Category String')
        category.save()
        self.assertEqual(category.slug, 'random-category-string')


class PetMethodTests(TestCase):
    def test_slug_creation(self):
        # Tests that a slug is properly constructed
        pet = Pet(name='Random Category String', owner=User.objects.create(username='petuser'))
        pet.save()
        self.assertEqual(pet.slug, 'petuser-random-category-string')


class PictureMethodTests(TestCase):
    def test_ensure_likes_are_positive(self):
        # Tests that number of likes of a Picture are 0 or greater.
        picture =  Picture.objects.create(category=Category.objects.create(name='likes-category'), creator=User.objects.create(username='likesuser'))
        like = picture.likes.create()
        self.assertEqual((picture.number_of_likes() >= 0), True)

# Urls Tests
class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('PetPhotos:index')
        self.assertEquals(resolve(url).func, index)

    def test_user_profiles_url_is_resolved(self):
        url = reverse('PetPhotos:user_profiles')
        self.assertEquals(resolve(url).func, user_profiles)

    def test_user_profile_url_is_resolved(self):
        url = reverse('PetPhotos:user_profile', args=['user1'])
        self.assertEquals(resolve(url).func, user_profile)

    def test_categories_url_is_resolved(self):
        url = reverse('PetPhotos:categories')
        self.assertEquals(resolve(url).func, categories)

    def test_show_category_url_is_resolved(self):
        url = reverse('PetPhotos:show_category', args=['test-slug'])
        self.assertEquals(resolve(url).func, show_category)

    def test_add_category_url_is_resolved(self):
        url = reverse('PetPhotos:add_category')
        self.assertEquals(resolve(url).func, add_category)

    def test_add_pet_url_is_resolved(self):
        url = reverse('PetPhotos:add_pet')
        self.assertEquals(resolve(url).func, add_pet)

    def test_add_picture_url_is_resolved(self):
        url = reverse('PetPhotos:add_picture')
        self.assertEquals(resolve(url).func, add_picture)

    def test_view_pet_profile_url_is_resolved(self):
        url = reverse('PetPhotos:view_pet_profile', args=['test-slug'])
        self.assertEquals(resolve(url).func, view_pet_profile)

    #Not sure if this still works for ID
    def test_view_picture_url_is_resolved(self):
        url = reverse('PetPhotos:view_picture', args=['test-slug'])
        self.assertEquals(resolve(url).func, view_picture)

    def test_search_category_url_is_resolved(self):
        url = reverse('PetPhotos:search_category')
        self.assertEquals(resolve(url).func, search_category)

    # Not sure if this still works for ID
    def test_like_post_url_is_resolved(self):
        url = reverse('PetPhotos:like_post', args=['test-slug'])
        self.assertEquals(resolve(url).func, like_view)

    # Not sure if this still works for ID
    def test_del_comment_url_is_resolved(self):
        url = reverse('PetPhotos:del_comment', args=['test-slug', '1'])
        self.assertEquals(resolve(url).func, del_comment)

    def test_register_url_is_resolved(self):
        url = reverse('PetPhotos:register')
        self.assertEquals(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse('PetPhotos:login')
        self.assertEquals(resolve(url).func, user_login)

    def test_logout_url_is_resolved(self):
        url = reverse('PetPhotos:logout')
        self.assertEquals(resolve(url).func, user_logout)

    def test_trending_url_is_resolved(self):
        url = reverse('PetPhotos:trending')
        self.assertEquals(resolve(url).func, trending)

# Views Tests

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        #datetimefield?
        self.category1 = Category.objects.create(name='category1')
        #user and email fields?
        self.user1 = User.objects.create(username='user1')
        #owner and picture fields?
        self.pet1 = Pet.objects.create(name='pet1', owner=User.objects.get(username='user1'))
        #INCOMPLETE - WHAT TO DO FOR FIELDS?
        self.picture1 = Picture.objects.create(category=Category.objects.create(name='picture-category'), creator=User.objects.get(username='user1'))
        self.comment1 = Comment.objects.create(picture=Picture.objects.get(id=1), creator=User.objects.get(username='user1'))

        self.index_url = reverse('PetPhotos:index')
        self.show_category_url = reverse('PetPhotos:show_category', args=['category1'])
        self.categories_url = reverse('PetPhotos:categories')
        #2nd param required?
        self.user_profile_url = reverse('PetPhotos:user_profile', args=['user1'])
        self.view_pet_profile_url = reverse('PetPhotos:view_pet_profile', args=['pet1'])
        self.add_category_url = reverse('PetPhotos:add_category')
        self.register_url = reverse('PetPhotos:register')
        self.user_login_url = reverse('PetPhotos:login')
        self.add_pet_url = reverse('PetPhotos:add_pet')
        self.add_picture_url = reverse('PetPhotos:add_picture')
        self.user_logout_url = reverse('PetPhotos:logout')
        #How to add to args??
        self.view_picture_url = reverse('PetPhotos:view_picture', args=['picture1'])
        self.search_category_url = reverse('PetPhotos:search_category')
        self.trending_url = reverse('PetPhotos:trending')
        self.like_view_url = reverse('PetPhotos:like_post', args=['picture1'])
        #How to add to args??
        self.del_comment_url = reverse('PetPhotos:del_comment', args=['picture1', '1'])


#Test for Successful response 200 OR 302 if the page is supposed to redirect you

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/index.html')

    def test_show_category_GET(self):
        response = self.client.get(self.show_category_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/category.html')

    def test_categories_GET(self):
        response = self.client.get(self.categories_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/categories.html')

    def test_user_profile_GET(self):
        response = self.client.get(self.user_profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/user_profile.html')

    def test_view_pet_profile_GET(self):
        response = self.client.get(self.view_pet_profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/view_pet_profile.html')

    def test_add_category_GET(self):
        response = self.client.get(self.add_category_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/add_category.html')

    #INCOMPLETE
    def test_add_category_POST(self):
        #datetimefield
        response = self.client.post(self.add_category_url, {'name': 'category2'})
        #redirect is response code 302
        self.assertEquals(response.status_code, 302)
        #self.assertEquals()   #UNFINISHED MEANT TO CHECK CATEGORY IS ADDED

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/register.html')
    # POST

    def test_user_login_GET(self):
        response = self.client.get(self.user_login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/login.html')

    # POST

    def test_add_pet_GET(self):
        response = self.client.get(self.add_pet_url)
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'PetPhotos/add_pet.html')

    #POST

    def test_add_picture_GET(self):
        response = self.client.get(self.add_picture_url)
        self.picture = SimpleUploadedFile(name='dog2.jpg', content=open('static/population_files', 'rb').read(), content_type='image/jpeg')
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'PetPhotos/add_picture.html')
    #POST

    def test_user_logout_GET(self):
        response = self.client.get(self.user_logout_url)
        self.assertEquals(response.status_code, 302)
        #exclude?
        #No template here

    def test_view_picture_GET(self):
        response = self.client.get(self.view_picture_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/view_picture.html')
    #POST

    def test_search_category_GET(self):
        response = self.client.get(self.search_category_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/search_category.html')

    def test_trending_GET(self):
        response = self.client.get(self.trending_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'PetPhotos/trending.html')

    def test_like_view_GET(self):
        response = self.client.get(self.like_view_url)
        self.assertEquals(response.status_code, 302)
        #No template
    #POST

    def test_del_comment_GET(self):
        response = self.client.get(self.del_comment_url)
        self.assertEquals(response.status_code, 302)
        #No template
    #DELETE

class TestForms(TestCase):
    def test_category_form_valid_data(self):
        #datetimefield?
        form = CategoryForm(data={'name': 'TestCategory'})
        self.assertTrue(form.is_valid())

    def test_category_form_no_data(self):
        form = CategoryForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_pet_form_valid_data(self):
        someperson = User.objects.create()
        form = PetForm(data={'name': 'Benji', 'owner': 'someperson'})
        self.assertTrue(form.is_valid())

    def test_pet_form_no_data(self):
        form = PetForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_picture_form_valid_data(self):
        # datetimefield?
        self.category2 = Category.objects.create(name='Category 2')
        self.someperson = User.objects.create(username='someperson')
        # datetimefield?
        form = PictureForm(data={'category': 'category2', 'creator': 'someperson'})
        self.assertTrue(form.is_valid())

    def test_picture_form_no_data(self):
        form = PictureForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_user_form_valid_data(self):
        form = UserForm(data={'password': 'someString', 'username': 'name'})
        self.assertTrue(form.is_valid())

    def test_user_form_no_data(self):
        form = UserForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_comment_form_valid_data(self):
        # datetimefield?
        form = CommentForm(data={'comment': 'someCommentString'})
        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)




