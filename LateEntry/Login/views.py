from django import forms
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    Choices = [('Student', 'Student'), ('Warden', 'Warden'), ('Guard', 'Guard')]
    choices = forms.ChoiceField(choices=Choices)


# Create your views here.
class LoginView(View):
    def get(self, request):

        # print(LoginForm())
        return render(request, "guard.html")

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            choice = form.cleaned_data['choices']

            auth = authenticate(username=username, password=password, role=choice)
            if auth is not None:
                login(request, auth)
                if choice == 'Warden':
                    return redirect('warden')
                elif choice == 'Guard':
                    return redirect('guard')
                elif choice == 'Student':
                    return redirect('student')

            else:
                return redirect('login')

        else:
            print(form.errors)
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')