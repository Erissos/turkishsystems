from django.urls import path

from .views import (
    about_page,
    contact_page,
    home,
    portfolio_detail,
    portfolio_page,
    services_page,
)

urlpatterns = [
    path("", home, name="home"),
    path("kurumsal/", about_page, name="about"),
    path("hizmetler/", services_page, name="services"),
    path("portfolyo/", portfolio_page, name="portfolio"),
    path("portfolyo/<slug:slug>/", portfolio_detail, name="portfolio_detail"),
    path("portfolyo/id/<int:pk>/", portfolio_detail, name="portfolio_detail_id"),
    path("iletisim/", contact_page, name="contact"),
]
