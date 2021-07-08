from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .form import TodoForm,RegisterForm,SigninForm
from .models import Todo,visitor
from django.utils import timezone
from django.contrib.auth.decorators import login_required



def signupuser(request):
	if request.method=='GET':
		return render(request, 'todo/signupuser.html', {'form':RegisterForm()})
	else:
		if request.POST['password']==request.POST['confirm_password']:
			try:
				if len(request.POST['password'])<8:
					return render(request, 'todo/signupuser.html', {'form':RegisterForm(), 'error':'weak password! Try again'})
				else:	
					user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
					user.save()
					login(request,user)
					return redirect('currenttodos')
			except IntegrityError:
				return render(request, 'todo/signupuser.html', {'form':RegisterForm(), 'error':'Username already taken. Try again'})				
		else:
			return render(request, 'todo/signupuser.html', {'form':RegisterForm(), 'error':'Password did not match'})


@login_required
def currenttodos(request):
	todos = Todo.objects.filter(user = request.user, datecompleted__isnull = True)
	return render(request, 'todo/currenttodos.html', {'todos':todos})			

@login_required
def logoutuser(request):
	if request.method=='POST':
		logout(request)
		return redirect('signupuser')

@login_required
def viewtodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	if request.method=='GET':
		form = TodoForm(instance=todo)
		return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
	else:
		try:
			form = TodoForm(request.POST, instance=todo)
			form.save()
			return redirect('currenttodos')
		except ValueError:
			return render(request, 'todo/currenttodos.html', {'form':form, 'todo':todo,  'error':'Bad data passed in! Try again'})	

@login_required
def deletetodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	if request.method=='POST':
		todo.delete()
		return redirect('currenttodos')

@login_required		
def completetodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	if request.method=='POST':
		todo.datecompleted = timezone.now()
		todo.save()
		return redirect('currenttodos')

@login_required		
def completed(request):
	todos = Todo.objects.filter(user = request.user, datecompleted__isnull = False).order_by('-datecompleted')
	return render(request, 'todo/completed.html', {'todos':todos})	

def loginuser(request):
	if request.method=='GET':
		return render(request, 'todo/loginuser.html', {'form':SigninForm()})
	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])		
		if user is None:
			return render(request, 'todo/loginuser.html', {'form':SigninForm(), 'error':'username and password did not match'})
		else:
			login(request, user)
			return redirect('currenttodos')

@login_required
def createtodo(request):
	if request.method=='GET':
		return render(request, 'todo/createtodo.html', {'form':TodoForm()})
	else:
		try:
			form = TodoForm(request.POST)
			newtodo = form.save(commit=False)
			newtodo.user = request.user
			newtodo.save()
			return redirect('currenttodos')
		except ValueError:
			return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in! Try again'})		
			
			 		
		 			