from django.shortcuts import render
from .models import Project
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer


def portfolio_home(request):
    projects = Project.objects.all()
    return render(request, 'portfolio/portfolio.html', {'projects': projects})



@api_view(['GET', 'POST'])
def project_list_create(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)