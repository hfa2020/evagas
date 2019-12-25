from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class UsuariosManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Usuarios(AbstractUser):
    FUNDAMENTAL = 1
    MEDIO = 2
    TECNOLOGO = 3
    SUPERIOR = 4
    POS = 5
    DOUTORADO = 6

    ESCOLARIDADE = [(FUNDAMENTAL, "Ensino Fundamental"),
                    (MEDIO, "Ensino Médio"), (TECNOLOGO, "Tecnólogo"),
                    (SUPERIOR, "Ensino Superior"),
                    (POS, "Pós / MBA / Mestrado"), (DOUTORADO, "Doutorado")]
    username = None
    email = models.EmailField('Endereço de email', unique=True)
    experiencia = models.TextField(max_length=500,
                                   verbose_name="Experiência",
                                   default="Sem experiência")
    ult_escola = models.IntegerField(choices=ESCOLARIDADE,
                                     default=FUNDAMENTAL,
                                     verbose_name="Última Escolaridade")
    is_empresa = models.BooleanField(default=False, verbose_name="Empresa? ")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'experiencia', 'ult_escola']

    objects = UsuariosManager()
