from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Form, Comment

# Récupère le modèle utilisateur pour l'utiliser dans le serializer d'inscription
User = get_user_model()


# Serializer pour l'inscription d'un utilisateur

class SignupSerializer(serializers.ModelSerializer):
    # Champ pour le mot de passe avec validation intégrée
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User  # Utilise le modèle utilisateur
        fields = ('email', 'username', 'password')  # Champs inclus dans le serializer

    # Méthode pour créer un utilisateur avec les données validées
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user



# Serializer pour la connexion d'un utilisateur

class LoginSerializer(serializers.Serializer):
    # Champs pour l'email et le mot de passe de l'utilisateur
    email = serializers.EmailField()  # Champ email pour la connexion
    password = serializers.CharField(write_only=True)  # Champ mot de passe (écriture seule)
    


# Serializer pour le modèle Form (Formulaire)

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form  # Utilise le modèle Form
        fields = ['id', 'email', 'region', 'place', 'topic', 'question', 'created_at']  # Champs du formulaire à inclure dans le serializer



# Serializer pour le modèle Comment (Commentaire)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment  # Utilise le modèle Comment
        fields = ['id', 'form', 'text', 'created_at']  # Champs du commentaire à inclure dans le serializer
        read_only_fields = ['form']  # Définit `form` comme champ en lecture seule
