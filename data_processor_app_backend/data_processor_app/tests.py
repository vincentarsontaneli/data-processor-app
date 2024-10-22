from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
import pandas as pd
import numpy as np
from datetime import datetime
import os
from .data_inference_processor.data_inference_processor import (
    infer_date,
    infer_column_type,
    convert_column_type,
    process_chunk,
    infer_and_convert_types
)

class DataInferenceProcessorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('process-data')
        self.test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_files')
        os.makedirs(self.test_dir, exist_ok=True)
        self.create_test_files()

    def create_test_files(self):
        # Create test data with various edge cases
        self.test_data = pd.DataFrame({
            'numeric_clean': [1, 2, 3, 4, 5],
            'numeric_with_nulls': [1, None, 3, None, 5],
            'numeric_mixed': [1, 2.5, 3, 4.5, 5],
            'text_clean': ['a', 'b', 'c', 'd', 'e'],
            'text_with_nulls': ['a', None, 'c', None, 'e'],
            'date_clean': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
            'date_mixed_format': ['2023-01-01', '01/02/2023', 'Jan 3, 2023', '2023-01-04', '05-01-2023'],
            'date_with_nulls': ['2023-01-01', None, '2023-01-03', None, '2023-01-05'],
            'boolean_clean': [True, False, True, False, True],
            'boolean_mixed': [True, 1, 'true', 'False', 0],
            'categorical': ['cat1', 'cat2', 'cat1', 'cat2', 'cat1'],
            'all_nulls': [None, None, None, None, None],
            'mixed_types': [1, 'text', 3.14, True, None],
        })
        
        # Save as CSV
        self.csv_path = os.path.join(self.test_dir, 'test_data.csv')
        self.test_data.to_csv(self.csv_path, index=False)
        
        # Save as Excel
        self.excel_path = os.path.join(self.test_dir, 'test_data.xlsx')
        self.test_data.to_excel(self.excel_path, index=False)

    def tearDown(self):
        # Clean up test files
        for file_path in [self.csv_path, self.excel_path]:
            if os.path.exists(file_path):
                os.remove(file_path)
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)

    def test_infer_date(self):
        """Test date inference with various formats and edge cases"""
        # Test valid dates
        self.assertIsInstance(infer_date('2023-01-01'), datetime)
        self.assertIsInstance(infer_date('01/01/2023'), datetime)
        self.assertIsInstance(infer_date('January 1, 2023'), datetime)
        
        # Test edge cases
        self.assertIsNone(infer_date('not a date'))
        self.assertIsNone(infer_date(''))
        self.assertIsNone(infer_date(None))
        self.assertIsNone(infer_date(123))

    def test_infer_column_type(self):
        """Test column type inference with various data types and edge cases"""
        # Test numeric types
        self.assertEqual(infer_column_type(pd.Series([1, 2, 3])), 'int64')
        self.assertEqual(infer_column_type(pd.Series([1.0, 2.5, 3.0])), 'float64')
        self.assertEqual(infer_column_type(pd.Series([1, None, 3])), 'int64')
        
        # Test boolean types
        self.assertEqual(infer_column_type(pd.Series([True, False, True])), 'boolean')
        self.assertEqual(infer_column_type(pd.Series([1, 0, 1, 0])), 'boolean')
        self.assertEqual(infer_column_type(pd.Series(['true', 'false', 'true'])), 'boolean')
        
        # Test date types
        dates = pd.Series(['2023-01-01', '2023-01-02'])
        self.assertEqual(infer_column_type(dates), 'datetime64[ns]')
        
        # Test categorical
        categorical = pd.Series(['A', 'B', 'A', 'B'] * 100)
        self.assertEqual(infer_column_type(categorical), 'category')
        
        # Test edge cases
        self.assertEqual(infer_column_type(pd.Series([])), 'object')
        self.assertEqual(infer_column_type(pd.Series([None, None])), 'object')
        self.assertEqual(infer_column_type(pd.Series(['A', 1, True])), 'object')

    def test_convert_column_type(self):
        """Test column type conversion with various cases"""
        # Test boolean conversion
        bool_series = convert_column_type(pd.Series(['true', 'false', '1', '0']), 'boolean')
        self.assertTrue(is_bool_dtype(bool_series))
        
        # Test date conversion
        date_series = convert_column_type(pd.Series(['2023-01-01', 'invalid', None]), 'datetime64[ns]')
        self.assertEqual(date_series.dtype, 'datetime64[ns]')
        
        # Test numeric conversion
        num_series = convert_column_type(pd.Series(['1', '2.5', 'invalid']), 'float64')
        self.assertTrue(pd.api.types.is_float_dtype(num_series))

    def test_api_view_csv(self):
        """Test the API view with CSV file"""
        with open(self.csv_path, 'rb') as file:
            file_content = file.read()
        
        response = self.client.post(
            self.url,
            {'file': SimpleUploadedFile("test_data.csv", file_content, content_type="text/csv")},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('dtypes', response.data)
        self.assertIn('head', response.data)
        self.assertIn('metadata', response.data)

    def test_api_view_excel(self):
        """Test the API view with Excel file"""
        with open(self.excel_path, 'rb') as file:
            file_content = file.read()
        
        response = self.client.post(
            self.url,
            {'file': SimpleUploadedFile(
                "test_data.xlsx",
                file_content,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('dtypes', response.data)
        self.assertIn('head', response.data)
        self.assertIn('metadata', response.data)

    def test_api_view_large_file(self):
        """Test handling of larger files"""
        # Create a larger test file
        large_data = pd.DataFrame({
            'numeric': range(10000),
            'text': ['text'] * 10000,
            'date': pd.date_range('2023-01-01', periods=10000).astype(str)
        })
        large_file_path = os.path.join(self.test_dir, 'large_test.csv')
        large_data.to_csv(large_file_path, index=False)
        
        with open(large_file_path, 'rb') as file:
            response = self.client.post(
                self.url,
                {'file': SimpleUploadedFile("large_test.csv", file.read(), content_type="text/csv")},
                format='multipart'
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)