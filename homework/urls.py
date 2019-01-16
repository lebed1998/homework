from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

from lab_app.views import FilmView, ListFilmView, AddFilmView, \
    SignUpView, LoginView, LogoutView, create_review, AboutView, InfoView, ChangeUpdateView, change_profile
from homework import settings

urlpatterns = [
    url(r'^$', ListFilmView.as_view()),
    url(r'^page=(?P<page>\d+)', ListFilmView.as_view()),
    url(r'^film/(?P<film_id>\d+)', FilmView.as_view()),
    url(r'^film/create_review/$', create_review, name='create_review'),
    url(r'^film/add_film/$', AddFilmView.as_view()),
    url(r'^signup/$', SignUpView.as_view()),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^change/$', change_profile, name='change_profile'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # url(r'^invalidUser/', InvalidUser.as_view()),
    url(r'^about/', AboutView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^info/', InfoView.as_view()),
    url(r'^change/update/$', ChangeUpdateView.as_view(), name='user-update')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)