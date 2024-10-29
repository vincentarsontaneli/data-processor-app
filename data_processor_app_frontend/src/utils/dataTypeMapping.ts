export const dataTypeMapping: { [key: string]: string } = {
    'int64': 'Integer',
    'int32': 'Integer',
    'float64': 'Decimal',
    'float32': 'Decimal',
    'bool': 'Boolean',
    'object': 'Alphanumeric',
    'category': 'Category',
    'datetime64[ns]': 'Date/Time',
    'timedelta[ns]': 'Time Duration',
    'string': 'Text',
    'numerical': 'Number',
    'complex': 'Complex Number',
  };


  export const conversionRules: { [key: string]: string[] } = {
    'Integer': ['Integer', 'Decimal', 'Boolean', 'Alphanumeric', 'Number', 'Complex Number'],
    'Decimal': ['Integer', 'Decimal', 'Boolean', 'Alphanumeric', 'Number', 'Complex Number'],
    'Boolean': ['Integer', 'Decimal', 'Boolean', 'Alphanumeric', 'Number'],
    'Alphanumeric': ['Alphanumeric', 'Text'],
    'Category': ['Category', 'Alphanumeric', 'Text'],
    'Date/Time': ['Date/Time', 'Alphanumeric', 'Text'],
    'Time Duration': ['Time Duration', 'Alphanumeric', 'Text'],
    'Text': ['Text', 'Alphanumeric', 'Category'],
    'Number': ['Number', 'Integer', 'Decimal', 'Boolean', 'Alphanumeric', 'Complex Number'],
    'Complex Number': ['Complex Number', 'Alphanumeric', 'Text'],
  };