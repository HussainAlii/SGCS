from django.urls import path
from .views import signin, forgetPassword, signup, resetPassword, signout

urlpatterns = [
    path('', signin, name="signin"),
    path('forgetPassword/', forgetPassword, name="forgetPassword"),
    path('signup/', signup, name="signup"),
    path('resetPassword/', resetPassword, name="resetPassword"),
    path('signout/', signout, name="signout"),
]
