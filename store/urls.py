from django.urls import path
from . import views


urlpatterns = [
     path ('', views.store , name="store"),
     path ('cart/', views.cart , name="cart"),
     path ('checkout/', views.checkout , name="checkout"),
     path ('updateitem/', views.updateItem , name="updateitem"),
     path ('processorder/', views.processOrder , name="processorder"),
     path('register/',views.registerPage,name="register"),
     path('login/',views.loginPage,name="login"),
]
