from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,name, phoneNumber, dob, address, password=None):
        if not phoneNumber:
            raise ValueError("The Mobile Number field must be set")
        user = self.model(
            phoneNumber=phoneNumber,
            dob=dob,
            address=address,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, userId, phoneNumber,dob, address,  password=None):
        user = self.create_user(
            phoneNumber=phoneNumber,
            password=password,
            dob=dob,
            address=address,
            name=name
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user




