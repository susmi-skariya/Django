from django.urls import path
from . import views


urlpatterns = [
    path("",views.home,name="home"),
    path("about1/",views.about,name="about"),
    path("contact/",views.contact,name="Contact"),
    path("view/",views.view,name="view"),
    path("createbook/",views.createbook,name="createbook"),
    path("update/<int:id>",views.update,name="update"),
    path("delete/<int:id>",views.delete,name="delete"),
    path("register/",views.Register,name="reg"),
    path("login/",views.LoginForm,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("cart/",views.cart,name="cart"),
    path("add_cart/<int:book_id>",views.add_cart,name="add"),
   
]
