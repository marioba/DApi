from django.urls import path
from .views import DataView, ConsentsView

urlpatterns = [
    path('data/', DataView.as_view()),
    path('data/<int:customerId>/<int:dialogId>', DataView.as_view()),
    path('consents/<int:dialogId>', ConsentsView.as_view()),
]
