from django.urls import path
from .views import ProcessDataView

urlpatterns = [
    path('process/', ProcessDataView.as_view(), name='process-data'),
]