from django.urls import path
from calc.views import plant_profiles,  edit_plant_profile, create_plant_profile, plant_profile_del, \
    upload_plant_profile,  plant_profile_precalc

urlpatterns = [

    path('plant_profile/new/', create_plant_profile, name='plant_profile_new'),
    path('plant_profile/from-file/', upload_plant_profile, name='upload_plant_profile'),
    path('plant_profile/<int:pk>/', edit_plant_profile, name='plant_profile_edit'),
    path('plant_profile/del/<int:pk>/', plant_profile_del, name='plant_profile_del'),
    path('plant_profile/precalc/<int:pk>/', plant_profile_precalc, name='plant_profile_precalc'),
    path('', plant_profiles, name='profile_index'),
   
 
]
