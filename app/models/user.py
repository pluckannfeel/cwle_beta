from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class User(Model):
    id = fields.UUIDField(pk=True)  # Primary key
    first_name = fields.CharField(max_length=128, null=False)
    last_name = fields.CharField(max_length=128, null=False)
    job = fields.CharField(max_length=128, null=True)
    introduction = fields.TextField(null=True)
    email = fields.CharField(max_length=255, unique=True, null=True)
    hashed_password = fields.CharField(max_length=255, null=True)
    google_id = fields.CharField(max_length=255, unique=True, null=True)
    apple_id = fields.CharField(max_length=255, unique=True, null=True)
    line_id = fields.CharField(max_length=255, unique=True, null=True)
    is_verified = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

class UserAffair(Model):
    id = fields.UUIDField(pk=True)  # Primary key
    user = fields.ForeignKeyField('models.User', related_name='user_goals')
    likes = fields.IntField(default=0)
    courses = fields.TextField(null=True) # JSON field [ { "course_id": "uuid"} , { "course_id": "uuid"} ]
    goal_count = fields.TextField(null=True) # JSON field [ { goal: "pages", count: 10 }, { goal: "words", count: 1000 }, { goal: "minutes", count: 10 }, { goal: "questions", count: 10 } ] 
    goal_set = fields.TextField(null=True) # JSON field [ { goal: "pages", set: 10 }, { goal: "words", set: 1000 }, { goal: "minutes", set: 10 }, { goal: "questions", set: 10 } ]  
    friendlist = fields.TextField(null=True) # JSON field [ { "user_id": "uuid"} , { "user_id": "uuid"} ]
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_affairs"

User_Pydantic = pydantic_model_creator(User, name='User')

UserAffair_Pydantic = pydantic_model_creator(UserAffair, name='UserAffair')
