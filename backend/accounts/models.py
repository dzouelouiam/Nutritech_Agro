from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model  # Import nécessaire pour gérer le modèle utilisateur personnalisé
from django.db import models
from django.conf import settings


# Manager personnalisé pour le modèle CustomUser

class CustomUserManager(BaseUserManager):
    # Méthode pour créer un utilisateur standard
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Le champ Email doit être renseigné')
        email = self.normalize_email(email)  # Normalise l'email pour consistance
        user = self.model(email=email, username=username, **extra_fields)  # Crée une instance de CustomUser
        user.set_password(password)  # Définit le mot de passe
        user.save(using=self._db)  # Sauvegarde dans la base de données
        return user

    # Méthode pour créer un superutilisateur
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Définit l'utilisateur comme staff
        extra_fields.setdefault('is_superuser', True)  # Définit l'utilisateur comme superutilisateur
        return self.create_user(email, username, password, **extra_fields)



# Modèle utilisateur personnalisé

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Champ email unique
    username = models.CharField(max_length=150, unique=True, default="default_user")  # Nom d'utilisateur unique avec valeur par défaut
    is_active = models.BooleanField(default=True)  # Indique si le compte est actif
    is_staff = models.BooleanField(default=False)  # Indique si l'utilisateur est membre du staff

    objects = CustomUserManager()  # Définit CustomUserManager comme gestionnaire pour ce modèle

    USERNAME_FIELD = 'email'  # Email utilisé pour l'authentification
    REQUIRED_FIELDS = ['username']  # Champs obligatoires en plus de l'email



# Utilise le modèle utilisateur configuré (ici, CustomUser)
User = get_user_model()



# Modèle pour les formulaires soumis par les utilisateurs

class Form(models.Model):
    # Choix pour le champ `topic` du formulaire
    TOPIC_CHOICES = [
        ('Engrais solides', 'Engrais solides'),
        ('Engrais spéciaux hydrosolubles', 'Engrais spéciaux hydrosolubles'),
        ('Correcteurs de carence', 'Correcteurs de carence'),
        ('Biostimulants', 'Biostimulants'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Référence à l'utilisateur qui a créé le formulaire
    email = models.EmailField()  # Email de l'utilisateur
    region = models.CharField(max_length=100)  # Région de l'utilisateur
    place = models.CharField(max_length=100)  # Lieu associé au formulaire
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)  # Sujet choisi parmi les choix disponibles
    question = models.TextField()  # Question posée dans le formulaire
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du formulaire
    
    def __str__(self):
        return f"{self.topic} par {self.user.username}"  # Affiche le sujet et l'auteur dans la représentation en chaîne


# Modèle pour les commentaires liés aux formulaires

class Comment(models.Model):
    form = models.ForeignKey(Form, related_name="comments", on_delete=models.CASCADE)  # Référence au formulaire
    text = models.TextField()  # Texte du commentaire
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du commentaire
