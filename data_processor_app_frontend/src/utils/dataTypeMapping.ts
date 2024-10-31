export const dataTypeMapping: { [key: string]: string } = {
    'integer': 'Integer',
    'float': 'Decimal',
    'boolean': 'Boolean',
    'object': 'Alphanumeric',
    'category': 'Category',
    'datetime': 'Date/Time',
    'string': 'Text',
    'numerical': 'Number',
    'percentage': 'Percentage',
  };


  export const conversionRules: { [key: string]: string[] } = {
    'Integer': ['Integer', 'Decimal', 'Boolean', 'Alphanumeric', 'Number'],
    'Decimal': ['Decimal', 'Boolean', 'Alphanumeric', 'Number'],
    'Boolean': ['Boolean', 'Alphanumeric'],
    'Alphanumeric': ['Alphanumeric'],
    'Category': ['Category', 'Alphanumeric', 'Text'],
    'Date/Time': ['Date/Time', 'Alphanumeric', 'Text'],
    'Time Duration': ['Time Duration', 'Alphanumeric', 'Text'],
    'Text': ['Text', 'Alphanumeric', 'Category'],
    'Number': ['Number', 'Integer', 'Decimal', 'Boolean', 'Alphanumeric'],
    'Percentage': ['Percentage', 'Integer', 'Decimal', 'Boolean', 'Alphanumeric', 'Number'],
  };