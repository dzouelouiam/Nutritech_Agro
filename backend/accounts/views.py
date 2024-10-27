from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer, FormSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Form, Comment
from .permissions import IsOwner
from .serializers import CommentSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "Login successful"
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateFormView(APIView):
    # If you want to make this view accessible to authenticated users only, uncomment the next line.
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Received data:", request.data)  # Debugging log
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("Save error:", str(e))  # Log any save-related error
                return Response({"error": "Failed to save form."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Validation errors:", serializer.errors)  # Log validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormListView(generics.ListAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer


class FormDetailView(APIView):
    # If you want only superusers to access this view, uncomment the next line.
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        try:
            form = Form.objects.get(pk=pk)
            serializer = FormSerializer(form)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Form.DoesNotExist:
            print(f"Form with ID {pk} not found.")  # Debugging log for missing form
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error: {e}")  # Log any unexpected error
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            form = Form.objects.get(pk=pk)
            serializer = FormSerializer(form, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print("Validation errors during update:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Form.DoesNotExist:
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error during update: {e}")
            return Response({"error": "Failed to update form."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            form = Form.objects.get(pk=pk)
            form.delete()
            return Response({"message": "Form deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Form.DoesNotExist:
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error during deletion: {e}")
            return Response({"error": "Failed to delete form."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        form_id = self.kwargs.get('form_id')
        return Comment.objects.filter(form_id=form_id)

    def perform_create(self, serializer):
        form_id = self.kwargs.get('form_id')
        form = Form.objects.get(pk=form_id)  # Retrieve the form instance
        serializer.save(form=form)  # Save comment with form instance