"""laxy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, path, include, register_converter
from django.contrib import admin

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from laxy_backend.views import (JobView, JobCreate,
                                FileCreate, FileView,
                                FileSetCreate, FileSetView,
                                SampleSetCreate, SampleSetView,
                                ComputeResourceView, ComputeResourceCreate,
                                ENAQueryView, ENAFastqUrlQueryView, )

from laxy_backend.view_auth import Login, Logout, view_user_profile

from laxy_backend.view_event import Events

app_name = 'laxy_backend'


# See: https://docs.djangoproject.com/en/2.0/topics/http/urls/#registering-custom-path-converters
class UUID62Converter:
    """
    For capturing Base62 encoded UUIDs from URLs.
    """
    regex = '[a-zA-Z0-9\-_]+'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return value


register_converter(UUID62Converter, 'uuid62')

api_urls = [
    # New format Django URLs - disabled until drf_openapi can properly format
    # them without escaping backslashes
    #
    # path('job/<uuid62:job_id>/',
    #     JobView.as_view(),
    #     name='job'),
    # path('job/',
    #     JobCreate.as_view(),
    #     name='create_job'),
    # path(
    #     'compute_resource/<uuid62:uuid>/',
    #     ComputeResourceView.as_view(),
    #     name='compute_resource'),
    # path('compute_resource/',
    #     ComputeResourceCreate.as_view(),
    #     name='compute_resource'),
    # path('event/',
    #     Events.as_view(),
    #     name='event'),

    re_path(r'auth/login/$',
            Login.as_view(),
            name='api_login'),
    re_path(r'auth/logout/$',
            Logout.as_view(),
            name='api_logout'),

    re_path(r'job/(?P<job_id>[a-zA-Z0-9\-_]+)/$',
            JobView.as_view(),
            name='job'),
    re_path(r'job/$',
            JobCreate.as_view(),
            name='create_job'),
    re_path(r'file/$',
            FileCreate.as_view(),
            name='create_file'),
    re_path(r'file/(?P<uuid>[a-zA-Z0-9\-_]+)/$',
            FileView.as_view(),
            name='file'),
    re_path(r'fileset/(?P<uuid>[a-zA-Z0-9\-_]+)/$',
            FileSetView.as_view(),
            name='fileset'),
    re_path(r'fileset/$',
            FileSetCreate.as_view(),
            name='create_fileset'),
    re_path(r'sampleset/(?P<uuid>[a-zA-Z0-9\-_]+)/$',
            SampleSetView.as_view(),
            name='sampleset'),
    re_path(r'sampleset/$',
            SampleSetCreate.as_view(),
            name='create_sampleset'),
    re_path(
        r'compute_resource/(?P<uuid>[a-zA-Z0-9\-_]+)/$',
        ComputeResourceView.as_view(),
        name='compute_resource'),
    re_path(r'compute_resource/$',
            ComputeResourceCreate.as_view(),
            name='compute_resource'),
    re_path(r'event/$',
            Events.as_view(),
            name='event'),

    re_path(r'ena/$',
            ENAQueryView.as_view(),
            name='ena_query'),
    re_path(r'ena/fastqs/$',
            ENAFastqUrlQueryView.as_view(),
            name='ena_fastq_ulr_query'),
]

urlpatterns = [
    re_path('^accounts/profile/', view_user_profile),

    # re_path(r'^api/(?P<version>(v1|v2))/', include(api_urls)),
    re_path(r'^api/v1/', include(api_urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)