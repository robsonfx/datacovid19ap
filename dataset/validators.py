import csv
import os
import io

from django.core.exceptions import ValidationError

REQUIRED_HEADER  = ['cidade','data','suspeitos','confirmados','descartados','recuperados','obitos']

def csv_file_validator(value):
    filename, ext = os.path.splitext(value.name)
    if  str(ext) != '.csv':
         raise ValidationError("Você não enviou um aquivo com extensão csv")
    decoded_file = value.read().decode('utf-8-sig')
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string, delimiter=';', quotechar='|')
    
    header_ = next(reader)
    
    if header_[-1] == '':
        header_.pop()
    required_header = REQUIRED_HEADER
    # raise Exception(header_)
    if required_header != header_:
        raise ValidationError("Arquivo inválido. o cabeçalho do aquivo deve conter data ,suspeitos, descartados, confirmados, recuperados, obitos .")
    return True