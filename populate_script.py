import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_photos_team_project.settings')
import django
django.setup()
from PetPhotos.models import Pet, Category, Picture, Comment, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File


def populate():

    # USER PROFILES

    users = [
        {'username': 'user1', 'email': 'user1@gmail.com', 'picture': None},
        {'username': 'user2', 'email': 'user2@gmail.com', 'picture': None},
        {'username': 'user3', 'email': 'user3@gmail.com', 'picture': None},
        {'username': 'user4', 'email': 'user4@gmail.com', 'picture': None},
        {'username': 'user5', 'email': 'user5@gmail.com', 'picture': None},
        {'username': 'user6', 'email': 'user6@gmail.com', 'picture': None}
    ]

    for item in users:
        add_user(item["username"], item["email"], item["picture"])
        add_user_profile(User.objects.get(username=item["username"]), item["username"], item["email"], item["picture"])

    # PETS

    user1_animals = [
        {'name': 'Jackie White', 'owner': User.objects.get(username='user1'), 'picture': None},
        {'name': 'Benny Blue', 'owner': User.objects.get(username='user1'), 'picture': None},
        {'name': 'Ally Red', 'owner': User.objects.get(username='user1'), 'picture': None}
    ]

    user2_animals = [
        {'name': 'Bonnie', 'owner': User.objects.get(username='user2'), 'picture': None},
        {'name': 'Meow', 'owner': User.objects.get(username='user2'), 'picture': None},
        {'name': 'Beck', 'owner': User.objects.get(username='user2'),  'picture': None}
    ]

    user4_animals = [
        {'name': 'Billy', 'owner': User.objects.get(username='user4'), 'picture': None},
        {'name': 'Lilly', 'owner': User.objects.get(username='user4'), 'picture': None},
        {'name': 'Minnie', 'owner': User.objects.get(username='user4'),  'picture': None}
    ]

    user5_animals = [
        {'name': 'Micky', 'owner': User.objects.get(username='user5'), 'picture': None},
        {'name': 'Buddy', 'owner': User.objects.get(username='user5'), 'picture': None},
        {'name': 'I ran out of name ideas', 'owner': User.objects.get(username='user5'),  'picture': None}
    ]
    for item in user1_animals:
        add_pet(item["name"], item["owner"], item["picture"])

    for item in user2_animals:
        add_pet(item["name"], item["owner"], item["picture"])

    for item in user4_animals:
        add_pet(item["name"], item["owner"], item["picture"])

    for item in user5_animals:
        add_pet(item["name"], item["owner"], item["picture"])

    # PICTURES

    dog_pics = [
        {'rating': 10, 'creator': User.objects.get(username='user2'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 15, 'creator': User.objects.get(username='user1'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 21, 'creator': User.objects.get(username='user3'), 'picture': None, 'creation_date': timezone.now()}
    ]

    cat_pics = [
        {'rating': 101, 'creator': User.objects.get(username='user2'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 1, 'creator': User.objects.get(username='user1'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 0, 'creator': User.objects.get(username='user3'), 'picture': None, 'creation_date': timezone.now()}
    ]

    mouse_pics = [
        {'rating': 13, 'creator': User.objects.get(username='user4'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 4, 'creator': User.objects.get(username='user4'), 'picture': None, 'creation_date': timezone.now()},
        {'rating': 0, 'creator': User.objects.get(username='user6'), 'picture': None, 'creation_date': timezone.now()}
    ]

    # CATEGORIES

    categories = {
        'cats': {'pics': cat_pics, 'creation_date': timezone.now()},
        'dogs': {'pics': dog_pics, 'creation_date': timezone.now()},
        'mice': {'pics': mouse_pics, 'creation_date': timezone.now()}
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
        {'comment': 'thanks', 'creator': User.objects.get(username='user1'),
         'picture': Picture.objects.get(id=2), 'creation_date': timezone.now()},
        {'comment': 'Looks just like mine!', 'creator': User.objects.get(username='user1'),
         'picture': Picture.objects.get(id=7), 'creation_date': timezone.now()},
        {'comment': 'nice picture', 'creator': User.objects.get(username='user5'),
         'picture': Picture.objects.get(id=5), 'creation_date': timezone.now()},
        {'comment': 'where is this?', 'creator': User.objects.get(username='user5'),
         'picture': Picture.objects.get(id=5), 'creation_date': timezone.now()}
    ]

    for item in comments:
        add_com(comment=item['comment'], creator=item['creator'], picture=item['picture'],
                creation_date=item['creation_date'])


def add_pet(name, owner, picture):
    p = Pet.objects.get_or_create(name=name, owner=owner)[0]
    p.picture.save('add_pet.jpg', File(open('media/population_files/test.jpg', 'rb')))
    return p


def add_cat(name, creation_date):
    c = Category.objects.get_or_create(name=name)[0]
    c.creation_date = creation_date
    c.save()
    return c


def add_pic(creator, category, picture, creation_date, rating=0):
    p = Picture.objects.get_or_create(creator=creator, category=category)[0]
    p.picture.save('add_pic.jpg', File(open('media/population_files/bueno.jpg', 'rb')))
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
    u.save()
    return u


def add_user_profile(user, username, email, picture):
    u = UserProfile.objects.get_or_create(user=user, username=username, email=email, picture=picture)[0]
    u.picture.save('add_user.jpg', File(open('media/population_files/dog.jpg', 'rb')))
    u.save()
    return u


if __name__ == '__main__':
    print('Starting PetPhotos population script...')
    populate()
