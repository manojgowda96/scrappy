from rest_framework import serializers
from .models import ScrapingJob


class ScrappingJobSerializer(serializers.ModelSerializer):
    class Meta:
        Model = ScrapingJob
        fields = ['job_id','status','result']