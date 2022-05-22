# django vue restful API
# 起始篇
## 安裝django
`pip install django`
## 安裝restframework
`pip install djangorestframework`
## 安裝django-cors-headers 防止CSRF
`pip install django-cors-headers`
## 建立project 
`django-admin startproject DjangoAPI`

cmd:`cd DjangoAPI`
cmd:`python manage.py runserver`
chrome: 127.0.0.1:8000

## 建立app
`python manage.py startapp EmployeeApp`

# 匯入需要用的APPS
## path:DjangoAPI/setting.py 

## 匯入apps rest_framework,corsheaders ,EmployeeApp.apps.EmployeeappConfig[-3:]
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'corsheaders',
        'EmployeeApp.apps.EmployeeappConfig',
    ]

## 匯入中介程式 corsheaders.middleware.CorsMiddleware[0]
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

## 開放全網域存取API
    CORS_ORIGIN_ALLOW_ALL =True

# 建立資料庫篇
## path:DjangoAPI/EmployeeApp/models.py
## 建立資料表以利遷移
    class Departments(models.Model):
        DepartmentId=models.AutoField(primary_key=True)
        DepartmentName=models.CharField(max_length=500)
    class Employees(models.Model):
        EmployeeId=models.AutoField(primary_key=True)
        EmployeeName=models.CharField(max_length=500)
        Department=models.CharField(max_length=500)
        DateOfJoining=models.DateField()
        PhotoFileName=models.CharField(max_length=500)

# XAMPP:mysql 
## 新增資料庫mytestdb

# path:DjangoAPI/setting.py 
## 匯入pymysql,ENGINE改成mysql及登入相關設定
    import pymysql
    pymysql.install_as_MySQLdb()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mytestdb',
            'USER': 'root',
            'PASSWORD':'',
            'HOST':'127.0.0.1',
            'PORT':3306
        }
    }

## 建立EmployeeApp中models遷移紀錄
cmd:`python manage.py makemirgations EmployeeApp`
![](https://i.imgur.com/jFw5v1e.png)
產生遷移紀錄

## 將遷移表作用於資料庫
cmd$`python manage.py migrate EmployeeApp`
![](https://i.imgur.com/RJO8Hgo.png)
資料表已經自動完成

# 資料序列化篇
## path:DjangoAPI/EmployeeApp
## 建立serializers.py檔案 --資料進行序列化
## path:DjangoAPI/EmployeeApp/serializers.py
    from rest_framework import serializers
    from EmployeeApp.models import Departments,Employees
    class DepartmentSerializer(serializers.ModelSerializer):
        class Meta:
            model=Departments
            fields=('DepartmentId','DepartmentName')

    class EmployeeSerializer(serializers.ModelSerializer):
        class Meta:
            model=Employees
            fields=('EmployeeId','EmployeeName','Department','DateOfJoining','PhotoFileName')
# 部門CRUD API篇
## path:DjangoAPI/EmployeeApp/views.py
    from django.shortcuts import render
    from django.views.decorators.csrf import csrf_exempt
    from rest_framework.parsers import JSONParser
    from django.http.response import  JsonResponse
    from EmployeeApp.models import Departments,Employees
    from EmployeeApp.serializers import DepartmentSerializer,EmployeeSerializer
    #實作crud操作
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

## path:DjangoAPI/urls.py --將根目錄路由到EmployeeApp的url下 
    from django.contrib import admin
    from django.urls import path
    from django.urls import include, re_path
    urlpatterns = [
        path('admin/', admin.site.urls),
        re_path(r'^',include('EmployeeApp.urls'))
    ]

## path:DjangoAPI/EmployeeApp
## 建立urls.py
## path:DjangoAPI/EmployeeApp/urls.py --將department路由到API 以使用views中的departmentApi實現CRUD
    from django.urls import include, re_path#django4 中用來取代url
    from EmployeeApp import views

    urlpatterns=[
        re_path(r'^department$',views.departmentApi),
        re_path(r'^department/([0-9]+)$',views.departmentApi)
    ]

# 員工CRUD API篇
## path:DjangoAPI/EmployeeApp/views.py --新增CRUD員工部分
    @csrf_exempt
    def employeeApi(request,id=0):
        if request.method=='GET':
            employees=Employees.objects.all()
            employees_serializers=EmployeeSerializer(employees,many=True)
            return JsonResponse(employees_serializers.data,safe=False)
        elif request.method=='POST':
            employee_data=JSONParser().parse(request)
            employees_serializers=EmployeeSerializer(data=employee_data)
            if employees_serializers.is_valid():
                employees_serializers.save()
                return JsonResponse('Added Successfully',safe=False)
            return JsonResponse('Failed to Add',safe=False)
        elif request.method=='PUT':
            employee_data=JSONParser().parse(request)
            employee=Employees.objects.get(EmployeeId=employee_data['EmployeeId'])
            employees_serializers=EmployeeSerializer(employee,data=employee_data)
            if employees_serializers.is_valid():
                employees_serializers.save()
                return JsonResponse("Updated Successfully",safe=False)
            return JsonResponse("Failed to Update", safe=False)
        elif request.method == 'DELETE':
            employee=Employees.objects.get(EmployeeId=id)
            employee.delete()
            return JsonResponse('Deleted Successfully',safe=False)
        return JsonResponse('Failed to Delete',safe=False)
## path:DjangoAPI/EmployeeApp/urls.py --將Employee加入路由到API 以使用views中的employeeApi 實現CRUD
    from django.urls import include, re_path
    from EmployeeApp import views

    urlpatterns=[
        re_path(r'^department$',views.departmentApi),
        re_path(r'^department/([0-9]+)$',views.departmentApi),
        re_path(r'^employee$',views.employeeApi),
        re_path(r'^employee/([0-9]+)$',views.employeeApi)
    ]
# 照片API篇
## path:DjangoAPI
## 新增一個資料夾Photos放置照片 

## path:DjangoAPI/setting.py 加入

    import os
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    MEDIA_URL='/Photos/'
    MEDIA_ROOT=os.path.join(BASE_DIR,'Photos')

## path:DjangoAPI/EmployeeApp/veiws --匯入檔案模組及建置存檔API

    from django.core.files.storage import default_storage

    @csrf_exempt
    def SaveFile(request):
        file=request.FILES['file']
        file_name=default_storage.save(file.name,file)
        return JsonResponse(file_name,safe=False)

## path:DjangoAPI/EmployeeApp/urls.py
    from django.urls import include, re_path
    from EmployeeApp import views
    from django.conf.urls.static import static
    from django.conf import settings
    urlpatterns=[
        re_path(r'^department$',views.departmentApi),
        re_path(r'^department/([0-9]+)$',views.departmentApi),
        re_path(r'^employee$',views.employeeApi),
        re_path(r'^employee/([0-9]+)$',views.employeeApi),
        re_path(r'^employee/SaveFile',views.SaveFile)


    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


