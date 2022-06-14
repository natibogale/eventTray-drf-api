from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
from django.core.validators import RegexValidator, MinValueValidator
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import auth
from datetime import datetime, timedelta
from django.conf import settings
import jwt


roles = (
    ("User", "User"),
    ("Organizer", "Organizer"),
    ("Checker", "Checker"),
)

types = (
    ("Individual", "Individual"),

    ("Organization", "Organization"),
)


gender = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class Manager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self, username, firstName, lastName, gender, role, phoneNumber, password
    ):
        if not username:
            raise ValueError("Users must have a Badge Number")
        if not firstName:
            raise ValueError("Users must have First Names")
        if not lastName:
            raise ValueError("Users must have Last Names")
        if not gender:
            raise ValueError("Users must have a Gender")
        if not role:
            raise ValueError("Users need roles for accounts")
        if not phoneNumber:
            raise ValueError("Users need phone Numbers for accounts")
        user = self.model(
            username=username,
            firstName=firstName,
            lastName=lastName,
            gender=gender,
            role=role,
            phoneNumber=phoneNumber,
        )

        user.set_password(password)
        user.save(using=self._db)
        # user.directorate.set([directorate])
        # user.team.set([team])
        return user

    def create_superuser(
        self,
        username,
        password,
        phoneNumber,
        firstName=None,
        lastName=None,
        gender=None,
        role=None,
    ):
        user = self.create_user(
            username=username,
            phoneNumber=phoneNumber,
            firstName=" ",
            lastName=" ",
            gender=" ",
            role=" ",
            password=password,
        )
        # user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        # user.directorate.set([directorate])
        # user.team.set([team])
        return user


def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = "get_%s_permissions" % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions


class User(AbstractBaseUser):
    username = models.CharField(max_length=500, verbose_name="User Name", unique=True)
    firstName = models.CharField(max_length=500, verbose_name="First Name", blank=True)
    lastName = models.CharField(max_length=500, verbose_name="Last Name", blank=True)
    gender = models.CharField(
        choices=gender,
        max_length=100,
        verbose_name="Gender",
        blank=True,
        default="Male",
    )
    phoneValidator = RegexValidator(
        regex=r"^\+?1?\d{10}$",
        message="Please enter your phonenumber in the format starting with: 09",
    )
    phoneNumber = models.CharField(
        validators=[phoneValidator],
        max_length=10,
        verbose_name="Phone Number",
    )
    profilePicture = models.ImageField(
        upload_to="Profile_Pictures/",
        default="Profile_Pictures/default.png",
        verbose_name="Profile Picture",
    )
    coverPicture = models.ImageField(
        upload_to="Cover_Pictures/",
        default="Cover_Pictures/cover.png",
        verbose_name="Cover Picture"
    )
    email = models.EmailField(verbose_name="Organizer Email", unique=True, blank=True, null=True)
    counter = models.PositiveIntegerField(default=0, blank=False)
    role = models.CharField(
        choices=roles, max_length=100, verbose_name="Role", blank=True
    )
    token = models.CharField(verbose_name="Token", max_length=500)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="date joined")
    last_login = models.DateTimeField(auto_now=True, verbose_name="last login")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "phoneNumber",
    ]

    objects = Manager()

    def admin_photo(self):
        return mark_safe
        ('<img src="{}" width="100" />'.format(self.profilePicture.url))

    admin_photo.short_description = "Profile Picture"
    admin_photo.allow_tags = True

    def natural_key(self, app_label, model):
        return (self.username,) + self.content_type.natural_key()

    natural_key.dependencies = ["contenttypes.contenttype"]

    @property
    def token(self):
        token = jwt.encode(
            {
                "username": self.username,
                "phoneNumber": self.phoneNumber,
                "exp": datetime.utcnow() + timedelta(hours=72),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    # def get_absolute_url(self):
    #     return reverse('ro-profile', kwargs={'pk' : self.pk})

    # def save(self, *args, **kwargs):
    #     try:
    #         self.directorate
    #     except:
    #         self.directorate = Directorates.objects.first()
    #     super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     try:
    #         self.team
    #     except:
    #         self.team = Teams.objects.first()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def has_module_perms(self, app_label):
        return True


class Organizer(models.Model):

    organizer = models.OneToOneField(
        "User", on_delete=models.CASCADE, verbose_name="Organizer ID", related_name="details",primary_key=True,
    )
    

    displayName = models.CharField(
        max_length=150, verbose_name="Business Display Name",  help_text="A name you want Customers to identify your business by. For organizations input the name of your organization."
    )
    organizerType  = models.CharField(choices=types, verbose_name="Organizer Type" , default="Organization", max_length = 150)
    

    twitter = models.CharField(
        verbose_name="Twitter", blank=True, null=True, max_length=150
    )
    telegram = models.CharField(
        verbose_name="Telegram", blank=True, null=True, max_length=150
    )
    facebook = models.CharField(
        verbose_name="Facebook", blank=True, null=True, max_length=150
    )
    instagram = models.CharField(
        verbose_name="Instagram", blank=True, null=True, max_length=150
    )
    verifyingDocument = models.FileField(
        upload_to="Verifying_Document",
        verbose_name="Verifying Document",
        blank=True,
        null=True,
    )
    verifiedOrganizer = models.BooleanField(default=False)
    followers = models.CharField(
        verbose_name="Followers", blank=True, null=True, default=0, max_length=150
    )
    rating = models.CharField(
        verbose_name="Rating", blank=True, null=True, default=0, max_length=150
    )
    totalEvents = models.PositiveIntegerField(
        verbose_name="Total Events",  default=0, blank=True, null=True
    )
    sales = models.PositiveIntegerField(
        verbose_name="Total Sales", blank=True, null=True, default=0
    )
  
    wallet = models.PositiveIntegerField(
        verbose_name="Wallet", blank=True, null=True, default=0
    )

    class Meta:
        verbose_name_plural = "Organizer Details"

    def __str__(self):
        return self.organizer.username
