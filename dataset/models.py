import csv
import io
from django.db import models
from django.contrib.auth.models import User
import datetime
from .signals import csv_uploaded
from .validators import csv_file_validator
from django.db.models.signals import pre_save, post_save
from datetime import datetime

# Create your models here.
class Municipios(models.IntegerChoices):
    MACAPA =            1, ('MACAPÁ')
    SANTANA =           2, ('SANTANA')
    LARANJAL_DO_JARI =  3, ('LARANJAL DO JARI')
    OIAPOQUE =          4, ('OIAPOQUE')
    MAZAGAO =           5, ('MAZAGÃO')
    PORTO_GRANDE =      6, ('PORTO GRANDE')
    TARTARUGALZINHO =   7, ('TARTARUGALZINHO')
    VITORIA_DO_JARI =   8, ('VITORIA DO JARI')
    PEDRA_BRANCA_DO_AMAPARI = 9, ('PEDRA BRANCA DO AMAPARI')
    CALCOENE =          10, ('CALÇOENE')
    AMAPA =             11, ('AMAPÁ')
    FERREIRA_GOMES =    12, ('FERREIRA GOMES') 
    CUTIAS_DO_ARAGUARY = 13, ('CUTIAS DO ARAGUARY')
    SERRA_DO_NAVIO =    14, ('SERRA DO NAVIO')
    ITAUBAL =           15, ('ITAUBAL')
    PRACUUBA =          16, ('PRACUUBA')


class Registro(models.Model):
    
    cidade = models.IntegerField("Cidade", choices=Municipios.choices)
    data        = models.DateField("Data do Registro")
    suspeitos   = models.IntegerField('Qtd Suspeitos', blank=True, null=True)
    confirmados = models.IntegerField('Qtd Confirmados', blank=True, null=True)
    descartados = models.IntegerField('Qtd Descartados', blank=True, null=True)
    recuperados = models.IntegerField('Qtd Recuperados', blank=True, null=True)
    obitos      = models.IntegerField('Qtd obitos', blank=True, null=True)


    class Meta:
        verbose_name        = "Registro"
        verbose_name_plural ="Registros"

    def __str__(self):
        return "Dados"

def upload_csv_file(instance, filename):
    qs = instance.__class__.objects.filter(user=instance.user)
    if qs.exists():
        num_ = qs.last().id + 1
    else:
        num_ = 1
    return f'csv/{num_}/{instance.user.username}/{filename}'

def create_registro(dados):
    registro = Registro.objects.create(
        cidade=dados['cidade'],
        data=dados['data'],
        suspeitos=dados['suspeitos'],
        confirmados=dados['confirmados'],
        descartados=dados['descartados'],
        recuperados=dados['recuperados'],
        obitos=dados['obitos'],
    )
    registro.save()



class CSVUpload(models.Model):
    nome        =   models.TextField("Nome", max_length=100)
    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    arquivo     =   models.FileField(upload_to=upload_csv_file,  validators=[csv_file_validator])
    completo    =   models.BooleanField(default=False)

    class Meta:
        verbose_name    =   "Arquivo"

    def __str__(self):
        return self.nome


def csv_upload_post_save(sender, instance, created, *args, **kwargs):
    if not instance.completo:
        csv_file = instance.arquivo
        decoded_file = csv_file.read().decode('utf-8-sig')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=';', quotechar='|')
        header_ = next(reader)
        header_cols = header_
        
        parsed_items = []
        
        for line in reader:

            parsed_row_data = {}
            i = 0
            row_item = line

            for item in row_item:
                key = header_cols[i]
                parsed_row_data[key] = item
                i+=1
            create_registro(parsed_row_data)
            parsed_items.append(parsed_row_data)
            # messages.success(parsed_items)
            print(parsed_items)
        csv_uploaded.send(sender=instance, user=instance.user, csv_file_list=parsed_items)


        instance.completo = True
        instance.save()

post_save.connect(csv_upload_post_save, sender=CSVUpload)