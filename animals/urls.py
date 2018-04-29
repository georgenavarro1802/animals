from django.conf.urls import url
from animals import views


urlpatterns = [

    # Add Animal to a herd and Get Animal dict
    url(r'^animal$', views.AnimalList.as_view(), name=views.AnimalList.name),

    # Animal detail
    url(r'^animal/(?P<pk>[0-9]+)$', views.AnimalDetail.as_view(), name=views.AnimalDetail.name),

    # Add Weight for an animal
    url(r'^animal/(?P<animal>\d+)/weight$', views.AnimalWeightList.as_view(), name=views.AnimalWeightList.name),

    # Detail Weight
    url(r'^animal/(?P<animal>\d+)/weight/(?P<pk>[0-9]+)$', views.AnimalWeightDetail.as_view(),
        name=views.AnimalWeightDetail.name),

    # Estimated total animal weight by date
    url(r'^animal/estimated_weight$', views.AnimalEstimatedWeightList.as_view(),
        name=views.AnimalEstimatedWeightList.name),


]
