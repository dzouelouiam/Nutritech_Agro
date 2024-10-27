from django.urls import path
from .views import SignupView, LoginView, CreateFormView, FormListView, FormDetailView, CommentListCreateView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-form/', CreateFormView.as_view(), name='create-form'),
    path('forms/', FormListView.as_view(), name='form-list'),
    path('form/<int:pk>/', FormDetailView.as_view(), name='form-detail'),
    path('form/<int:form_id>/comments/', CommentListCreateView.as_view(), name='form-comments'),
]
