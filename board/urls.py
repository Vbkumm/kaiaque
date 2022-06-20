"""kaiaque URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import url
from board import views

app_name = 'board'


urlpatterns = [
    url(r'^experience_wizard_create/$', views.ExperienceWizardCreateView.as_view(), name='experience_wizard_create'),
    url(r'^experience_detail/(?P<pk>\d+)/$', views.ExperienceDetailView.as_view(), name='experience_detail'),
    url(r'^experience_update/(?P<pk>\d+)/$', views.ExperienceUpdateView.as_view(), name='experience_update'),
    url(r'^category_sport_create/$', views.CategorySportCreateView.as_view(), name='category_sport_create'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_price_create/$', views.ExperiencePriceCreateView.as_view(), name='experience_price_create'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_price_update/(?P<e_price_pk>\d+)/$', views.ExperiencePriceUpdateView.as_view(),
        name='experience_price_update'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_location_create/$', views.ExperienceMeetPointCreateView.as_view(),
        name='experience_location_create'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_location_update/(?P<e_location_pk>\d+)/$', views.ExperienceMeetPointUpdateView.as_view(),
        name='experience_location_update'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_comment_create/$', views.ExperienceCommentCreateView.as_view(),
        name='experience_comment_create'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_comment_update/(?P<e_comment_pk>\d+)/$', views.ExperienceCommentUpdateView.as_view(),
        name='experience_comment_update'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_comment_delete/(?P<e_comment_pk>\d+)/$', views.ExperienceCommentDeleteView.as_view(),
        name='experience_comment_delete'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_photo_gallery_create/$',
        views.ExperiencePhotoGalleryCreateView.as_view(), name='experience_photo_gallery_create'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_photo_delete/(?P<e_photo_pk>\d+)/$', views.ExperiencePhotoDeleteView.as_view(),
        name='experience_photo_delete'),
    url(r'^experience_detail/(?P<pk>\d+)/equipment_wizard_create/$', views.EquipmentWizardCreateView.as_view(),
        name='equipment_wizard_create'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_equipment_update/(?P<equipment_pk>\d+)/$', views.ExperienceEquipmentUpdateView.as_view(),
        name='experience_equipment_update'),
    url(r'^experience_detail/(?P<pk>\d+)/experience_equipment_delete/(?P<equipment_pk>\d+)/$', views.ExperienceEquipmentDeleteView.as_view(),
        name='experience_equipment_delete'),

]
