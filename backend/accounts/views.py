from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer, FormSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Form, Comment
from .permissions import IsOwner


# Vue pour l'inscription de l'utilisateur

class SignupView(APIView):
    # Méthode POST pour créer un nouvel utilisateur
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        # Retourne les erreurs de validation si les données sont invalides
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Vue pour la connexion de l'utilisateur

class LoginView(APIView):
    # Méthode POST pour authentifier l'utilisateur et retourner des jetons JWT
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Génère un jeton de rafraîchissement et d'accès pour l'utilisateur authentifié
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "Login successful"
                }, status=status.HTTP_200_OK)
            # Retourne une erreur si l'authentification échoue
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        # Retourne les erreurs de validation si les données sont invalides
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Vue pour la création de formulaires

class CreateFormView(APIView):
    # Méthode POST pour créer un nouveau formulaire
    def post(self, request):
        print("Received data:", request.data)  # Journalisation des données reçues
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Log de l'erreur si l'enregistrement échoue
                print("Save error:", str(e))
                return Response({"error": "Failed to save form."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Log des erreurs de validation
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Vue pour lister tous les formulaires existants

class FormListView(generics.ListAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer



# Vue pour afficher, mettre à jour ou supprimer un formulaire spécifique

class FormDetailView(APIView):
    # Méthode GET pour récupérer un formulaire spécifique par ID
    def get(self, request, pk):
        try:
            form = Form.objects.get(pk=pk)
            serializer = FormSerializer(form)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Form.DoesNotExist:
            # Log si le formulaire n'existe pas
            print(f"Form with ID {pk} not found.")
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log pour toute autre erreur inattendue
            print(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Méthode PUT pour mettre à jour un formulaire existant
    def put(self, request, pk):
        try:
            form = Form.objects.get(pk=pk)
            serializer = FormSerializer(form, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Log des erreurs de validation lors de la mise à jour
                print("Validation errors during update:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Form.DoesNotExist:
            # Retourne une erreur si le formulaire n'existe pas
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log de toute erreur inattendue lors de la mise à jour
            print(f"Unexpected error during update: {e}")
            return Response({"error": "Failed to update form."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Méthode DELETE pour supprimer un formulaire existant
    def delete(self, request, pk):
        try:
            form = Form.objects.get(pk=pk)
            form.delete()
            return Response({"message": "Form deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Form.DoesNotExist:
            # Retourne une erreur si le formulaire à supprimer n'existe pas
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log pour toute erreur inattendue lors de la suppression
            print(f"Unexpected error during deletion: {e}")
            return Response({"error": "Failed to delete form."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Vue pour lister les commentaires d'un formulaire et en créer de nouveaux

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    # Méthode pour obtenir la liste des commentaires d'un formulaire spécifique
    def get_queryset(self):
        form_id = self.kwargs.get('form_id')
        return Comment.objects.filter(form_id=form_id)

    # Méthode pour sauvegarder un nouveau commentaire associé à un formulaire
    def perform_create(self, serializer):
        form_id = self.kwargs.get('form_id')
        form = Form.objects.get(pk=form_id)  # Récupère l'instance du formulaire
        serializer.save(form=form)  # Sauvegarde le commentaire avec l'instance du formulaire
