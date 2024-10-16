from orm.models import Model
from orm.fields import IntegerField, StringField, BooleanField

class Users(Model):
    id = IntegerField()
    email = StringField()
    username = StringField()
    password = StringField()
    biography = StringField()
    is_active = BooleanField()


class Followers(Model):
    id = IntegerField()
    user_id = IntegerField()
    follower_id = IntegerField()


class Posts(Model):
    id = IntegerField()
    user_id = IntegerField()
    content = StringField()
    image_url = StringField()


class Likes(Model):
    id = IntegerField()
    post_id = IntegerField()
    user_id = IntegerField()


class Comments(Model):
    id = IntegerField()
    post_id = IntegerField()
    user_id = IntegerField()
    comment = StringField()