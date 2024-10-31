export const dataTypeMapping: { [key: string]: string } = {
    'integer': 'Integer',
    'float': 'Decimal',
    'boolean': 'Boolean',
    'object': 'Alphanumeric',
    'category': 'Category',
    'datetime': 'Date/Time',
    'string': 'Text',
    'numerical': 'Number',
    'complex': 'Complex Number',
    'percentage': 'Percentage',
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
    'Percentage': ['Percentage', 'Integer', 'Decimal', 'Boolean', 'Alphanumeric', 'Number'],
  };