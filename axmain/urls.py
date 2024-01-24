"""axmain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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


from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [
    path('department/', include('modules.department.urls', namespace='department')),
    path('venture/', include('modules.venture.urls', namespace='venture')),
    path('zoom_meeting/', include('modules.zoom_meeting.urls', namespace='zoom_meeting')),
    path('social_auth/', include('modules.social_auth.urls', namespace='social_auth')),
    path('admin/', include('modules.frontend.admindashboard.urls', namespace='admindashboard')),
    path('account/', include('modules.frontend.account.urls', namespace='account')),
    path('', include('modules.frontend.axhome.urls', namespace='axhome')),
    path('gst/', include('modules.gst.urls', namespace='gst'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/',
             include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
