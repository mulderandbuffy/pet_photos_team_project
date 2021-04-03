import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_photos_team_project.settings')
import django
django.setup()
from PetPhotos.models import Pet, Category, Picture, Comment, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone


def populate():

    # USER PROFILES

    users = [
        {'username': 'user1', 'email': 'user1@gmail.com', 'picture': None},
        {'username': 'user2', 'email': 'user2@gmail.com', 'picture': None},
        {'username': 'user3', 'email': 'user3@gmail.com', 'picture': None}
    ]

    for item in users:
        add_user(item["username"], item["email"], item["picture"])
        add_user_profile(User.objects.get(username=item["username"]), item["username"], item["email"], item["picture"])

    # PETS

    user1_animals = [
        {'name': 'Jackie White', 'owner': User.objects.get(username='user1'), 'picture': None, 'about_pet': 'dog'},
        {'name': 'Benny Blue', 'owner': User.objects.get(username='user1'), 'picture': None, 'about_pet': 'cute dog'},
        {'name': 'Ally Red', 'owner': User.objects.get(username='user1'), 'picture': None, 'about_pet': 'cutest of them all'}
    ]

    user2_animals = [
        {'name': 'Bonnie', 'owner': User.objects.get(username='user2'), 'picture': None, 'about_pet': 'cat'},
        {'name': 'Meow', 'owner': User.objects.get(username='user2'), 'picture': None,  'about_pet': 'cute cat'},
        {'name': 'Beck', 'owner': User.objects.get(username='user2'), 'picture': None, 'about_pet': ''}
    ]

    for item in user1_animals:
        add_pet(item["name"], item["owner"], item["picture"], item["about_pet"])

    for item in user2_animals:
        add_pet(item["name"], item["owner"], item["picture"], item["about_pet"])

    # PICTURES

    dog_pics = [
        {'rating': 10, 'creator': User.objects.get(username='user2'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 15, 'creator': User.objects.get(username='user1'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 21, 'creator': User.objects.get(username='user3'), 'picture': None, 'creation_date': timezone.now()}
    ]

    cat_pics = [
        {'rating': 100, 'creator': User.objects.get(username='user2'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 1, 'creator': User.objects.get(username='user1'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 0, 'creator': User.objects.get(username='user3'), 'picture': None, 'creation_date': timezone.now()}
    ]

    # CATEGORIES

    categories = {
        'cats': {'pics': cat_pics, 'creation_date': timezone.now()},
        'dogs': {'pics': dog_pics, 'creation_date': timezone.now()}
    }

    for cat, cat_data in categories.items():

        c = add_cat(name=cat, creation_date=cat_data['creation_date'])

        for p in cat_data['pics']:
            add_pic(rating=p['rating'], creator=p['creator'], category=c, picture=p['picture'],
                    creation_date=p['creation_date'])

    # COMMENTS

    comments = [
        {'comment': 'i like this picture', 'creator': User.objects.get(username='user1'),
         'picture': Picture.objects.get(id=1), 'creation_date': timezone.now()},
        {'comment': 'nice dog', 'creator': User.objects.get(username='user2'),
         'picture': Picture.objects.get(id=2), 'creation_date': timezone.now()},
        {'comment': 'okay', 'creator': User.objects.get(username='user1'),
         'picture': Picture.objects.get(id=2), 'creation_date': timezone.now()}
    ]

    for item in comments:
        add_com(comment=item['comment'], creator=item['creator'], picture=item['picture'],
                creation_date=item['creation_date'])


def add_pet(name, owner, picture, about_pet):
    p = Pet.objects.get_or_create(name=name, owner=owner)[0]
    p.picture = picture
    p.about_pet = about_pet
    return p


def add_cat(name, creation_date):
    c = Category.objects.get_or_create(name=name)[0]
    c.creation_date = creation_date
    c.save()
    return c


def add_pic(creator, category, picture, creation_date, rating=0):
    p = Picture.objects.get_or_create(creator=creator, category=category, picture=picture)[0]
    p.rating = rating
    p.creation_date = creation_date
    p.save()
    return p


def add_com(comment, creator, picture, creation_date):
    c = Comment.objects.get_or_create(comment=comment, creator=creator, picture=picture)[0]
    c.creation_date = creation_date
    c.save()
    return c


def add_user(username, email, picture):
    u = User.objects.get_or_create(username=username)[0]
    u.email = email
    u.picture = picture
    return u


def add_user_profile(user, username, email, picture):
    u = UserProfile.objects.get_or_create(user=user, username=username, email=email, picture=picture)[0]
    u.save()
    return u


if __name__ == '__main__':
    print('Starting PetPhotos population script...')
    populate()
