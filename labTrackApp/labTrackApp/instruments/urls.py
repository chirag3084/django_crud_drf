from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.InstrumentListView.as_view(), name='instruments-page'),
    path('add/', views.InstrumentAddView.as_view(), name='instrument-add'),
    path('<int:pk>/', include([
        path('', views.InstrumentDetailView.as_view(), name='instrument-details'),
        path('record/', views.InstrumentMaintenanceView.as_view(), name='instrument-maintenance'),

    ])),

    ]