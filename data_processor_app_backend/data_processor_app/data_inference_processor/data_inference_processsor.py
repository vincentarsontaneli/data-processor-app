import pandas as pd
import numpy as np
from dateutil import parser
import re

def infer_and_convert_types(df: pd.DataFrame, sample_size: int = 500000) -> tuple[pd.DataFrame, dict]:
    """
    Infer and convert column types in a DataFrame.
    Samples 20000 rows for performance on large datasets.
    
    Args:
        df: Input DataFrame
        sample_size: Number of rows to sample for type inference
        
    Returns:
        tuple: (converted DataFrame, dictionary of column types)
    """
    
    # Sample the dataframe for faster type inference
    sample_df = df.sample(n=min(sample_size, len(df))) if len(df) > sample_size else df

    type_summary = {}

    for column in df.columns:
        print(f"Processing column: {column}")
        # Get non-null sample values
        sample_values = sample_df[column].replace(['NaN', 'nan', 'NULL', 'None'], np.nan).dropna().astype(str)

        if len(sample_values) == 0:
            type_summary[column] = 'unknown'
            continue

        try:
            # Clean the values of common artifacts
            cleaned_values = sample_values.str.strip().str.upper()

            # Test for dates
            date_success = 0
            test_values = cleaned_values[:min(10, len(cleaned_values))]
            for value in test_values:
                try:
                    # Skip obvious non-dates
                    if len(value.strip()) < 6:  # Too short to be a date
                        break
                    parser.parse(value)
                    date_success += 1
                except:
                    continue

            if date_success >= min(5, len(test_values)):
                type_summary[column] = 'datetime'
                continue

            # Test for numeric with flexible pattern
            numeric_pattern = r'^[-+]?\d*\.?\d+$'
            if (cleaned_values.str.replace(',', '').str.match(numeric_pattern)).all():
                # Convert to float temporarily for check
                cleaned_values = pd.to_numeric(cleaned_values, errors='coerce')
                if (cleaned_values % 1 == 0).all():
                    type_summary[column] = 'integer'
                else:
                    type_summary[column] = 'float'
                continue

            # Test for boolean
            bool_map = {
                'TRUE': True, 'FALSE': False,
                'YES': True, 'NO': False,
                'Y': True, 'N': False,
                '1': True, '0': False,
                'T': True, 'F': False
            }
            if cleaned_values.isin(bool_map.keys()).all():
                type_summary[column] = 'boolean'
                continue

            # Test for categorical - IT IS RECOMMENDED TO USE A LARGE DATASET
            unique_ratio = len(cleaned_values.unique()) / len(cleaned_values)
            if unique_ratio < 0.3:  # If less than 20% unique values
                type_summary[column] = 'category'
                continue

            # Test for text without numbers
            if cleaned_values.str.match(r'^[A-Za-z\-_\.]+$').all():
                type_summary[column] = 'string'
                continue

            # Default to object if no other type matched
            type_summary[column] = 'object'

        except Exception as e:
            continue  # Keep as object type if conversion fails

    return df, type_summary
