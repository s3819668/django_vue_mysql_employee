from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import  JsonResponse
from EmployeeApp.models import Departments,Employees
from EmployeeApp.serializers import DepartmentSerializer,EmployeeSerializer
# Create your views here.

@csrf_exempt
def departmentApi(request,id=0):
    if request.method=='GET':
        departments=Departments.objects.all()
        departments_serializers=DepartmentSerializer(departments,many=True)
        return JsonResponse(departments_serializers.data,safe=False)
    elif request.method=='POST':
        department_data=JSONParser().parse(request)
        departments_serializers=DepartmentSerializer(data=department_data)
        if departments_serializers.is_valid():
            departments_serializers.save()
            return JsonResponse('Added Successfully',safe=False)
        return JsonResponse('Failed to Add',safe=False)
    elif request.method=='PUT':
        department_data=JSONParser().parse(request)
        department=Departments.objects.get(DepartmentId=department_data['DepartmentId'])
        departments_serializers=DepartmentSerializer(department,data=department_data)
        if departments_serializers.is_valid():
            departments_serializers.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        department=Departments.objects.get(DepartmentId=id)
        department.delete()
        return JsonResponse('Deleted Successfully',safe=False)
    return JsonResponse('Failed to Delete',safe=False)

@csrf_exempt
def employeeApi(request,id=0):
    if request.method=='GET':
        departments=Departments.objects.all()
        departments_serializers=DepartmentSerializer(departments,many=True)
        return JsonResponse(departments_serializers.data,safe=False)
    elif request.method=='POST':
        department_data=JSONParser().parse(request)
        departments_serializers=DepartmentSerializer(data=department_data)
        if departments_serializers.is_valid():
            departments_serializers.save()
            return JsonResponse('Added Successfully',safe=False)
        return JsonResponse('Failed to Add',safe=False)
    elif request.method=='PUT':
        department_data=JSONParser().parse(request)
        department=Departments.objects.get(DepartmentId=department_data['DepartmentId'])
        departments_serializers=DepartmentSerializer(department,data=department_data)
        if departments_serializers.is_valid():
            departments_serializers.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        department=Departments.objects.get(DepartmentId=id)
        department.delete()
        return JsonResponse('Deleted Successfully',safe=False)
    return JsonResponse('Failed to Delete',safe=False)













