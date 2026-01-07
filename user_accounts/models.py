from django.db import models

# Create your models here.

class UserAccounts(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(max_length=100,unique=True,primary_key=True)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_accounts"

    def __str__(self):
        return self.email
  