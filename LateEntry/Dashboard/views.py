from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django import forms
from DeleteData.views import connection


class DashboardView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.email == 'Guard':
                return redirect('guard')
            elif user.email == 'Warden':
                return redirect('warden')
            else:
                return redirect('student')
        else:
            return redirect('login')


class GuardDashBoardView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.email == "Guard":
            return render(request, 'guard_dashboard.html')
        else:
            return redirect('login')


class StudentForm(forms.Form):
    rollNumber = forms.IntegerField()
    date = forms.DateField()
    time = forms.TimeField()


class StudentDashBoardView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.email == "Student":
            return render(request, 'student.html')
        else:
            return redirect('login')

    def post(self, request):
        user = request.user
        if user.is_authenticated and user.email == "Student":
            form = StudentForm(request.POST)
            if form.is_valid():
                rollNumber = form.cleaned_data['rollNumber']
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                with connection.cursor() as cursor:

                    cursor.execute(
                        f"INSERT INTO permission (rollNumber, date, time) VALUES ({rollNumber}, '{date}', '{time.strftime('%H:%M:%S')}')")

                    return HttpResponse("Form Submitted")
            return redirect('student')
        return redirect('login')


class WardenDashBoardView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.email == "Warden":
            return render(request, 'warden_dashboard.html')
        else:
            return redirect('login')


class Permission:
    def __init__(self, permissionID, rollNumber, time, date):
        self.permissionID = permissionID
        self.rollNumber = rollNumber
        self.time = time
        self.date = date


class WardenGrantView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.email == "Warden":
            with connection.cursor() as cursor:
                cursor.execute('SELECT permissionID,rollNumber,time,date FROM permission where status is NULL;')
                permissions = []
                for result in cursor.fetchall():
                    permissions.append(Permission(result[0], result[1], result[2], result[3]))

            return render(request, 'warden_grant.html', context={'permissions': permissions})


class GrantedPermissionView(View):
    def get(self, request, permissionID):
        user = request.user
        if user.is_authenticated and user.email == "Warden":
            with connection.cursor() as cursor:
                cursor.execute(
                    f"UPDATE permission SET status=TRUE,  w_id = {user.username[:-1]} WHERE permissionID={permissionID}")
        return redirect('grant')


class RejectedPermissionView(View):
    def get(self, request, permissionID):
        user = request.user
        if user.is_authenticated and user.email == "Warden":
            print(user.username)
            with connection.cursor() as cursor:
                cursor.execute(
                    f"UPDATE permission SET status=FALSE,  w_id = {user.username[:-1]} WHERE permissionID={permissionID}")
        return redirect('grant')
