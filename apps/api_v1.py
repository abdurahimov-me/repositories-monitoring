from django.urls import path, include

urlpatterns = [

    path(
        'common',
        include('apps.common.urls'),
        name='common'

    ),
    path(
        'users/',
        include('apps.users.urls'),
        name='users'
    )
]
