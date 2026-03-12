from django.urls import path

from .views import (
    account_auth_page,
    about_page,
    contact_page,
    dashboard_page,
    home,
    logout_view,
    product_detail,
    products_page,
    portfolio_detail,
    portfolio_page,
    services_page,
)

urlpatterns = [
    path("", home, name="home"),
    path("kurumsal/", about_page, name="about"),
    path("hizmetler/", services_page, name="services"),
    path("urunler/", products_page, name="products"),
    path("urunler/<slug:slug>/", product_detail, name="product_detail"),
    path("portfolyo/", portfolio_page, name="portfolio"),
    path("portfolyo/<slug:slug>/", portfolio_detail, name="portfolio_detail"),
    path("portfolyo/id/<int:pk>/", portfolio_detail, name="portfolio_detail_id"),
    path("iletisim/", contact_page, name="contact"),
    path("hesap/", dashboard_page, name="dashboard"),
    path("giris/", account_auth_page, name="account_auth"),
    path("cikis/", logout_view, name="logout"),
]
