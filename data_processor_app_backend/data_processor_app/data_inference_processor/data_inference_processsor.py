import pandas as pd
import numpy as np
from dateutil import parser
import re

def infer_and_convert_types(df: pd.DataFrame, sample_size: int = 20000) -> tuple[pd.DataFrame, dict]:
    """
    Infer and convert column types in a DataFrame.
    Samples 20000 rows for performance on large datasets.
    
    Args:
        df: Input DataFrame
        sample_size: Number of rows to sample for type inference
        
    Returns:
        tuple: (converted DataFrame, dictionary of column types)
    """
    df = df.copy()
    
    # Sample the dataframe for faster type inference
    sample_df = df.sample(n=min(sample_size, len(df))) if len(df) > sample_size else df
    
    for column in df.columns:

        print(f"Processing column: {column}")
        # Skip columns that are already properly typed
        if df[column].dtype != 'object':
            continue
            
        # Get non-null sample values
        sample_values = sample_df[column].dropna().astype(str)
        if len(sample_values) == 0:
            continue

        try:
            # Clean the values of common artifacts
            cleaned_values = sample_values.str.strip().str.upper()
            
            # Test for boolean
            bool_map = {
                'TRUE': True, 'FALSE': False, 
                'YES': True, 'NO': False,
                'Y': True, 'N': False,
                '1': True, '0': False,
                'T': True, 'F': False
            }
            if cleaned_values.isin(bool_map.keys()).all():
                df[column] = df[column].str.strip().str.upper().map(bool_map).astype(bool)
                continue

            # Test for percentage
            if sample_values.str.contains('%').any():
                print("PERCENTAGE")
                df[column] = df[column].str.rstrip('%').str.replace(',', '').astype(float) / 100
                continue

            # Test for complex numbers
            if sample_values.str.contains(r'[+-][0-9.]*[ji]').any():
                df[column] = df[column].apply(lambda x: complex(str(x).replace(' ', '')) if pd.notna(x) else None).astype(complex)
                continue

            # Test for numeric with flexible pattern
            numeric_pattern = r'^[-+]?\d*\.?\d+$'
            if (sample_values.str.replace(',', '').str.match(numeric_pattern)).all():
                print("NUMERIC")
                df[column] = pd.to_numeric(df[column].str.replace(',', ''), errors='coerce')
                # Convert to Int64 if all values are integers
                if (df[column] % 1 == 0).all():
                    print("INTEGER")
                    df[column] = df[column].astype('Int64')
                continue

            # Test for dates
            date_success = 0
            test_values = sample_values[:min(10, len(sample_values))]
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
                df[column] = pd.to_datetime(df[column], errors='coerce')
                continue

            # Test for mixed IDs (alphanumeric with special characters)
            if sample_values.str.match(r'^[A-Za-z0-9\-_\.]+$').all():
                df[column] = df[column].astype(str).replace('None', np.nan)
                continue

            # Test for categorical
            unique_ratio = len(sample_values.unique()) / len(sample_values)
            if unique_ratio < 0.6:  # If less than 60% unique values
                df[column] = df[column].astype('category')
                continue

        except Exception as e:
            continue  # Keep as object type if conversion fails

    # Generate summary of conversions
    type_summary = {
        col: str(df[col].dtype) 
        for col in df.columns
    }
    
    return df, type_summary