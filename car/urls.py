from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add', views.add, name="add"),
    path("addFavGen/<int:id>", views.addFavGen, name="addFavGen"),
    path("genFavList", views.genFavList, name="genFavList"),
    path("addCommentFav", views.addCommentFav, name="addCommentFav"),
    path("first/<int:frstID>", views.frstCar, name="first"),
    path("compare/<int:frstID>/<int:secID>", views.compare, name="compare"),
    path("comment/<int:CID>", views.addComent, name="comment"),
    path("evaluate/<int:CID>", views.evaluate, name="evaluate"),
    path("totalEvaluation", views.totalEvaluation, name="totalEvaluation"),
    path("add/<int:CID>", views.addToFavList, name="addToFavList"),
    path("remove/<int:CID>", views.removeFavList, name="removeFavList"),
    path("favList", views.favList, name="favList"),
    path("changeSold/<int:AdId>/<int:CID>", views.changeSold, name="changeSold"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('AdName', views.AdName, name="AdName"),
    path('AdDate/<str:name>', views.AdDate, name="AdDate"),
    path('AdRest/<int:id>', views.AdRest, name="AdRest"),
    path('car/edit/<int:id>', views.edit, name="edit"),
    path('car/delete/<int:id>', views.delete, name="delete"),
    path('ad/delete/<int:id>/<int:CID>', views.deleteAd, name="adDelete"),
    path('list', views.list_cars, name="list"),
    path('list-admin', views.list_cars_admin, name="list-admin"),
    path('authorize', views.authorize, name="authorize"),
    path('authorize-add', views.authorizeAdd, name="authorize-add"),
    path('car', views.carPage, name="car"),
    path('<int:id>', views.carPage),
    path('users', views.users, name="users"),
    path('ban/<int:id>', views.ban, name="ban"),
    path('unban/<int:id>', views.unban, name="unban"),
    path('ads', views.ads, name="ads"),
    path('ads/<str:C>', views.alpha, name="alpha"),
    path('list/<str:C>', views.carAlpha, name="carAlpha"),
    path('', views.home, name="home"),
    path('google9d3ea0c0cb0559ab.html', views.gooogle, name="gooogle"),
    path("app-ads.txt", RedirectView.as_view(url=staticfiles_storage.url("app-ads.txt")),),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)