from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from sobhan_admin.views import AdminUsersView, AdminLoginView

router = DefaultRouter()
router.register('users', AdminUsersView, basename='admin-users')

urlpatterns = [
    url('^login$', AdminLoginView.as_view(), name='admin-login'),

]

urlpatterns += router.urls
