from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone

import secrets
from datetime import timedelta


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est requise.")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Un superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Un superutilisateur doit avoir is_superuser=True.")
        return self.create_user(email, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(unique=True, verbose_name="Adresse e-mail")
    phone = models.CharField(max_length=32, blank=True, verbose_name="Téléphone")
    country = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Membre de l'équipe")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Inscrit le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split(" ")[0]


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="email_verification", verbose_name="Utilisateur")
    code_hash = models.CharField(max_length=128, verbose_name="Code (haché)")
    expires_at = models.DateTimeField(verbose_name="Expire le")
    last_sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Dernier envoi")
    attempts = models.PositiveSmallIntegerField(default=0, verbose_name="Tentatives")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    class Meta:
        verbose_name = "vérification d'e-mail"
        verbose_name_plural = "vérifications d'e-mail"

    @classmethod
    def issue_for(cls, user):
        code = f"{secrets.randbelow(1_000_000):06d}"
        verification, _ = cls.objects.update_or_create(
            user=user,
            defaults={
                "code_hash": make_password(code),
                "expires_at": timezone.now() + timedelta(minutes=10),
                "last_sent_at": timezone.now(),
                "attempts": 0,
            },
        )
        return verification, code

    def verify(self, code):
        if self.attempts >= 5 or timezone.now() >= self.expires_at:
            return False
        self.attempts += 1
        valid = check_password(code, self.code_hash)
        self.save(update_fields=["attempts"])
        return valid

    def can_resend(self):
        return timezone.now() >= self.last_sent_at + timedelta(seconds=60)
