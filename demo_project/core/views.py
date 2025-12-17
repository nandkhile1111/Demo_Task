from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Expense
from .serializers import ExpenseSerializer
import requests
from django.db.models import Sum
from django.shortcuts import render


# ===================================================A basic CRUD =====================================================
# Create and Read 
@api_view(['GET', 'POST'])
def expense_list_create(request):
    if request.method == 'GET':
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


# unique read, upadte and delete
@api_view(['GET', 'PUT', 'DELETE'])
def expense_detail(request, id):
    try:
        expense = Expense.objects.get(id=id)
    except Expense.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        expense.delete()
        return Response({'message': 'Deleted'}, status=204)

# ===================================================Third-party API Data Pulling =====================================================

# wether api
@api_view(['GET'])
def weather_api(request,city):
    # city = request.GET.get('city', 'Mumbai')
    print("city=============",city)
    api_key = '0990541fe91e971b1aaafaa9c9b47f0e'

    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    print("Response========",response)
    return Response(response.json())


# ===================================================A simple data visualization  =====================================================

# Visualization data
def expense_report(request):
    data = Expense.objects.values('category').annotate(total=Sum('amount'))
    print("report data===========",data)
    return render(request, 'report.html', {'data': data})
