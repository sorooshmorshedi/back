from django.conf.urls import url

from users.views.citiesView import CityListCreateView, CityDetailView
from users.views.rolesView import RoleCreateView, RoleUpdateView, RoleDestroyView, RoleListView, PermissionListView
from users.views.usersView import SetActiveCompany, SetActiveFinancialYear, CurrentUserApiView, UserCreateView, \
    UserUpdateView, UserListView, UserChangePasswordView, SendVerificationCodeView, \
    ChangePasswordByVerificationCodeView, UserInvitationsListView, ChangeUserInvitationStatusView

urlpatterns = [
    url(r'^create$', UserCreateView.as_view(), name='create-user'),
    url(r'^update/(?P<pk>[0-9]+)$', UserUpdateView.as_view(), name='update-user'),
    url(r'^changePassword$', UserChangePasswordView.as_view(), name='change-user-password'),
    url(r'^invitations$', UserInvitationsListView.as_view(), name='user-invitations'),
    url(r'^invitations/changeStatus$', ChangeUserInvitationStatusView.as_view(), name='change-user-invitation-status'),

    url(r'^list$', UserListView.as_view(), name='list-users'),

    url(r'^sendVerificationCode$', SendVerificationCodeView.as_view()),
    url(r'^changePasswordByVerificationCode$', ChangePasswordByVerificationCodeView.as_view()),

    url(r'^roles/create$', RoleCreateView.as_view(), name='create-role'),
    url(r'^roles/update/(?P<pk>[0-9]+)$', RoleUpdateView.as_view(), name='update-role'),
    url(r'^roles/delete/(?P<pk>[0-9]+)$', RoleDestroyView.as_view(), name='destroy-role'),
    url(r'^roles/list$', RoleListView.as_view(), name='list-roles'),
    url(r'^permissions/list$', PermissionListView.as_view(), name='list-permissions'),

    url(r'^currentUser/$', CurrentUserApiView.as_view(), name='current-user'),

    url(r'^setActiveCompany$', SetActiveCompany.as_view(), name='set-active-company'),
    url(r'^setActiveFinancialYear$', SetActiveFinancialYear.as_view(), name='set-active-financial-year'),

    url(r'^cities$', CityListCreateView.as_view(), name='list-create-city'),
    url(r'^cities/(?P<pk>[0-9]+)$', CityDetailView.as_view(), name='detail-city'),
]
