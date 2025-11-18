from django import forms
from django.shortcuts import render, redirect
from django.views import View

import mysql.connector

from LateEntry.credentialManager import CredentialManager as cm

connection = mysql.connector.connect(user=cm.user, password=cm.password, host=cm.host, database=cm.database,
                                     autocommit=True)


class Record:
    def __init__(self, rollNumber, date, time, reason, penalty, guardID):
        self.rollNumber = rollNumber
        self.date = date
        self.time = time
        self.reason = reason
        self.penalty = penalty
        self.guardID = guardID


class ViewDataFormRoll(forms.Form):
    rollNumber = forms.IntegerField(required=False)


class ViewDataFormDate(forms.Form):
    date = forms.DateField(required=False)


# Create your views here.
class ViewPreviousData(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.email in ['Guard', 'Warden']:
            return render(request, 'view.html')
        else:
            return redirect('login')


class ViewPreviousDataRoll(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.email in ['Guard', 'Warden']:
            return render(request, 'view.html')
        else:
            return redirect('login')

    def post(self, request):
        user = request.user
        if user.is_authenticated and user.email in ['Guard', 'Warden']:
            form = ViewDataFormRoll(request.POST)
            if form.is_valid():
                rollNumber = form.cleaned_data['rollNumber']
                print(rollNumber)
                with connection.cursor() as cursor:
                    cursor.execute(
                        'SELECT roll_no,entry_date,entry_time,reason,penalty_type,g_id FROM entry_info WHERE roll_no = %s',
                        (rollNumber,))
                    records = []
                    for row in cursor.fetchall():
                        records.append(Record(row[0], row[1], row[2], row[3], row[4], row[5]))

                return render(request, 'view.html', {'records': records})
        else:
            return redirect('login')


class ViewPreviousDataDate(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.email in ['Guard', 'Warden']:
            return render(request, 'view.html')
        else:
            return redirect('login')

    def post(self, request):
        user = request.user
        if user.is_authenticated and user.email in ['Guard', 'Warden']:

            form = ViewDataFormDate(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                with connection.cursor() as cursor:
                    cursor.execute(
                        'SELECT roll_no,entry_date,entry_time,reason,penalty_type,g_id FROM entry_info WHERE entry_date = %s',
                        (date,))
                    records = []
                    for row in cursor.fetchall():
                        records.append(Record(row[0], row[1], row[2], row[3], row[4], row[5]))

                return render(request, 'view.html', {'records': records})
        else:
            return redirect('login')
class PermissionRecord():
    def __init__(self,rollNumber,date,time,status,w_id) -> None:
            self.rollNumber = rollNumber
            self.date = date
            self.time = time
            self.permission = 'Granted' if status else 'Rejected'
            self.wardenID = w_id

class PermissionView(View):
    def get(self,request):
        user = request.user
        if user.is_authenticated and user.email in ['Guard', 'Warden']:
            with connection.cursor() as cursor:
                    cursor.execute(
                        'SELECT rollNumber,date,time,status,w_id FROM permission ORDER BY date desc;')
                    records = []
                    for row in cursor.fetchall():
                        records.append(PermissionRecord(row[0], row[1], row[2], row[3], row[4]))
            return render(request,'permissionView.html',{'records':records})
        else:
            return redirect('login')