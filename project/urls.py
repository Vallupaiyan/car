"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apple import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexView.as_view(), name="home"),

    path('collection/', views.CollectionView.as_view(), name="collection"),

    path('about/', views.AboutView.as_view(), name="about"),

    path('index/', views.IndexView.as_view(), name="index"),

    path('service/', views.ServiceView.as_view(), name="service"),

    path('contact/', views.ContactView.as_view(), name="contact"),

    path('login/', views.LoginView.as_view(), name="login"),

    path('register/', views.RegisterView.as_view(), name="register"),

    path('save/', views.CustomerSaveView.as_view(), name="customer_save"),

    path('check-login/', views.check_login_details, name="check_login"),

    path('bynow/', views.BynowView.as_view(), name='bynow'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('create-order/', views.CreateOrderView.as_view(), name="create_order"),

    path('verify-payment/', views.VerifyPaymentView.as_view(), name="verify_payment"),

    path('payment-success/', views.PaymentSuccessView.as_view(), name="payment_success"),
    path('logout/', views.logout_view, name="logout"),
]