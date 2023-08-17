from django.urls import path

from tour_guide_bulgaria.web.views.generic import HomeView, AboutUsView, show_dashboard, contact_view
from tour_guide_bulgaria.web.views.sights import EditSightView, \
    DeleteSightView, AddSightView, user_sights_view, like_sight, sight_details

urlpatterns = (
    path('', HomeView.as_view(), name='show index'),
    path('dashboard/', show_dashboard, name='show dashboard'),
    path('user-sights/', user_sights_view, name='user sights'),
    path('about/', AboutUsView.as_view(), name='about us'),
    path('contact/', contact_view, name='contact'),


    path('sight/add/', AddSightView.as_view(), name='add sight'),
    path('sight/details/<int:pk>/', sight_details, name='sight details'),
    path('like/<int:pk>/', like_sight, name='like sight'),
    path('sight/edit/<int:pk>', EditSightView.as_view(), name='edit sight'),
    path('sight/delete/<int:pk>', DeleteSightView.as_view(), name='delete sight'),
    )

