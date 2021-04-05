import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_photos_team_project.settings')
import django
django.setup()
from PetPhotos.models import Pet, Category, Picture, Comment
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

    # PETS

    user1_animals = [
        {'name': 'Thor', 'owner': User.objects.get(username='user1'), 'picture': 'thor.jpg'},
        {'name': 'Buster', 'owner': User.objects.get(username='user1'), 'picture': 'dog4.jpg'},
        {'name': 'Smudge', 'owner': User.objects.get(username='user1'), 'picture': 'cat5.jpg'}
    ]

    user2_animals = [
        {'name': 'Bonnie', 'owner': User.objects.get(username='user2'), 'picture': 'horse.jpg'},
        {'name': 'Meow', 'owner': User.objects.get(username='user2'), 'picture': 'cat4.jpg'},
        {'name': 'Beck', 'owner': User.objects.get(username='user2'),  'picture': 'dog5.jpg'}
    ]

    user4_animals = [
        {'name': 'Molly', 'owner': User.objects.get(username='user4'), 'picture': 'molly.jpg'},
        {'name': 'Lilly', 'owner': User.objects.get(username='user4'), 'picture': 'larkin.jpg'},
        {'name': 'Oreo', 'owner': User.objects.get(username='user4'),  'picture': 'oreo.jpg'}
    ]

    user5_animals = [
        {'name': 'Mickey', 'owner': User.objects.get(username='user5'), 'picture':'cat2.jpg'},
        {'name': 'Buddy', 'owner': User.objects.get(username='user5'), 'picture': 'blacklab.jpg'},
        {'name': 'Megatron', 'owner': User.objects.get(username='user5'),  'picture': 'birbagain.jpg'}
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
        {'creator': User.objects.get(username='user2'), 'picture': 'fluffydog.jpg', 'creation_date': timezone.now()},
        {'creator': User.objects.get(username='user1'), 'picture': 'dog2.jpg', 'creation_date': timezone.now()},
        {'creator': User.objects.get(username='user3'), 'picture': 'dog3.jpg', 'creation_date': timezone.now()}
    ]

    cat_pics = [
        {'creator': User.objects.get(username='user2'), 'picture': 'void.jpg', 'creation_date': timezone.now()},
        {'creator': User.objects.get(username='user1'), 'picture': 'cat2.jpg', 'creation_date': timezone.now()},
        {'creator': User.objects.get(username='user3'), 'picture': 'cat3.jpg', 'creation_date': timezone.now()}
    ]

    bird_pics = [
        {'creator': User.objects.get(username='user4'), 'picture': 'budgie.jpg', 'creation_date': timezone.now()},
        {'creator': User.objects.get(username='user5'), 'picture': 'birb2.jpg', 'creation_date': timezone.now()},
        {'creator': User.objects.get(username='user6'), 'picture': 'birbagain.jpg', 'creation_date': timezone.now()}
    ]

    # CATEGORIES

    categories = {
        'cats': {'pics': cat_pics, 'creation_date': timezone.now()},
        'dogs': {'pics': dog_pics, 'creation_date': timezone.now()},
        'birds': {'pics': bird_pics, 'creation_date': timezone.now()}
    }

    for cat, cat_data in categories.items():

        c = add_cat(name=cat, creation_date=cat_data['creation_date'])

        for p in cat_data['pics']:
            add_pic(creator=p['creator'], category=c, picture=p['picture'],
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

    # LIKES

    set1 = [User.objects.get(username='user4'), User.objects.get(username='user1'), User.objects.get(username='user2')]
    set2 = [User.objects.get(username='user2'), User.objects.get(username='user1')]
    set3 = [User.objects.get(username='user6'), User.objects.get(username='user5'), User.objects.get(username='user2')]

    for pic in Picture.objects.all():
        if pic.id == 3 or pic.id == 2:
            for user in set1:
                pic.likes.add(user)
        elif pic.id == 1 or pic.id == 7:
            for user in set2:
                pic.likes.add(user)
        elif pic.id == 5:
            for user in set3:
                pic.likes.add(user)


def add_pet(name, owner, picture):
    p = Pet.objects.get_or_create(name=name, owner=owner)[0]
    p.picture.save('add_pet.jpg', File(open('media/population_files/' + str(picture), 'rb')))
    return p


def add_cat(name, creation_date):
    c = Category.objects.get_or_create(name=name)[0]
    c.creation_date = creation_date
    c.save()
    return c


def add_pic(creator, category, picture, creation_date, rating=0):
    p = Picture.objects.get_or_create(creator=creator, category=category)[0]
    p.picture.save('add_pic.jpg', File(open('media/population_files/' + str(picture), 'rb')))
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


if __name__ == '__main__':
    print('Starting PetPhotos population script...')
    populate()
