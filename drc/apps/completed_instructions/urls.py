from django.urls import path
from . import views

app_name = 'completed_instructions'

urlpatterns = [
    path('<int:instruction_id>/',
        views.CompletedInstructionListCreateAPIView.as_view(),
        name='completed-instruction'
    ),
]