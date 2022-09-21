from django.urls import path
from calc.views import plant_profile_history_add, plant_profile_history_del, plant_profile_share_get_history, plant_profiles, edit_plant_profile, \
    create_plant_profile, \
    plant_profile_del, \
    upload_plant_profile, plant_profile_precalc, plant_profile_history, plant_profile_share

urlpatterns = [

    path('plant_profile/new/', create_plant_profile, name='plant_profile_new'),
    path('plant_profile/from-file/', upload_plant_profile, name='upload_plant_profile'),
    path('plant_profile/<int:pk>/', edit_plant_profile, name='plant_profile_edit'),
    path('plant_profile/share/<int:pk>/', plant_profile_share, name='plant_profile_share'),
    
    path('share/<str:name>/', plant_profile_share_get_history, name='plant_profile_share_get_history'),
    
    path('plant_profile_micro/<int:pk>/', edit_plant_profile, kwargs={'micro':True},  name='plant_profile_edit_micro'),
    

    
    
    path('plant_profile_history/<int:pk>/', plant_profile_history, name='plant_profile_history'),
    path('plant_profile_history/add/<int:pk>/', plant_profile_history_add, name='plant_profile_history_add'),
    path('plant_profile_history/del/<int:pk>/', plant_profile_history_del, name='plant_profile_history_del'),
    

    path('plant_profile/del/<int:pk>/', plant_profile_del, name='plant_profile_del'),
    path('plant_profile/precalc/<int:pk>/', plant_profile_precalc, name='plant_profile_precalc'),
    path('', plant_profiles, name='profile_index'),
   
 
]
