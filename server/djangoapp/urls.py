from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('register', views.registration, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('get_dealers', views.get_dealers, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealers_by_state, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review', views.add_review, name='add_review'),
    path('get_cars', views.get_car_models, name='get_car_models'),
    path('analyze_review', views.analyze_review, name='analyze_review'),
    path('analyze_review/<str:text>', views.analyze_review, name='analyze_review_text'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
