from django.urls import path
from . import views

urlpatterns = [

   #Auth
   path('', views.signupuser, name='signupuser'),
   path('current/', views.currenttodos, name='currenttodos'),
   path('logout/', views.logoutuser, name='logoutuser'),
   path('login/', views.loginuser, name='loginuser'),
   path('create/', views.createtodo, name='createtodo'),
   path('completed/', views.completed, name='completed'),
   path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
   path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
   path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
]