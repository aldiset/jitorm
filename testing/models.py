from orm.models import Model
from orm.fields import AutoField, IntegerField, StringField

class Users(Model):
    id = AutoField()
    username = StringField()
    email = StringField()
    password = StringField()
    biography = StringField()


class Followers(Model):
    id = AutoField()
    user_id = IntegerField()
    follower_id = IntegerField()


class Posts(Model):
    id = AutoField()
    user_id = IntegerField()
    content = StringField()
    image_url = StringField()


class Likes(Model):
    id = AutoField()
    post_id = IntegerField()
    user_id = IntegerField()


class Comments(Model):
    id = AutoField()
    post_id = IntegerField()
    user_id = IntegerField()
    comment = StringField()