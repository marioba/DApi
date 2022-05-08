from django.urls import path
from dataapi.core.views import CreateDataView, ListDataView, ConsentsView

urlpatterns = [
    path('data/', ListDataView.as_view()),
    path('data/<int:customerId>/<int:dialogId>', CreateDataView.as_view()),
    path('consents/<int:dialogId>', ConsentsView.as_view()),
]
