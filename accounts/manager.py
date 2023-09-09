from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phoneNumber, dob, address, password=None):
        if not phoneNumber:
            raise ValueError("The Mobile Number field must be set")
        user = self.model(
            phoneNumber=phoneNumber,
            dob=dob,
            address=address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phoneNumber,dob, address,  password=None):
        user = self.create_user(
            phoneNumber=phoneNumber,
            password=password,
            dob=dob,
            address=address
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user




