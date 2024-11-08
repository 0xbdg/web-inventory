from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
        path("accounts/login/",views.signin,name="login"),
        path("accounts/signup",views.register, name="register"),
        path("accounts/logout/",views.logouts,name="logout"),
        path("accounts/password_change/",views.change_password,name="password_change"),
        path("accounts/password_reset/",auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),name="password_reset"),
        path("accounts/password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
        path("accounts/reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
        path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
        path("",views.home, name="home"),
        path("category/",views.category,name="category"),
        path("category/<uuid:item_id>/",views.category_detail,name="category-detail"),
        path("profile/",views.profile, name="profile"),
        path("lending/",views.lending,name="lending"),
        path("history/",views.history,name="history")
]
