from rest_framework import generics, viewsets, views, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
)
from . import models, serializers, renderers
from drc.apps.recipes import models as recipe_models, serializers as recipe_serializers


class CompletedInstructionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CompletedInstructionSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (renderers.CompletedInstructionJSONRenderer,)
    lookup_field = 'instruction__id'
    lookup_url_kwarg = 'instruction_id'
    queryset = models.CompletedInstruction.objects.all()

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)

    def post(self, request, instruction_id=None):
            user = self.request.user.profile
            context = {'request': request}

            try:
                instruction = recipe_models.Instruction.objects.get(pk=instruction_id)
            except recipe_models.Instruction.DoesNotExist:
                raise NotFound('An instruction with this ID does not exist.')

            completed = models.CompletedInstruction.objects.filter(instruction=instruction,user=user)
            
            if completed.exists():
                completed.delete()
            else:
                models.CompletedInstruction.objects.create(instruction=instruction,user=user)
                        
            serializer = recipe_serializers.InstructionSerializer(
                instruction,
                context=context
            )

            return Response(serializer.data, status=status.HTTP_200_OK)