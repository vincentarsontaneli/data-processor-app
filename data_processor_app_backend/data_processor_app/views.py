from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from data_processor_app.data_inference_processor.data_inference_processsor import infer_and_convert_types
import pandas as pd
import numpy as np
import time
class ProcessDataView(APIView):

    def clean_for_json(self, df):
        return df.replace([np.inf, -np.inf, np.nan], None).copy()
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        
        # Validate file type
        if not file.name.endswith('.csv'):
            return Response({'error': 'Only CSV files are allowed'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file)
            
            df_inferred, type_summary = infer_and_convert_types(df)
            df_preview = self.clean_for_json(df_inferred)

            print(type_summary)
            time.sleep(2)
            return Response({
            'dtypes': type_summary, 
            'head': df_preview.head(10).to_dict(orient='records')
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)