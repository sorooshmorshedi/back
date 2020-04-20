from django.conf.urls import url

from users.views import SetActiveCompany, SetActiveFinancialYear, CurrentUserApiView, UserCreateView, UserUpdateView, \
    UserDestroyView, UserListView, UserChangePasswordView

urlpatterns = [
    url(r'^create$', UserCreateView.as_view(), name='create-user'),
    url('update/(?P<pk>[0-9]+)', UserUpdateView.as_view(), name='update-user'),
    url('delete/(?P<pk>[0-9]+)', UserDestroyView.as_view(), name='destroy-user'),
    url('changePassword', UserChangePasswordView.as_view(), name='change-user-password'),
    url(r'^list$', UserListView.as_view(), name='list-users'),

    url(r'^currentUser/$', CurrentUserApiView.as_view(), name='current-user'),

    url(r'^setActiveCompany$', SetActiveCompany.as_view(), name='set-active-company'),
    url(r'^setActiveFinancialYear$', SetActiveFinancialYear.as_view(), name='set-active-financial-year'),
]
