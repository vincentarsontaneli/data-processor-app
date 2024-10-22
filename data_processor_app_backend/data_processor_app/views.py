from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from data_processor_app.data_inference_processor.data_inference_processor import infer_and_convert_types
import pandas as pd

class ProcessDataView(APIView):
    def post(self, request, format=None):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        file_path = os.path.join(default_storage.location, file_name)

        try:
            df = infer_and_convert_types(file_path)
            result = {
                'dtypes': df.dtypes.apply(lambda x: x.name).to_dict(),
                'head': df.head().to_dict(orient='records')
            }
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            default_storage.delete(file_name)