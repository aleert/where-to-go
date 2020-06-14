import pytest
from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from django.test import RequestFactory

from server.apps.users.models import User
from server.apps.users.tests.factories import UserFactory
from server.apps.users.views import UserRedirectView, UserUpdateView, user_detail_view

pytestmark = pytest.mark.django_db

fake_url = '/fake-url/'


class TestUserUpdateView:
    """Testing user update."""

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get(fake_url)
        request.user = user

        view.request = request

        assert view.get_success_url() == f'/users/{user.username}/'

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get(fake_url)
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get(fake_url)
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f'/users/{user.username}/'


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get(fake_url)
        request.user = UserFactory()

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get(fake_url)
        request.user = AnonymousUser()  # type: ignore

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 302
        assert response.url == f'/accounts/login/?next=/fake-url/'

    def test_case_sensitivity(self, rf: RequestFactory):
        request = rf.get(fake_url)
        request.user = UserFactory(username='UserName')

        with pytest.raises(Http404):
            user_detail_view(request, username='username')
