from django.shortcuts import get_object_or_404, render

from .models import NavLink, PortfolioItem, PricingPackage, Service, SiteSettings, SocialLink, Stat


def _ensure_defaults() -> SiteSettings:
    settings_obj, _ = SiteSettings.objects.get_or_create(
        id=1,
        defaults={
            "meta_title": "TurkishSystems | Dijital Sanat ve Mühendislik",
            "meta_description": "TurkishSystems, üst segment oyun geliştirme ve karmaşık yazılım mimarileri üzerine uzmanlaşmış bir teknoloji atölyesidir.",
            "brand_name": "Turkish",
            "brand_highlight": "Systems",
            "hero_badge_year": "2026",
            "hero_badge_text": "Vizyonuyla Yazılımın Geleceği",
            "hero_heading_line_one": "Hayalleri",
            "hero_heading_highlight_one": "Kodla,",
            "hero_heading_line_two": "Dünyayı",
            "hero_heading_highlight_two": "Değiştir.",
            "hero_subtitle": "TurkishSystems, üst segment oyun geliştirme ve karmaşık yazılım mimarileri üzerine uzmanlaşmış, freelance esnekliği ile kurumsal kaliteyi birleştiren bir teknoloji atölyesidir.",
            "primary_cta_label": "Sipariş Oluştur",
            "primary_cta_url": "#contact",
            "secondary_cta_label": "Çalışmaları İncele",
            "secondary_cta_url": "#portfolio",
            "services_title": "Uçtan Uca Çözümler",
            "portfolio_title": "Portfolyo",
            "contact_title": "Bir sonraki büyük adımı\nbirlikte atalım.",
            "contact_body": "Kurumsal siparişleriniz veya freelance talepleriniz için uzman ekibimizle iletişime geçin.",
            "contact_button_label": "Projenizi Anlatın",
            "contact_button_url": "#contact-modal",
            "contact_whatsapp_url": "https://wa.me/905527205590",
            "contact_email": "ademmertkan01@gmail.com",
            "contact_linkedin_url": "https://www.linkedin.com/in/adem-mertkan-durmaz-683667251/",
            "footer_intro": "Yazılımda kaliteyi, oyun geliştirmede yaratıcılığı ön planda tutan teknoloji çözüm ortağınız.",
            "footer_copyright": "© 2026 TurkishSystems. All rights reserved. Crafting Digital Excellence.",
        },
    )

    # Force-update contact fields if they are empty or default placeholders
    params_updated = False
    if not settings_obj.contact_whatsapp_url or settings_obj.contact_whatsapp_url == "https://wa.me/905000000000":
        settings_obj.contact_whatsapp_url = "https://wa.me/905527205590"
        params_updated = True
    if not settings_obj.contact_email or settings_obj.contact_email == "info@turkishsystems.com":
        settings_obj.contact_email = "ademmertkan01@gmail.com"
        params_updated = True
    if not settings_obj.contact_linkedin_url:
        settings_obj.contact_linkedin_url = "https://www.linkedin.com/in/adem-mertkan-durmaz-683667251/"
        params_updated = True
    
    if params_updated:
        settings_obj.save()

    if not NavLink.objects.exists():
        NavLink.objects.bulk_create(
            [
                NavLink(label="Kurumsal", url="/kurumsal/", order=1),
                NavLink(label="Hizmetler", url="/hizmetler/", order=2),
                NavLink(label="Portfolyo", url="/portfolyo/", order=3),
                NavLink(label="İş Birliği Başlat", url="/iletisim/", is_primary=True, order=4),
            ]
        )
    else:
        default_link_map = {
            "Kurumsal": "/kurumsal/",
            "Hizmetler": "/hizmetler/",
            "Portfolyo": "/portfolyo/",
            "İş Birliği Başlat": "/iletisim/",
        }
        for link in NavLink.objects.all():
            if link.label in default_link_map and link.url.startswith("#"):
                link.url = default_link_map[link.label]
                link.save(update_fields=["url"])

    if not Stat.objects.exists():
        Stat.objects.bulk_create(
            [
                Stat(value="60+", label="Tamamlanan Proje", order=1),
                Stat(value="12M+", label="Satır Kod", color_class="text-blue-500", order=2),
                Stat(value="90%", label="Müşteri Memnuniyeti", color_class="text-purple-500", order=3),
                Stat(value="24/7", label="Teknik Destek", order=4),
            ]
        )

    if not Service.objects.exists():
        Service.objects.bulk_create(
            [
                Service(
                    title="Oyun Motoru Mimarisi",
                    description=(
                        "Unity ve C# üzerinde derin uzmanlık. Fizik tabanlı "
                        "sistemlerden yapay zeka entegrasyonuna kadar profesyonel oyun geliştirme."
                    ),
                    bullet_one="Mobil ve PC Optimizasyonu",
                    bullet_two="Çok Oyunculu (Multiplayer) Yapılar",
                    icon_class="fa-solid fa-layer-group",
                    accent_class="blue",
                    order=1,
                ),
                Service(
                    title="Sistem ve Otomasyon",
                    description=(
                        "İş süreçlerinizi hızlandıran özel yazılımlar. Veri "
                        "madenciliği, bot sistemleri ve yüksek trafikli backend mimarileri."
                    ),
                    bullet_one="API Entegrasyonları",
                    bullet_two="Veritabanı Yönetimi",
                    icon_class="fa-solid fa-microchip",
                    accent_class="purple",
                    order=2,
                ),
                Service(
                    title="Freelance Danışmanlık",
                    description=(
                        "Mevcut projelerinizdeki teknik tıkanıklıkları gideriyoruz. "
                        "Kod incelemesi ve performans iyileştirme hizmetleri."
                    ),
                    bullet_one="Hızlı Çözüm Odaklılık",
                    bullet_two="Esnek Çalışma Modeli",
                    icon_class="fa-solid fa-terminal",
                    accent_class="pink",
                    order=3,
                ),
            ]
        )

    if not PortfolioItem.objects.exists():
        PortfolioItem.objects.bulk_create(
            [
                PortfolioItem(
                    title="Iduk",
                    slug="iduk",
                    description="Eğitim odaklı bir bilgi platformu için hazırlanan modern arayüz.",
                    image="iduk.png",
                    order=1,
                ),
                PortfolioItem(
                    title="Sormaca",
                    slug="sormaca",
                    description="Kullanıcıları etkileyen interaktif quiz deneyimi.",
                    image="sormaca.png",
                    order=2,
                ),
                PortfolioItem(
                    title="Turkishpedia",
                    slug="turkishpedia",
                    description="Bilgiye hızlı erişim sağlayan, yalnızca Türkçe odaklı kütüphane.",
                    image="turkishpedia.png",
                    order=3,
                ),
            ]
        )

    if not PricingPackage.objects.exists():
        PricingPackage.objects.bulk_create(
            [
                PricingPackage(
                    name="Start",
                    price="₺9.900/ay",
                    description="Yeni çıkan SaaS ürünleri için temel özellik seti.",
                    features="5.000 aktif kullanıcı\nE-posta destek\n2 entegrasyon",
                    is_highlighted=False,
                    order=1
                ),
                PricingPackage(
                    name="Scale",
                    price="₺24.900/ay",
                    description="Büyüme aşamasındaki ürünler için optimize paket.",
                    features="50.000 aktif kullanıcı\nSLA destek\n8 entegrasyon",
                    is_highlighted=True,
                    order=2
                ),
                PricingPackage(
                    name="Enterprise",
                    price="Özel teklif",
                    description="Kurumsal ihtiyaçlara göre uyarlanmış özel paket.",
                    features="Sınırsız kullanıcı\nÖzel müşteri başarı ekibi\nÖzel güvenlik katmanı",
                    is_highlighted=False,
                    order=3
                ),
            ]
        )

    if not SocialLink.objects.exists():
        SocialLink.objects.bulk_create(
            [
                SocialLink(label="Github", url="https://github.com/erissos", order=1),
                SocialLink(label="LinkedIn", url="https://www.linkedin.com/in/adem-mertkan-durmaz-683667251/", order=2),
            ]
        )

    return settings_obj


def _base_context(settings_obj: SiteSettings) -> dict:
    return {
        "site": settings_obj,
        "nav_links": NavLink.objects.all(),
        "social_links": SocialLink.objects.all(),
    }


def home(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj),
        "stats": Stat.objects.all(),
        "services": Service.objects.all(),
        "portfolio_items": PortfolioItem.objects.all(),
    }
    return render(request, "main/home.html", context)


def about_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj),
        "stats": Stat.objects.all(),
    }
    return render(request, "main/about.html", context)


def services_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj),
        "services": Service.objects.all(),
        "pricing_packages": PricingPackage.objects.all(),
    }
    return render(request, "main/services.html", context)


def portfolio_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj),
        "portfolio_items": PortfolioItem.objects.all(),
    }
    return render(request, "main/portfolio_list.html", context)


def portfolio_detail(request, slug: str = "", pk: int | None = None):
    settings_obj = _ensure_defaults()
    if pk is not None:
        item = get_object_or_404(PortfolioItem, pk=pk)
    else:
        item = get_object_or_404(PortfolioItem, slug=slug)
    context = {
        **_base_context(settings_obj),
        "item": item,
    }
    return render(request, "main/portfolio_detail.html", context)


def contact_page(request):
    settings_obj = _ensure_defaults()
    context = _base_context(settings_obj)
    return render(request, "main/contact.html", context)
