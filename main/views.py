from django.shortcuts import get_object_or_404, render

from .models import NavLink, PortfolioItem, PricingPackage, Service, SiteSettings, SocialLink, Stat


def _ensure_defaults() -> SiteSettings:
    settings_obj, created = SiteSettings.objects.get_or_create(
        id=1,
        defaults={
            "meta_title": "TurkishSystems | Mühendislik & Teknoloji Atölyesi",
            "meta_description": "TurkishSystems; oyun motoru mimarisi, bulut tabanlı SaaS platformları ve kurumsal yazılım geliştirme alanlarında uçtan uca mühendislik hizmetleri sunmaktadır.",
            "brand_name": "Turkish",
            "brand_highlight": "Systems",
            "hero_badge_year": "Est. 2021",
            "hero_badge_text": "Mühendislik Odaklı Teknoloji Atölyesi",
            "hero_heading_line_one": "Ölçeklenebilir",
            "hero_heading_highlight_one": "Yazılım,",
            "hero_heading_line_two": "Kalıcı",
            "hero_heading_highlight_two": "Değer.",
            "hero_subtitle": "Karmaşık mühendislik problemlerini ölçeklenebilir mimariler, yüksek performanslı kod ve öngörülü ürün stratejisiyle çözüyoruz. Fikirden üretime — uçtan uca.",
            "primary_cta_label": "Projeyi Başlat",
            "primary_cta_url": "/iletisim/",
            "secondary_cta_label": "Referansları İncele",
            "secondary_cta_url": "/portfolyo/",
            "services_title": "Uçtan Uca Mühendislik Çözümleri",
            "portfolio_title": "Seçili Referanslar",
            "contact_title": "Bir Sonraki\nBüyük Adım.",
            "contact_body": "Teknik danışmanlık, fiyat teklifi veya proje değerlendirmesi için doğrudan ulaşın. Her görüşme ücretsizdir.",
            "contact_button_label": "Projenizi Anlatın",
            "contact_button_url": "/iletisim/",
            "contact_whatsapp_url": "https://wa.me/905527205590",
            "contact_email": "info@turkish.systems",
            "contact_linkedin_url": "https://www.linkedin.com/in/adem-mertkan-durmaz-683667251/",
            "footer_intro": "Ölçeklenebilir yazılım mimarileri ve mühendislik disipliniyle, kalıcı değer yaratan dijital ürünler inşa ediyoruz.",
            "footer_copyright": "© 2026 TurkishSystems. Tüm hakları saklıdır.",
        },
    )

    # Force-update all SiteSettings content fields (single field update for idempotency)
    content_updates = {
        "meta_title": "TurkishSystems | Mühendislik & Teknoloji Atölyesi",
        "meta_description": "TurkishSystems; oyun motoru mimarisi, bulut tabanlı SaaS platformları ve kurumsal yazılım geliştirme alanlarında uçtan uca mühendislik hizmetleri sunmaktadır.",
        "hero_badge_year": "Est. 2021",
        "hero_badge_text": "Mühendislik Odaklı Teknoloji Atölyesi",
        "hero_heading_line_one": "Ölçeklenebilir",
        "hero_heading_highlight_one": "Yazılım,",
        "hero_heading_line_two": "Kalıcı",
        "hero_heading_highlight_two": "Değer.",
        "hero_subtitle": "Karmaşık mühendislik problemlerini ölçeklenebilir mimariler, yüksek performanslı kod ve öngörülü ürün stratejisiyle çözüyoruz. Fikirden üretime — uçtan uca.",
        "primary_cta_label": "Projeyi Başlat",
        "primary_cta_url": "/iletisim/",
        "secondary_cta_label": "Referansları İncele",
        "secondary_cta_url": "/portfolyo/",
        "services_title": "Uçtan Uca Mühendislik Çözümleri",
        "portfolio_title": "Seçili Referanslar",
        "contact_title": "Bir Sonraki\nBüyük Adım.",
        "contact_body": "Teknik danışmanlık, fiyat teklifi veya proje değerlendirmesi için doğrudan ulaşın. Her görüşme ücretsizdir.",
        "contact_button_label": "Projenizi Anlatın",
        "contact_button_url": "/iletisim/",
        "contact_whatsapp_url": "https://wa.me/905527205590",
        "contact_email": "info@turkish.systems",
        "contact_linkedin_url": "https://www.linkedin.com/in/adem-mertkan-durmaz-683667251/",
        "footer_intro": "Ölçeklenebilir yazılım mimarileri ve mühendislik disipliniyle, kalıcı değer yaratan dijital ürünler inşa ediyoruz.",
        "footer_copyright": "© 2026 TurkishSystems. Tüm hakları saklıdır.",
    }
    needs_save = False
    for field, value in content_updates.items():
        if getattr(settings_obj, field) != value:
            setattr(settings_obj, field, value)
            needs_save = True
    if needs_save:
        settings_obj.save()

    if not NavLink.objects.exists():
        NavLink.objects.bulk_create(
            [
                NavLink(label="Kurumsal", url="/kurumsal/", order=1),
                NavLink(label="Hizmetler", url="/hizmetler/", order=2),
                NavLink(label="Referanslar", url="/portfolyo/", order=3),
                NavLink(label="İş Birliği Başlat", url="/iletisim/", is_primary=True, order=4),
            ]
        )
    else:
        default_link_map = {
            "Kurumsal": "/kurumsal/",
            "Hizmetler": "/hizmetler/",
            "Portfolyo": "/portfolyo/",
            "Referanslar": "/portfolyo/",
            "İş Birliği Başlat": "/iletisim/",
        }
        for link in NavLink.objects.all():
            if link.label in default_link_map and link.url.startswith("#"):
                link.url = default_link_map[link.label]
                link.save(update_fields=["url"])

    if not Stat.objects.exists():
        Stat.objects.bulk_create(
            [
                Stat(value="60+", label="Teslim Edilen Proje", order=1),
                Stat(value="5+", label="Yıllık Deneyim", order=2),
                Stat(value="%96", label="Müşteri Memnuniyeti", order=3),
                Stat(value="24/7", label="Teknik Destek", order=4),
            ]
        )
    else:
        _STAT_DEFAULTS = [
            {"value": "60+",  "label": "Teslim Edilen Proje"},
            {"value": "5+",   "label": "Yıllık Deneyim"},
            {"value": "%96",  "label": "Müşteri Memnuniyeti"},
            {"value": "24/7", "label": "Teknik Destek"},
        ]
        for i, stat in enumerate(Stat.objects.order_by("order", "id")[:4], start=0):
            d = _STAT_DEFAULTS[i]
            if stat.value != d["value"] or stat.label != d["label"]:
                stat.value = d["value"]
                stat.label = d["label"]
                stat.save(update_fields=["value", "label"])

    if not Service.objects.exists():
        Service.objects.bulk_create(
            [
                Service(
                    title="Oyun Motoru & Simülasyon",
                    description=(
                        "Unity ve C# üzerinde derinlemesine uzmanlaşma. "
                        "Fizik tabanlı simülasyonlardan çok oyunculu ağ mimarisine, "
                        "AI davranış sistemlerinden shader optimizasyonuna kadar "
                        "production-ready oyun geliştirme."
                    ),
                    bullet_one="Multiplayer Ağ Mimarisi & Düşük Gecikme",
                    bullet_two="Mobil / PC / Konsol Optimizasyonu",
                    icon_class="fa-solid fa-gamepad",
                    accent_class="blue",
                    order=1,
                ),
                Service(
                    title="Bulut Mimarisi & Backend",
                    description=(
                        "Yüksek erişilebilirlik gerektiren SaaS platformları için "
                        "mikroservis tabanlı backend tasarımı. REST & GraphQL API "
                        "servisleri, CI/CD otomasyonu ve bulut altyapı yönetimi "
                        "(AWS / GCP / Azure)."
                    ),
                    bullet_one="Mikroservis & Konteyner (Docker / K8s)",
                    bullet_two="Yüksek Trafikli API ve Veritabanı Katmanı",
                    icon_class="fa-solid fa-server",
                    accent_class="purple",
                    order=2,
                ),
                Service(
                    title="Kurumsal Yazılım & Otomasyon",
                    description=(
                        "İş süreçlerinizi hızlandıran özel e-ticaret, ERP, CRM "
                        "entegrasyon ve otomasyon sistemleri. Legacy altyapı "
                        "modernizasyonu ve teknik borç tasfiyesi."
                    ),
                    bullet_one="İş Akışı Otomasyonu & ERP/CRM Entegrasyonu",
                    bullet_two="Legacy Modernizasyonu & Teknik Dönüşüm",
                    icon_class="fa-solid fa-gears",
                    accent_class="pink",
                    order=3,
                ),
            ]
        )
    else:
        _SRV_DEFAULTS = [
            {
                "title": "Oyun Motoru & Simülasyon",
                "description": (
                    "Unity ve C# üzerinde derinlemesine uzmanlaşma. "
                    "Fizik tabanlı simülasyonlardan çok oyunculu ağ mimarisine, "
                    "AI davranış sistemlerinden shader optimizasyonuna kadar "
                    "production-ready oyun geliştirme."
                ),
                "bullet_one": "Multiplayer Ağ Mimarisi & Düşük Gecikme",
                "bullet_two": "Mobil / PC / Konsol Optimizasyonu",
                "icon_class": "fa-solid fa-gamepad",
            },
            {
                "title": "Bulut Mimarisi & Backend",
                "description": (
                    "Yüksek erişilebilirlik gerektiren SaaS platformları için "
                    "mikroservis tabanlı backend tasarımı. REST & GraphQL API "
                    "servisleri, CI/CD otomasyonu ve bulut altyapı yönetimi "
                    "(AWS / GCP / Azure)."
                ),
                "bullet_one": "Mikroservis & Konteyner (Docker / K8s)",
                "bullet_two": "Yüksek Trafikli API ve Veritabanı Katmanı",
                "icon_class": "fa-solid fa-server",
            },
            {
                "title": "Kurumsal Yazılım & Otomasyon",
                "description": (
                    "İş süreçlerinizi hızlandıran özel e-ticaret, ERP, CRM "
                    "entegrasyon ve otomasyon sistemleri. Legacy altyapı "
                    "modernizasyonu ve teknik borç tasfiyesi."
                ),
                "bullet_one": "İş Akışı Otomasyonu & ERP/CRM Entegrasyonu",
                "bullet_two": "Legacy Modernizasyonu & Teknik Dönüşüm",
                "icon_class": "fa-solid fa-gears",
            },
        ]
        for i, srv in enumerate(Service.objects.order_by("order", "id")[:3], start=0):
            d = _SRV_DEFAULTS[i]
            updated = False
            for field, val in d.items():
                if getattr(srv, field) != val:
                    setattr(srv, field, val)
                    updated = True
            if updated:
                srv.save()

    if not PortfolioItem.objects.exists():
        PortfolioItem.objects.bulk_create(
            [
                PortfolioItem(
                    title="Iduk",
                    slug="iduk",
                    description=(
                        "Eğitim teknolojisi alanında geliştirilen kapsamlı bir bilgi platformu. "
                        "Öğrencilerin ders içeriklerine, alıştırmalara ve kişiselleştirilmiş "
                        "öğrenme yollarına tek platformdan ulaşmasını sağlayan, "
                        "yüksek trafikli ve responsive bir web uygulaması.\n\n"
                        "Teknik kapsam: Django tabanlı backend, PostgreSQL veritabanı, "
                        "gerçek zamanlı bildirim sistemi ve içerik yönetim paneli."
                    ),
                    image="portfolio/iduk.png",
                    order=1,
                ),
                PortfolioItem(
                    title="Sormaca",
                    slug="sormaca",
                    description=(
                        "Canlı soru-cevap etkinlikleri için tasarlanan interaktif bir quiz platformu. "
                        "WebSocket tabanlı gerçek zamanlı senkronizasyon ile yüzlerce eş zamanlı "
                        "kullanıcıyı destekleyen, etkinlik yönetim paneli ve anlık skor "
                        "tabanlı rekabet sistemi içeren tam kapsamlı bir uygulama.\n\n"
                        "Teknik kapsam: Django Channels, Redis, React frontend ve "
                        "mobil uyumlu arayüz tasarımı."
                    ),
                    image="portfolio/sormaca.png",
                    order=2,
                ),
                PortfolioItem(
                    title="Turkishpedia",
                    slug="turkishpedia",
                    description=(
                        "Türkçe içeriğe öncelik veren, Wikipedia modelinden ilham alan "
                        "bağımsız bir bilgi ansiklopedisi. Editöryal iş akışları, "
                        "kategori sistemi ve hızlı tam-metin arama altyapısıyla "
                        "donatılmış, topluluk katkısına açık bir platform.\n\n"
                        "Teknik kapsam: Python/Django, Elasticsearch entegrasyonu, "
                        "katmanlı yetki sistemi ve otomatik içerik moderasyon araçları."
                    ),
                    image="portfolio/turkishpedia.png",
                    order=3,
                ),
            ]
        )
    else:
        _PF_DEFAULTS = [
            {
                "slug": "iduk",
                "title": "Iduk",
                "description": (
                    "Eğitim teknolojisi alanında geliştirilen kapsamlı bir bilgi platformu. "
                    "Öğrencilerin ders içeriklerine, alıştırmalara ve kişiselleştirilmiş "
                    "öğrenme yollarına tek platformdan ulaşmasını sağlayan, "
                    "yüksek trafikli ve responsive bir web uygulaması.\n\n"
                    "Teknik kapsam: Django tabanlı backend, PostgreSQL veritabanı, "
                    "gerçek zamanlı bildirim sistemi ve içerik yönetim paneli."
                ),
            },
            {
                "slug": "sormaca",
                "title": "Sormaca",
                "description": (
                    "Canlı soru-cevap etkinlikleri için tasarlanan interaktif bir quiz platformu. "
                    "WebSocket tabanlı gerçek zamanlı senkronizasyon ile yüzlerce eş zamanlı "
                    "kullanıcıyı destekleyen, etkinlik yönetim paneli ve anlık skor "
                    "tabanlı rekabet sistemi içeren tam kapsamlı bir uygulama.\n\n"
                    "Teknik kapsam: Django Channels, Redis, React frontend ve "
                    "mobil uyumlu arayüz tasarımı."
                ),
            },
            {
                "slug": "turkishpedia",
                "title": "Turkishpedia",
                "description": (
                    "Türkçe içeriğe öncelik veren, Wikipedia modelinden ilham alan "
                    "bağımsız bir bilgi ansiklopedisi. Editöryal iş akışları, "
                    "kategori sistemi ve hızlı tam-metin arama altyapısıyla "
                    "donatılmış, topluluk katkısına açık bir platform.\n\n"
                    "Teknik kapsam: Python/Django, Elasticsearch entegrasyonu, "
                    "katmanlı yetki sistemi ve otomatik içerik moderasyon araçları."
                ),
            },
        ]
        for d in _PF_DEFAULTS:
            try:
                pf = PortfolioItem.objects.get(slug=d["slug"])
                updated = False
                for field in ("title", "description"):
                    if getattr(pf, field) != d[field]:
                        setattr(pf, field, d[field])
                        updated = True
                if updated:
                    pf.save()
            except PortfolioItem.DoesNotExist:
                pass

    if not PricingPackage.objects.exists():
        PricingPackage.objects.bulk_create(
            [
                PricingPackage(
                    name="Başlangıç",
                    price="₺14.900",
                    description="Fikir aşamasındaki ürünler ve MVP'ler için sabit kapsamlı başlangıç paketi.",
                    features="Tek sayfalık web uygulaması veya API\nTemel kullanıcı kimlik doğrulama\nAdmin paneli\n30 gün hata destek garantisi\nKod teslimi + dokümantasyon",
                    is_highlighted=False,
                    order=1,
                ),
                PricingPackage(
                    name="Büyüme",
                    price="₺39.900",
                    description="Ölçeklenmesi gereken, kullanıcı kitlesi olan ürünler için mühendislik odaklı paket.",
                    features="Çoklu modül backend mimarisi\nREST API + mobil hazır tasarım\nCI/CD pipeline kurulumu\nPerformans & güvenlik testi\n90 gün teknik destek + SLA\nKapsamlı teknik dokümantasyon",
                    is_highlighted=True,
                    order=2,
                ),
                PricingPackage(
                    name="Kurumsal",
                    price="Özel Teklif",
                    description="Kritik iş süreçleri için özelleştirilmiş, SLA güvenceli kurumsal çözüm.",
                    features="Mimari tasarım danışmanlığı\nMikroservis & bulut altyapısı\nLegacy sistem entegrasyonu\n7/24 izleme & müdahale\nDedike teknik proje yönetimi\nNDA + kod mülkiyeti garantisi",
                    is_highlighted=False,
                    order=3,
                ),
            ]
        )
    else:
        _PKG_DEFAULTS = [
            {
                "name": "Başlangıç",
                "price": "₺14.900",
                "description": "Fikir aşamasındaki ürünler ve MVP'ler için sabit kapsamlı başlangıç paketi.",
                "features": "Tek sayfalık web uygulaması veya API\nTemel kullanıcı kimlik doğrulama\nAdmin paneli\n30 gün hata destek garantisi\nKod teslimi + dokümantasyon",
                "is_highlighted": False,
            },
            {
                "name": "Büyüme",
                "price": "₺39.900",
                "description": "Ölçeklenmesi gereken, kullanıcı kitlesi olan ürünler için mühendislik odaklı paket.",
                "features": "Çoklu modül backend mimarisi\nREST API + mobil hazır tasarım\nCI/CD pipeline kurulumu\nPerformans & güvenlik testi\n90 gün teknik destek + SLA\nKapsamlı teknik dokümantasyon",
                "is_highlighted": True,
            },
            {
                "name": "Kurumsal",
                "price": "Özel Teklif",
                "description": "Kritik iş süreçleri için özelleştirilmiş, SLA güvenceli kurumsal çözüm.",
                "features": "Mimari tasarım danışmanlığı\nMikroservis & bulut altyapısı\nLegacy sistem entegrasyonu\n7/24 izleme & müdahale\nDedike teknik proje yönetimi\nNDA + kod mülkiyeti garantisi",
                "is_highlighted": False,
            },
        ]
        for i, pkg in enumerate(PricingPackage.objects.order_by("order", "id")[:3], start=0):
            d = _PKG_DEFAULTS[i]
            updated = False
            for field, val in d.items():
                if getattr(pkg, field) != val:
                    setattr(pkg, field, val)
                    updated = True
            if updated:
                pkg.save()

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
    return render(request, "main/home.jinja", context, using="jinja2")


def about_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj),
        "stats": Stat.objects.all(),
    }
    return render(request, "main/about.jinja", context, using="jinja2")


def services_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj),
        "services": Service.objects.all(),
        "pricing_packages": PricingPackage.objects.all(),
    }
    return render(request, "main/services.jinja", context, using="jinja2")


def portfolio_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj),
        "portfolio_items": PortfolioItem.objects.all(),
    }
    return render(request, "main/portfolio_list.jinja", context, using="jinja2")


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
    return render(request, "main/portfolio_detail.jinja", context, using="jinja2")


def contact_page(request):
    settings_obj = _ensure_defaults()
    context = _base_context(settings_obj)
    return render(request, "main/contact.jinja", context, using="jinja2")
