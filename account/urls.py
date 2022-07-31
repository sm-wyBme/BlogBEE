from account import views
from django.urls import path

app_name = 'account'

urlpatterns = [
    path('<user_id>/', views.user_profile, name = 'view'),
    path('<user_id>/edit/', views.edit_account_view, name = 'edit'),
    path('<user_id>/update-profile/', views.update_profile_image, name = 'update-image'),
    path('<user_id>/update-profile/crop-image', views.crop_image, name = 'crop_image'),

]