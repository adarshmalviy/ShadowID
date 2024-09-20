from tortoise import fields, models
from uuid import uuid4
import hashlib


class User(models.Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    anonymous_identifier = fields.CharField(max_length=256)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_login = fields.DatetimeField(null=True)
    role = fields.CharField(max_length=50, default="user")

    def generate_anonymous_identifier(self, seed: str) -> str:
        # Example: SHA256 based anonymous identifier
        return hashlib.sha256(seed.encode()).hexdigest()

    class Meta:
        table = "users"
