from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Registro
from .serializers import RegistroSerializer

@api_view(['GET'])
def lista_registros(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        registros = Registro.objects.all().order_by('data')
        page = request.GET.get('page', 1)
        paginator = Paginator(registros, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = RegistroSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/registros/?page=' + str(nextPage), 'prevlink': '/api/registros/?page=' + str(previousPage)})

    elif request.method == 'POST':
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
