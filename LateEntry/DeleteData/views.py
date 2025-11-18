from django import forms
from django.shortcuts import render, redirect
from django.views import View
import mysql.connector
from LateEntry.credentialManager import CredentialManager as cm

connection = mysql.connector.connect(user=cm.user, password=cm.password, host=cm.host, database=cm.database,
                                     autocommit=True)


class DeleteForm(forms.Form):
    rollNumber = forms.CharField(required=True)
    date = forms.DateField(required=True)


# Create your views here.
class DeleteDataView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.email == "Guard":
            return render(request, 'delete.html')
        else:
            return redirect('login')

    def post(self, request):
        user = request.user
        if user.is_authenticated and user.email == "Guard":
            form = DeleteForm(request.POST)
            if form.is_valid():
                rollNumber = form.cleaned_data['rollNumber']
                date = form.cleaned_data['date']
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM entry_info WHERE roll_no = %s and entry_date = %s",
                                   (rollNumber, date))
                return redirect('delete')
            else:
                return redirect('delete')
        else:
            return redirect('login')
