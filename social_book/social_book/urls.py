from django.contrib import admin
from django.urls import path,include
from users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.RegisterPage,name='register'),
    path('signin/',views.SigninPage,name='signin'),
    path('index/',views.IndexPage,name='home'),
    path('authors-and-sellers/', views.authors_and_sellers, name='authors_and_sellers'),
    path('upload-book/', views.upload_book, name='upload_book'),
    path('uploaded_files/', views.custom_uploaded_files_wrapper, name='custom_uploaded_files'),
    path('uploaded-files/', views.uploaded_files, name='uploaded_files'),
    path('logout/',views.LogoutPage,name='logout'),
    path('api/', include('users.urls')),
    path('api/uploaded_files/', views.get_uploaded_files, name='get_uploaded_files'),
    

    #path('',views.SignupPage,name='signup'),
    #path('login/',views.LoginPage,name='login'),
    #path('home/',views.HomePage,name='home'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
