"""
URL configuration for tft_django project.

The `urlpatterns` list routes URLs to api. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function api
    1. Add an import:  from my_app import api
    2. Add a URL to urlpatterns:  path('', api.home, name='home')
Class-based api
    1. Add an import:  from other_app.api import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tft/', include('tft.urls')),
    path('query/', include('tft_selenium.urls')),
    path('ml/', include('tft_ml.urls'))
]
