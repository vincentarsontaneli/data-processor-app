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
        # Clean DataFrame to ensure JSON compatibility
        df_clean = df.replace({
            np.inf: np.nan,
            -np.inf: np.nan,
            np.nan: None
        })
        return df_clean
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        # Check if the file extension is supported
        if not file.name.endswith(('.csv', '.xls', '.xlsx')):
            return Response({'error': 'Only CSV, XLS, and XLSX files are allowed'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:  # .xls or .xlsx
                df = pd.read_excel(file)
            df_inferred, type_summary = infer_and_convert_types(df)
            df_preview = self.clean_for_json(df_inferred)

            print(type_summary)
            return Response({
                'dtypes': type_summary,
                'head': df_preview.head(20).to_dict(orient='records')
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)