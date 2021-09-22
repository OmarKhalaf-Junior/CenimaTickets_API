from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken
from tickets import views
from rest_framework.routers import DefaultRouter


router= DefaultRouter()
router.register('guest', views.Viewsets_Guest)
router.register('movie', views.Viewsets_Movie)
router.register('reservation', views.Viewsets_Reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api-auth/', include('rest_framework.urls')),      ## Rest Framework Authentication

    path('api-token-auth/', ObtainAuthToken),      ##  return a JSON response

    path('static_data/', views.static_data),

    path('quering_data/', views.quering_data),

    path('FBV_List/', views.FBV_List),
    path('FBV_pk/<int:pk>', views.FBV_pk),

    path('CBV_List/', views.CBV_List.as_view()),
    path('CBV_pk/<int:pk>', views.CBV_pk.as_view()),

    path('Mixins_List/', views.Mixins_List.as_view()),
    path('Mixins_pk/<int:pk>', views.Mixins_pk.as_view()),

    path('Generics_List/', views.Generics_List.as_view()),
    path('Generics_pk/<int:pk>', views.Generics_pk.as_view()),

    path('Viewsets/', include(router.urls)),

    path('find_movie/', views.find_movie),

    path('create_reservation/', views.create_reservation),
]
