from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q


class UserManager(BaseUserManager):
    def create_user(self, name, id, phoneNumber, dob, address, password=None):
        if not phoneNumber:
            raise ValueError("The Mobile Number field must be set")
        user = self.model(
            id=id,
            phoneNumber=phoneNumber,
            dob=dob,
            address=address,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, id, phoneNumber,dob, address,  password=None):
        user = self.create_user(
            id = id,
            phoneNumber=phoneNumber,
            password=password,
            dob=dob,
            address=address,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user



