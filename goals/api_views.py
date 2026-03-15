from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Goal
from .serializers import GoalSerializer
from .services import GoalService


class GoalListCreateApi(generics.ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalService.filtered_queryset(self.request.user, self.request.query_params)

    def perform_create(self, serializer):
        serializer.instance = GoalService.create_goal(self.request.user, serializer.validated_data)


class GoalDetailApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(owner=self.request.user)
