from django.conf.urls import url
from animals import views


urlpatterns = [

    # Add Animal to a herd and Get Animal dict
    url(r'^animal$', views.AnimalList.as_view(), name=views.AnimalList.name),

    # Add Weight for an animal
    url(r'^animal/(?P<animal>\d+)/weight', views.AnimalWeightList.as_view(), name=views.AnimalWeightList.name),

    # Estimated total animal weight by date
    url(r'^animal/estimated_weight$', views.AnimalEstimatedWeightList.as_view(),
        name=views.AnimalEstimatedWeightList.name),

    # url(r'^animal/(?P<pk>[0-9]+)$', views.AnimalDetail.as_view(), name=views.AnimalDetail.name),
]
