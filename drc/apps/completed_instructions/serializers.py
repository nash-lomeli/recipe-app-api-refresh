from rest_framework import serializers
from . import models

class CompletedInstructionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CompletedInstruction
        fields = (
            'id','instruction_id','user_id',
            'created_at','updated_at',
        )

