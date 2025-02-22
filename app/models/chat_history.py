from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator
import datetime
import uuid
from tortoise.functions import Max

class ChatHistory(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)  # ✅ Primary Key as UUID
    int_id = fields.IntField(unique=True, index=True)  # ✅ Auto-incremented integer
    user_id = fields.UUIDField(null=True)  # ✅ Optional user ID
    role = fields.CharField(max_length=20, null=True)  # ✅ Optional user role
    model_name = fields.CharField(max_length=50)
    prompt = fields.TextField()
    response = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_history"

    async def save(self, *args, **kwargs):
        """
        Auto-generate int_id before saving, ensuring sequential order.
        """
        if self.int_id is None:  # ✅ Only set if not already assigned
            last_chat = await ChatHistory.all().order_by("-int_id").first()  # ✅ Fetch highest int_id

            if last_chat and last_chat.int_id:
                self.int_id = last_chat.int_id + 1  # ✅ Increment from last ID
            else:
                self.int_id = 1  # ✅ Default to 1 if no records exist

        await super().save(*args, **kwargs)

chat_history_pydantic = pydantic_model_creator(
    ChatHistory, name='ChatHistory', exclude=('created_at'))