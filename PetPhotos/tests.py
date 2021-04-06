from django.test import TestCase, SimpleTestCase
from PetPhotos.models import Pet, Category, Picture
from django.urls import reverse, resolve
from PetPhotos.views import index, user_profiles, user_profile, categories, show_category, add_category, add_pet, add_picture, view_pet_profile, view_picture, search_category, like_view, del_comment, register, user_login, user_logout, trending

# Models Tests
class CategoryMethodTests(TestCase):
    def test_slug_creation(self):
        # Tests that a slug is properly constructed
        category = Category(name='Random Category String')
        category.save()
        self.assertEqual(category.slug, 'random-category-string')


class PetMethodTests(TestCase):
    def test_slug_creation(self):
        # Tests that a slug is properly constructed
        pet = Pet(name='Random Category String')
        pet.save()
        self.assertEqual(pet.slug, 'random-category-string')


class PictureMethodTests(TestCase):
    def test_ensure_likes_are_positive(self):
        # Tests that number of likes of a Picture are 0 or greater.
        picture = Picture(likes=-1)
        self.assertEqual((picture.number_of_likes() >= 0), True)

# Urls Tests
class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_user_profiles_url_is_resolved(self):
        url = reverse('user_profiles')
        self.assertEquals(resolve(url).func, user_profiles)

    def test_user_profile_url_is_resolved(self):
        url = reverse('user_profile')
        self.assertEquals(resolve(url).func, user_profile)

    def test_categories_url_is_resolved(self):
        url = reverse('categories')
        self.assertEquals(resolve(url).func, categories)

    def test_show_category_url_is_resolved(self):
        url = reverse('show_category', args=['test-slug'])
        self.assertEquals(resolve(url).func, show_category)

    def test_add_category_url_is_resolved(self):
        url = reverse('add_category')
        self.assertEquals(resolve(url).func, add_category)

    def test_add_pet_url_is_resolved(self):
        url = reverse('add_pet')
        self.assertEquals(resolve(url).func, add_pet)

    def test_add_picture_url_is_resolved(self):
        url = reverse('add_picture')
        self.assertEquals(resolve(url).func, add_picture)

    def test_view_pet_profile_url_is_resolved(self):
        url = reverse('view_pet_profile', args=['test-slug'])
        self.assertEquals(resolve(url).func, view_pet_profile)

    def test_view_picture_url_is_resolved(self):
        url = reverse('view_picture', args=['test-slug'])
        self.assertEquals(resolve(url).func, view_picture)

    def test_search_category_url_is_resolved(self):
        url = reverse('search_category')
        self.assertEquals(resolve(url).func, search_category)

    def test_like_post_url_is_resolved(self):
        url = reverse('like_post', args=['test-slug'])
        self.assertEquals(resolve(url).func, like_view)

    def test_del_comment_url_is_resolved(self):
        url = reverse('del_comment', args=['test-slug'])
        self.assertEquals(resolve(url).func, del_comment)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, user_login)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, user_logout)

    def test_trending_url_is_resolved(self):
        url = reverse('trending')
        self.assertEquals(resolve(url).func, trending)
# Views Tests


