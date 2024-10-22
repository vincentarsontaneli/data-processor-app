import pandas as pd
import numpy as np
from datetime import datetime
import dateutil.parser
from typing import Union, Dict, Tuple
import concurrent.futures
import os
from pandas.api.types import is_numeric_dtype, is_bool_dtype

def infer_date(value: str) -> Union[datetime, None]:
    """Attempt to parse a string as a date, returning None if parsing fails."""
    if pd.isna(value):
        return None
    if isinstance(value, (datetime, pd.Timestamp)):
        return value
    if not isinstance(value, str):
        return None
    try:
        return dateutil.parser.parse(value)
    except (ValueError, TypeError):
        return None

def get_sample_values(column: pd.Series, sample_size: int = 1000) -> pd.Series:
    """Retrieve a sample of values from a column."""
    if len(column) <= sample_size:
        return column
    return column.sample(n=sample_size, random_state=42)

def infer_column_type(column: pd.Series) -> str:
    """Infer the data type of a column, considering various data forms."""
    if column.isna().all():
        return 'object'

    non_null = column.dropna()
    sample = get_sample_values(non_null)

    if is_bool_dtype(column) or set(non_null.astype(str).unique()) <= {True, False, '1', '0', 'true', 'false', 'True', 'False'}:
        return 'boolean'
    
    if is_numeric_dtype(column) or (pd.to_numeric(sample, errors='coerce').notna().mean() > 0.9):
        return 'int64' if (column.dropna() % 1 == 0).all() else 'float64'
    
    if column.dtype == 'object' and sample.apply(infer_date).notna().mean() > 0.9:
        return 'datetime64[ns]'

    if len(non_null.unique()) / len(non_null) < 0.1 and len(non_null) > 100:
        return 'category'
    
    return 'object'

def convert_column_type(column: pd.Series, inferred_type: str) -> pd.Series:
    """Convert a column to the inferred data type, handling conversion errors."""
    try:
        if inferred_type == 'datetime64[ns]':
            return pd.to_datetime(column, errors='coerce')
        elif inferred_type == 'category':
            return column.astype('category')
        elif inferred_type == 'boolean':
            if column.dtype != 'bool':
                return column.map({'1': True, '0': False, 'true': True, 'false': False, 'True': True, 'False': False}).astype('boolean')
            return column.astype('boolean')
        elif inferred_type in ['int64', 'float64']:
            return pd.to_numeric(column, errors='coerce')
        else:
            return column.astype(inferred_type)
    except Exception as e:
        print(f"Error converting column: {e}")
        return column

def process_chunk(chunk: pd.DataFrame, dtypes: Dict[str, str]) -> pd.DataFrame:
    """Process a chunk of data, converting columns to inferred types."""
    for col in chunk.columns:
        if col in dtypes:
            chunk[col] = convert_column_type(chunk[col], dtypes[col])
    return chunk

def infer_and_convert_types(file_path: str, chunk_size: int = 100000) -> Tuple[pd.DataFrame, Dict]:
    """Infer and convert data types from a file"""
    file_ext = os.path.splitext(file_path)[1].lower()
    read_func = pd.read_csv if file_ext == '.csv' else pd.read_excel if file_ext in ('.xls', '.xlsx') else None

    if read_func is None:
        raise ValueError(f"Unsupported file type: {file_ext}")

    try:
        initial_chunk = read_func(file_path, nrows=chunk_size)
        inferred_dtypes = {col: infer_column_type(initial_chunk[col]) for col in initial_chunk.columns}

        chunks = []
        reader = read_func(file_path, chunksize=chunk_size)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_chunk, chunk, inferred_dtypes): chunk for chunk in reader}
            for future in concurrent.futures.as_completed(futures):
                chunks.append(future.result())

        df = pd.concat(chunks, ignore_index=True)
        metadata = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'null_counts': df.isna().sum().to_dict(),
            'unique_counts': {col: df[col].nunique() for col in df.columns},
            'memory_usage': df.memory_usage(deep=True).sum(),
            'dtypes': df.dtypes.apply(lambda x: x.name).to_dict()
        }
        return df, metadata

    except Exception as e:
        raise ValueError(f"Error processing file: {e}")