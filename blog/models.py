from dateutil import parser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from PIL import Image
from clarifai.rest import ClarifaiApp
from .getGPS import get_lat_lon_dt

app = ClarifaiApp()
model = app.models.get('general-v1.3')
forbidden = ['backlit', 'light', 'no person', 'silhouette', 'sky']

# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=50)

    class Meta:
        ordering = ('tag',)

    def __str__(self):
        return self.tag

class Theme(models.Model):
    """docstring for Subject"""
    """ Subject """
    PUBLIC = 'P'
    PRIVATE = 'V'

    STATUS = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    )
    name = models.CharField(max_length=30)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='themes')
    status = models.CharField(max_length=1, choices=STATUS, default=PUBLIC)
    create_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Content(models.Model):
    """docstring for Content"""
    """ Content """
    file = models.FileField(upload_to='contents/%Y/%m/')
    address = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    taken_dt = models.DateTimeField(blank=True, null=True)
    tag_set = models.ManyToManyField(Tag)
    create_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.id, self.file.url)


class Post(models.Model):
    """docstring for Post"""
    """ 설명 """
    theme = models.ForeignKey(Theme, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField(default=0, blank=True, null=True)
    lng = models.FloatField(default=0, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    create_dt = models.DateTimeField(auto_now_add=True)
    contents = models.ManyToManyField(Content)
    tag_set = models.ManyToManyField(Tag)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='like_user_set',
                                           through='Like')  # post.like_set 으로 접근 가능
    bucket_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='bucket_user_set',
                                           through='Bucket')  # post.bucket_set 으로 접근 가능

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "{} - {}".format(self.id, self.text)

    @property
    def like_count(self):
        return self.like_user_set.count()

    @property
    def bucket_count(self):
        return self.bucket_user_set.count()


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    create_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'post')
        )

class Bucket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buckets')
    post = models.ForeignKey(Post)
    create_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'post')
        )

from os import listdir
from os.path import isfile, join
def file_upload():

    user = get_user_model().objects.get(username='njyoon@naver.com')
    theme = Theme.objects.get(id=6)

    db_path = 'contents/2017/cc'
    mypath = '/Users/happy/Django/simpleMap/media/contents/2017/cc'
    for file in listdir(mypath):
        if isfile(join(mypath, file)):
            fullpath = join(mypath,file)
            db_save_path = join(db_path, file)

            if fullpath != '/Users/happy/Django/simpleMap/media/contents/2017/cc/.DS_Store':
                
                post = Post()
                post.author = user
                post.theme = theme

                post.save()

                content = Content()
                content.file = db_save_path
                image = Image.open(fullpath)

                lat, lng, dt = get_lat_lon_dt(image)
                if lat:
                    content.lat = lat
                    content.lng = lng
                if dt:
                    dt = parser.parse(dt)
                    content.taken_dt = dt

                content.save()
                post.contents.add(content)

                response = model.predict_by_filename(fullpath)
                concepts = response['outputs'][0]['data']['concepts']
                tag_array = []
                for concept in concepts:
                    if concept['value'] > 0.95:
                        if concept['name'] not in forbidden:
                            obj, created = Tag.objects.get_or_create(tag=concept['name'])
                            tag_array.append(obj)
                content.tag_set.set(tag_array)

                post.tag_set.set(tag_array)
                post.lat = lat
                post.lng = lng
                post.save()



# from openpyxl import load_workbook
# import pandas as pd
# def read_person_data():

#     wb = load_workbook('person.xlsx')
#     ws = wb['Sheet']
#     df = pd.DataFrame(ws.values)

#     for index, row in df.iterrows():
#         if index == 0:
#             continue
#         print(row)
#         email = row[0]
#         passwd = row[1]
#         name = row[2]
#         birth = row[3]
#         num = row[4]
#         friends = row[5]

#         user, created = User.objects.get_or_create(username=email, first_name=name, email=email)
#         user.set_password(passwd)
#         # 사진 입력

#         person, created = Person.objects.get_or_create(user=user, birthdate=birth, num=num)

#         if friends:
#             friends = friends.strip()
#             friend_list = friends.split(',')
#             for friend in friend_list:
#                 obj = Person.objects.get(num=friend)
#                 print(obj.user.first_name)
#                 person.friends.add(obj)
#                 obj.friends.add(person)




# from openpyxl import load_workbook
# import pandas as pd
# from django.contrib.auth import get_user_model
# def read_post_data():

#     User = get_user_model()
#     wb = load_workbook('positions.xlsx')
#     ws = wb['Sheet']
#     df = pd.DataFrame(ws.values)

#     for index, row in df.iterrows():
#         if index == 0:
#             continue
#         print(row)
#         name = row[0]
#         address = row[1]
#         lat = row[2]
#         lng = row[3]
#         picture = row[4]
#         user = row[5]

#         user = User.objects.get(id=user)
#         post= Post.objects.create(name=name, address=address, lat=lat,
#                 lng=lng, picture=picture, create_user=user)
#         print(post)