from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScrapingJob
from .serializers import ScrappingJobSerializer
from .tasks import scrape_coin_data

# Create your views here.
class StartScrapingView(APIView):
    def post(self,request):
        coins = request.data.get('coins',[])
        job = ScrapingJob.objects.create()
        scrape_coin_data.delay(coins, str(job.job_id))
        return Response({'job_id':job.job_id},status=status.HTTP_202_ACCEPTED)
    


class ScrapingStatusView(APIView):
    def get(self,request,job_id):
        try:
            job = ScrapingJob.objects.get(job_id=job_id)
            serializer = ScrappingJobSerializer(job)
            return Response(serializer.data)
        except ScrapingJob.DoesNotExist:
            return Response({'error':'Job Not Found'},status=status.HTTP_404_NOT_FOUND)