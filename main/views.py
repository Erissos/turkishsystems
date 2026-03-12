from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectRequestForm, SignInForm, SignUpForm
from .models import (
    NavLink,
    PortfolioItem,
    PricingPackage,
    Product,
    ProductFAQ,
    ProductOrder,
    ProductPackage,
    ProductReview,
    ProjectRequest,
    Reference,
    Service,
    SiteSettings,
    SocialLink,
    Stat,
)

PORTAL_URL = "https://portal.turkish.systems"


def _site_defaults() -> dict[str, str]:
    return {
        "meta_title": "TurkishSystems | Kurumsal Yazılım ve Portal Sistemleri",
        "meta_description": "TurkishSystems; kurumsal hizmetler sunar, somut dijital ürünler geliştirir ve müşteri portalı altyapıları kurar.",
        "brand_name": "Turkish",
        "brand_highlight": "Systems",
        "hero_badge_year": "Est. 2021",
        "hero_badge_text": "Kurumsal Hizmetler, Dijital Ürünler ve Portal Altyapıları",
        "hero_heading_line_one": "Kurumsal",
        "hero_heading_highlight_one": "Sistemler,",
        "hero_heading_line_two": "Hızlı Operasyon",
        "hero_heading_highlight_two": "Net Takip.",
        "hero_subtitle": "Müşterilerinize özel portal sistemleri, merkezi takip akışları ve güvenli dosya paylaşım altyapıları geliştiriyoruz. Ekiplerinizle senkron, denetlenebilir ve hızlı çalışan dijital operasyon katmanı kuruyoruz.",
        "primary_cta_label": "Talep Oluştur",
        "primary_cta_url": "/iletisim/",
        "secondary_cta_label": "Ürünleri İncele",
        "secondary_cta_url": "/urunler/",
        "services_title": "Sağladığımız Kurumsal Hizmetler",
        "portfolio_title": "Portfolyo ve Referanslar",
        "contact_title": "Projenizi\nPlanlayalım.",
        "contact_body": "Kayıt olun, talep gönderin ve süreçlerinizi bizimle daha görünür hale getirin. Her talep teknik kapsam, zaman planı ve entegrasyon ihtiyaçlarıyla birlikte değerlendirilir.",
        "contact_button_label": "Talep Formuna Geç",
        "contact_button_url": "/iletisim/",
        "contact_whatsapp_url": "https://wa.me/905527205590",
        "contact_email": "info@turkish.systems",
        "contact_linkedin_url": "https://www.linkedin.com/in/adem-mertkan-durmaz-683667251/",
        "footer_intro": "TurkishSystems; portal, takip, entegrasyon ve kurumsal yazılım projelerinde mühendislik disiplini ile çalışan teknik partnerinizdir.",
        "footer_copyright": "© 2026 TurkishSystems. Tüm hakları saklıdır.",
    }


def _nav_defaults() -> list[dict[str, object]]:
    return [
        {"label": "Kurumsal", "url": "/kurumsal/", "order": 1, "is_primary": False},
        {"label": "Hizmetler", "url": "/hizmetler/", "order": 2, "is_primary": False},
        {"label": "Ürünler", "url": "/urunler/", "order": 3, "is_primary": False},
        {"label": "Portfolyo", "url": "/portfolyo/", "order": 4, "is_primary": False},
        {"label": "Talep Gönder", "url": "/iletisim/", "order": 5, "is_primary": True},
    ]


def _stat_defaults() -> list[dict[str, str]]:
    return [
        {"value": "72s", "label": "İlk Teknik Dönüş"},
        {"value": "%99.2", "label": "Operasyon Görünürlüğü"},
        {"value": "60+", "label": "Teslim Edilen Çözüm"},
        {"value": "24/7", "label": "Süreç Takip Disiplini"},
    ]


def _service_defaults() -> list[dict[str, str]]:
    return [
        {
            "title": "Sosyal Medya Yönetimi",
            "description": "Marka dilinizi, içerik planlamanızı ve reklam stratejinizi profesyonel biçimde yönetiyoruz.",
            "bullet_one": "İçerik takvimi ve yayın planı",
            "bullet_two": "Reklam optimizasyonu ve raporlama",
            "icon_class": "fa-solid fa-bullhorn",
            "accent_class": "gold",
        },
        {
            "title": "Web Siteleri",
            "description": "Kurumsal güven veren, SEO uyumlu ve yönetilebilir web siteleri tasarlıyor ve geliştiriyoruz.",
            "bullet_one": "Marka kimliğiyle uyumlu tasarım",
            "bullet_two": "Performans ve güvenlik odaklı altyapı",
            "icon_class": "fa-solid fa-globe",
            "accent_class": "gold",
        },
        {
            "title": "Mobil Uygulamalar",
            "description": "iOS ve Android platformlarında kullanıcı odaklı, performanslı mobil uygulamalar geliştiriyoruz.",
            "bullet_one": "Cross-platform ve native çözümler",
            "bullet_two": "Kullanıcı deneyimi ve performans optimizasyonu",
            "icon_class": "fa-solid fa-mobile-screen-button",
            "accent_class": "gold",
        },
        {
            "title": "Otomasyon Sistemi",
            "description": "Teklif, onay, görev, teslimat ve raporlama adımlarını tek merkezden yöneten süreç otomasyonları geliştiriyoruz.",
            "bullet_one": "Durum bazlı iş akışları ve SLA takibi",
            "bullet_two": "Alarm, rapor ve yönetici görünürlüğü",
            "icon_class": "fa-solid fa-diagram-project",
            "accent_class": "gold",
        },
        {
            "title": "Kurumsal Kaynak Uygulamaları",
            "description": "Muhasebe, CRM, ERP ve iç sistemlerinizi entegre eden kurumsal kaynak yönetim çözümleri sunuyoruz.",
            "bullet_one": "Merkezi veri senkronizasyonu",
            "bullet_two": "API gateway ve özel entegrasyon mantığı",
            "icon_class": "fa-solid fa-plug-circle-bolt",
            "accent_class": "gold",
        },
        {
            "title": "Kurumsal Web Platformları",
            "description": "Kurumsal güven veren, dönüşüm odaklı, yönetilebilir ve SEO uyumlu web platformları tasarlıyor ve geliştiriyoruz.",
            "bullet_one": "Marka kimliğiyle uyumlu yönetim paneli",
            "bullet_two": "Performans, güvenlik ve içerik operasyonu",
            "icon_class": "fa-solid fa-building-shield",
            "accent_class": "gold",
        },
        {
            "title": "Operasyon ve Takip Otomasyonları",
            "description": "Teklif, onay, görev, teslimat ve raporlama adımlarını tek merkezden yöneten süreç otomasyonları geliştiriyoruz.",
            "bullet_one": "Durum bazlı iş akışları ve SLA takibi",
            "bullet_two": "Alarm, rapor ve yönetici görünürlüğü",
            "icon_class": "fa-solid fa-diagram-project",
            "accent_class": "gold",
        },
        {
            "title": "Altyapı, DevOps ve İzleme",
            "description": "Canlı sistemlerinizi hızlı, izlenebilir ve geri döndürülebilir dağıtım süreçleriyle ayakta tutuyoruz.",
            "bullet_one": "CI/CD, yedekleme ve log yönetimi",
            "bullet_two": "Olay takibi, uptime ve performans görünürlüğü",
            "icon_class": "fa-solid fa-server",
            "accent_class": "gold",
        },
    ]


def _portfolio_defaults() -> list[dict[str, str | bool | int]]:
    return [
        {
            "title": "Iduk Akademi Operasyon Portalı",
            "slug": "iduk",
            "description": "Eğitim operasyonlarını, içerik yayın takvimini ve öğrenci bildirim süreçlerini tek merkezde yöneten kurumsal portal altyapısı.",
            "client_name": "Iduk",
            "industry": "Eğitim Teknolojileri",
            "location": "Türkiye",
            "delivery_year": "2025",
            "scope_summary": "Portal, içerik operasyonu, rol bazlı yönetim ve raporlama",
            "highlight_metric": "%43 daha hızlı içerik yayını",
            "challenge": "Farklı ekipler; içerik planlama, onay ve öğrenci bilgilendirme süreçlerini dağınık araçlar üzerinden yürütüyordu. Dosya paylaşımı ve görev görünürlüğü operasyonu yavaşlatıyordu.",
            "solution": "Rol bazlı kontrol paneli, merkezi belge alanı, görev akış motoru ve yönetici raporlama modülü olan özel bir müşteri portalı geliştirildi.",
            "results": "İçerik teslim süresi kısaldı, tekrar eden koordinasyon yükü azaldı ve tüm operasyon tek dashboard üzerinden izlenebilir hale geldi.",
            "technologies": "Django\nPostgreSQL\nCelery\nRedis\nRole Based Access Control",
            "project_url": "",
            "is_featured": True,
            "is_live": True,
            "order": 1,
        },
        {
            "title": "Sormaca Etkinlik Takip Sistemi",
            "slug": "sormaca",
            "description": "Canlı etkinliklerde yönetim, kullanıcı takibi ve anlık skor akışını bir arada sunan yüksek tempolu takip sistemi.",
            "client_name": "Sormaca",
            "industry": "Etkinlik ve Eğitim",
            "location": "Uzaktan",
            "delivery_year": "2024",
            "scope_summary": "Gerçek zamanlı takip, kontrol paneli ve katılımcı yönetimi",
            "highlight_metric": "1000+ eş zamanlı kullanıcı desteği",
            "challenge": "Etkinlik akışlarında senkronizasyon ve yönetici görünürlüğü yetersizdi. Manuel takip ciddi koordinasyon maliyeti üretiyordu.",
            "solution": "Gerçek zamanlı durum yönetimi, bildirim akışları ve merkezi moderasyon paneli içeren özel bir takip altyapısı kuruldu.",
            "results": "Canlı etkinliklerde aksiyon alma süresi düştü, teknik ekip ve moderasyon aynı panelden çalışmaya başladı.",
            "technologies": "Django Channels\nRedis\nWebSocket\nReact\nNginx",
            "project_url": "",
            "is_featured": True,
            "is_live": True,
            "order": 2,
        },
        {
            "title": "Turkishpedia İçerik ve Dosya Yönetim Altyapısı",
            "slug": "turkishpedia",
            "description": "Editör, yayıncı ve yönetici ekiplerinin içerik ve belge akışını izleyebildiği, merkezi arama destekli bilgi platformu altyapısı.",
            "client_name": "Turkishpedia",
            "industry": "Medya ve Bilgi Sistemleri",
            "location": "Türkiye",
            "delivery_year": "2024",
            "scope_summary": "İçerik workflow, arama, yönetim paneli ve denetim izi",
            "highlight_metric": "%58 daha hızlı editoryal akış",
            "challenge": "Yayın süreci; içerik, belge ve görev tarafında parçalı ilerliyordu. Denetim izi ve yönetici takibi yeterli değildi.",
            "solution": "Denetim kayıtları, editoryal aşama takibi, merkezi arama ve dosya yönetimi modülleri içeren modüler kurumsal arka ofis geliştirildi.",
            "results": "Editöryal ekipler arası görünürlük güçlendi, onay süreçleri kısaldı ve içerik operasyonu standartlaştı.",
            "technologies": "Python\nDjango\nElasticsearch\nCelery\nAudit Logging",
            "project_url": "",
            "is_featured": True,
            "is_live": True,
            "order": 3,
        },
    ]


def _reference_defaults() -> list[dict[str, str | bool | int]]:
    return [
        {
            "portfolio_slug": "iduk",
            "company_name": "Iduk",
            "person_name": "Merve A.",
            "role": "Operasyon Direktörü",
            "quote": "TurkishSystems ekibi sadece yazılım teslim etmedi; operasyonumuzu sadeleştiren, müşterilerimizle daha hızlı belge paylaştığımız ve süreci net takip ettiğimiz bir altyapı kurdu.",
            "outcome": "İçerik ve görev akışlarında ölçülebilir hız artışı",
            "sector": "Eğitim",
            "is_featured": True,
            "order": 1,
        },
        {
            "portfolio_slug": "sormaca",
            "company_name": "Sormaca",
            "person_name": "Onur T.",
            "role": "Dijital Operasyon Yöneticisi",
            "quote": "Canlı etkinlik akışlarımız daha görünür hale geldi. Portal mantığıyla çalışan yönetim panelleri sayesinde ekip koordinasyonu ciddi biçimde iyileşti.",
            "outcome": "Gerçek zamanlı operasyon görünürlüğü",
            "sector": "Etkinlik",
            "is_featured": True,
            "order": 2,
        },
        {
            "portfolio_slug": "turkishpedia",
            "company_name": "Turkishpedia",
            "person_name": "Ayşe K.",
            "role": "Yayın Koordinatörü",
            "quote": "Dosya paylaşımı, görev geçmişi ve onay takibi artık tek yerde. Teknik altyapı kadar süreç tasarımında da çok güçlü ilerlediler.",
            "outcome": "Editoryal süreçlerde merkezi takip",
            "sector": "Medya",
            "is_featured": True,
            "order": 3,
        },
    ]


def _pricing_defaults() -> list[dict[str, str | bool]]:
    return [
        {
            "name": "Başlangıç",
            "price": "₺24.900",
            "description": "Tek modül, hızlı kurulum ve kontrollü kapsam isteyen işler için.",
            "features": "Tek akışlı panel\nTemel rol yönetimi\nCanlıya alma desteği\n30 gün destek",
            "is_highlighted": False,
        },
        {
            "name": "Büyüme",
            "price": "₺64.900",
            "description": "Portal, entegrasyon ve takip katmanı birlikte çalışan projeler için.",
            "features": "Müşteri portalı\nDosya paylaşım alanı\nRaporlama ve bildirimler\n90 gün destek",
            "is_highlighted": True,
        },
        {
            "name": "Kurumsal",
            "price": "Özel Teklif",
            "description": "Çok ekipli, SLA gerektiren ve entegrasyon yoğun kurumsal operasyonlar için.",
            "features": "Çoklu panel mimarisi\nSLA ve izleme\nÖzel entegrasyon katmanı\nSürekli teknik partnerlik",
            "is_highlighted": False,
        },
    ]


def _product_defaults() -> list[dict[str, object]]:
    return [
        {
            "name": "Kurumsal E-Ticaret Platformu",
            "slug": "kurumsal-e-ticaret-platformu",
            "short_description": "E-ticaret altyapınızı kurumsal düzeyde tasarlıyor, geliştiriyor ve yönetiyoruz.",
            "detailed_features": "Ürün ve stok yönetimi\nÖdeme entegrasyonları\nSEO ve performans\nYönetim paneli\nKampanya ve fiyat motoru\nKargo entegrasyonu",
            "order": 1,
            "is_active": True,
            "packages": [],
            "reviews": [],
            "faqs": [],
        },
        {
            "name": "Sunucu Yönetimi",
            "slug": "sunucu-yonetimi",
            "short_description": "Sunucu kurulumu, izleme, güvenlik ve yedekleme süreçlerinizi profesyonelce yönetiyoruz.",
            "detailed_features": "Sunucu kurulumu ve yapılandırma\nGüvenlik sertleştirme\nYedekleme ve felaket planı\nPerformans izleme\nUptime takibi\nGüncelleme yönetimi",
            "order": 2,
            "is_active": True,
            "packages": [],
            "reviews": [],
            "faqs": [],
        },
        {
            "name": "Müşteri Portalı Platformu",
            "slug": "musteri-portali-platformu",
            "short_description": "Dosya paylaşımı, süreç takibi ve bildirim yapılarıyla müşterilerinizle senkron çalışan portal altyapısı.",
            "detailed_features": "Güvenli belge paylaşımı\nSüreç takibi\nBildirim akışları\nRol bazlı erişim\nYorum ve geri bildirim\nYönetici raporlama",
            "order": 3,
            "is_active": True,
            "packages": [],
            "reviews": [],
            "faqs": [],
        },
        {
            "name": "Kurumsal Web ve Başvuru Platformu",
            "slug": "kurumsal-web-ve-basvuru-platformu",
            "short_description": "Kurumsal web varlığınızı ve başvuru süreçlerinizi tek platform üzerinde yönetin.",
            "detailed_features": "Kurumsal web sitesi\nBaşvuru formları\nYönetim paneli\nSEO ve performans\nİçerik operasyonu\nEntegrasyon desteği",
            "order": 4,
            "is_active": True,
            "packages": [],
            "reviews": [],
            "faqs": [],
        },
    ]


def _social_defaults() -> list[dict[str, str]]:
    return [
        {"label": "Github", "url": "https://github.com/erissos"},
        {"label": "LinkedIn", "url": "https://www.linkedin.com/in/adem-mertkan-durmaz-683667251/"},
    ]


def _update_fields(instance, defaults: dict[str, object], skip_fields: set[str] | None = None) -> None:
    skip_fields = skip_fields or set()
    changed_fields: list[str] = []
    for field, value in defaults.items():
        if field in skip_fields:
            continue
        if getattr(instance, field) != value:
            setattr(instance, field, value)
            changed_fields.append(field)
    if changed_fields:
        instance.save(update_fields=changed_fields)


def _ensure_defaults() -> SiteSettings:
    settings_obj, _ = SiteSettings.objects.get_or_create(id=1, defaults=_site_defaults())
    _update_fields(settings_obj, _site_defaults())

    legacy_products_link = NavLink.objects.filter(label="Sistemler").first()
    if legacy_products_link:
        legacy_products_link.label = "Ürünler"
        legacy_products_link.save(update_fields=["label"])

    for link_defaults in _nav_defaults():
        links = list(NavLink.objects.filter(label=link_defaults["label"]).order_by("id"))
        if links:
            link = links[0]
            for duplicate_link in links[1:]:
                duplicate_link.delete()
        else:
            link = NavLink.objects.create(**link_defaults)
        _update_fields(link, link_defaults)

    for index, stat_defaults in enumerate(_stat_defaults(), start=1):
        stat, _ = Stat.objects.get_or_create(order=index, defaults={**stat_defaults, "order": index})
        _update_fields(stat, {**stat_defaults, "order": index})

    for index, service_defaults in enumerate(_service_defaults(), start=1):
        service, _ = Service.objects.get_or_create(title=service_defaults["title"], defaults={**service_defaults, "order": index})
        _update_fields(service, {**service_defaults, "order": index})

    for item_defaults in _portfolio_defaults():
        slug = item_defaults["slug"]
        portfolio_item, _ = PortfolioItem.objects.get_or_create(slug=slug, defaults=item_defaults)
        _update_fields(portfolio_item, item_defaults)

    slug_map = {item.slug: item for item in PortfolioItem.objects.all()}
    for reference_defaults in _reference_defaults():
        defaults = {k: v for k, v in reference_defaults.items() if k != "portfolio_slug"}
        defaults["portfolio_item"] = slug_map.get(reference_defaults["portfolio_slug"])
        reference, _ = Reference.objects.get_or_create(
            company_name=reference_defaults["company_name"],
            person_name=reference_defaults["person_name"],
            defaults=defaults,
        )
        _update_fields(reference, defaults)

    for index, package_defaults in enumerate(_pricing_defaults(), start=1):
        package, _ = PricingPackage.objects.get_or_create(name=package_defaults["name"], defaults={**package_defaults, "order": index})
        _update_fields(package, {**package_defaults, "order": index})

    for index, social_defaults in enumerate(_social_defaults(), start=1):
        social, _ = SocialLink.objects.get_or_create(label=social_defaults["label"], defaults={**social_defaults, "order": index})
        _update_fields(social, {**social_defaults, "order": index})

    seeded_product_slugs: list[str] = []
    for product_defaults in _product_defaults():
        product_data = {k: v for k, v in product_defaults.items() if k not in {"packages", "reviews", "faqs"}}
        product, _ = Product.objects.get_or_create(slug=product_data["slug"], defaults=product_data)
        _update_fields(product, product_data)
        seeded_product_slugs.append(product.slug)

        for package_defaults in product_defaults["packages"]:
            package, _ = ProductPackage.objects.get_or_create(
                product=product,
                name=package_defaults["name"],
                defaults=package_defaults,
            )
            _update_fields(package, package_defaults)

        for review_defaults in product_defaults["reviews"]:
            review, _ = ProductReview.objects.get_or_create(
                product=product,
                full_name=review_defaults["full_name"],
                defaults=review_defaults,
            )
            _update_fields(review, review_defaults)

        for faq_defaults in product_defaults["faqs"]:
            faq, _ = ProductFAQ.objects.get_or_create(
                product=product,
                question=faq_defaults["question"],
                defaults={**faq_defaults, "is_active": True},
            )
            _update_fields(faq, {**faq_defaults, "is_active": True})

    Product.objects.exclude(slug__in=seeded_product_slugs).update(is_active=False)

    return settings_obj


def _base_context(settings_obj: SiteSettings, request) -> dict:
    featured_portfolio = PortfolioItem.objects.filter(is_featured=True)
    featured_references = Reference.objects.filter(is_featured=True)
    return {
        "site": settings_obj,
        "nav_links": NavLink.objects.all(),
        "social_links": SocialLink.objects.all(),
        "portal_url": PORTAL_URL,
        "featured_portfolio": featured_portfolio,
        "featured_references": featured_references,
        "request": request,
    }


def _form_values(form) -> dict[str, object]:
    return {name: form[name].value() or "" for name in form.fields}


def home(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj, request),
        "stats": Stat.objects.all(),
        "services": Service.objects.all()[:3],
        "portfolio_items": PortfolioItem.objects.filter(is_featured=True)[:3],
        "products": Product.objects.filter(is_active=True)[:3],
        "portal_highlights": [
            {
                "title": "Müşteriye özel giriş ve görünüm",
                "body": "Her müşteri kendi dosyalarını, taleplerini ve süreç adımlarını kendine özel ekrandan takip eder.",
            },
            {
                "title": "Hızlı dosya paylaşımı",
                "body": "Dosyalar merkezi akışta tutulur; sürüm, teslim ve onay süreçleri karışmadan ilerler.",
            },
            {
                "title": "Güçlü takip katmanı",
                "body": "Yönetici ekipleri gecikme, teslim ve aksiyon noktalarını tek panelden görebilir.",
            },
        ],
    }
    return render(request, "main/home.jinja", context, using="jinja2")


def about_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj, request),
        "stats": Stat.objects.all(),
        "references": Reference.objects.filter(is_featured=True),
    }
    return render(request, "main/about.jinja", context, using="jinja2")


def services_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj, request),
        "services": Service.objects.all(),
        "delivery_layers": [
            "Keşif ve süreç analizi",
            "Bilgi mimarisi ve ekran akışları",
            "Portal ve yönetim paneli geliştirme",
            "Entegrasyon, test ve canlıya alma",
        ],
    }
    return render(request, "main/services.jinja", context, using="jinja2")


def portfolio_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj, request),
        "portfolio_items": PortfolioItem.objects.all(),
        "references": Reference.objects.select_related("portfolio_item").all(),
    }
    return render(request, "main/portfolio_list.jinja", context, using="jinja2")


def products_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj, request),
        "products": Product.objects.filter(is_active=True),
        "portal_summary": {
            "title": "Portal Altyapımız",
            "body": "Müşteri portalı; sattığımız ürünlerden ayrı olarak kurumlara özel tasarladığımız operasyon katmanıdır. Dosya paylaşımı, talep takibi ve ekip senkronunu aynı yerde toplar.",
        },
    }
    return render(request, "main/products_list.jinja", context, using="jinja2")


def product_detail(request, slug: str):
    settings_obj = _ensure_defaults()
    product = get_object_or_404(Product, slug=slug, is_active=True)
    packages = product.packages.all()
    reviews = product.reviews.filter(is_published=True)
    faqs = product.faqs.filter(is_active=True)
    form_data = {
        "full_name": request.user.first_name if request.user.is_authenticated else "",
        "email": request.user.email if request.user.is_authenticated else "",
        "phone": "",
        "detail_note": "",
        "package_id": "",
    }
    order_error = ""

    if request.method == "POST":
        package_id = request.POST.get("package_id", "").strip()
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        detail_note = request.POST.get("detail_note", "").strip()
        form_data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "detail_note": detail_note,
            "package_id": package_id,
        }

        selected_package = packages.filter(id=package_id).first() if package_id else None
        if not selected_package:
            order_error = "Lütfen bir paket seçin."
        elif not full_name or not email:
            order_error = "Ad soyad ve e-posta alanları zorunludur."
        elif selected_package.ask_details_on_order and not detail_note:
            order_error = "Bu paket için lütfen proje detaylarını belirtin."
        else:
            ProductOrder.objects.create(
                product=product,
                package=selected_package,
                full_name=full_name,
                email=email,
                phone=phone,
                detail_note=detail_note,
            )
            messages.success(request, "Paket talebiniz alındı. Teknik ekibimiz kısa sürede size dönecek.")
            return redirect(product.get_absolute_url())

    context = {
        **_base_context(settings_obj, request),
        "product": product,
        "packages": packages,
        "reviews": reviews,
        "faqs": faqs,
        "order_error": order_error,
        "order_form": form_data,
    }
    return render(request, "main/product_detail.jinja", context, using="jinja2")


def portfolio_detail(request, slug: str = "", pk: int | None = None):
    settings_obj = _ensure_defaults()
    if pk is not None:
        item = get_object_or_404(PortfolioItem, pk=pk)
    else:
        item = get_object_or_404(PortfolioItem, slug=slug)
    related_items = PortfolioItem.objects.exclude(id=item.id).filter(is_featured=True)[:3]
    context = {
        **_base_context(settings_obj, request),
        "item": item,
        "related_items": related_items,
        "project_references": item.references.all(),
    }
    return render(request, "main/portfolio_detail.jinja", context, using="jinja2")


def contact_page(request):
    settings_obj = _ensure_defaults()
    initial = {}
    if request.user.is_authenticated:
        initial = {
            "full_name": request.user.first_name,
            "email": request.user.email,
            "wants_portal_access": True,
        }
    form = ProjectRequestForm(initial=initial)

    if request.method == "POST":
        form = ProjectRequestForm(request.POST)
        if form.is_valid():
            project_request = form.save(commit=False)
            if request.user.is_authenticated:
                project_request.user = request.user
            project_request.save()
            messages.success(request, "Talebiniz alındı. Kapsam ve öncelik planlaması için sizinle iletişime geçeceğiz.")
            return redirect("contact")

    context = {
        **_base_context(settings_obj, request),
        "request_form": form,
        "request_values": _form_values(form),
        "request_errors": form.errors,
        "request_type_choices": ProjectRequest.REQUEST_TYPE_CHOICES,
        "budget_choices": ProjectRequest.BUDGET_CHOICES,
        "timeline_choices": ProjectRequest.TIMELINE_CHOICES,
    }
    return render(request, "main/contact.jinja", context, using="jinja2")


def account_auth_page(request):
    settings_obj = _ensure_defaults()
    if request.user.is_authenticated:
        return redirect("dashboard")

    sign_in_form = SignInForm()
    sign_up_form = SignUpForm()
    active_tab = "signin"

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "signup":
            active_tab = "signup"
            sign_up_form = SignUpForm(request.POST)
            if sign_up_form.is_valid():
                user = sign_up_form.save()
                login(request, user)
                messages.success(request, "Hesabınız oluşturuldu. Artık taleplerinizi hesabınızdan takip edebilirsiniz.")
                return redirect("dashboard")
        else:
            sign_in_form = SignInForm(request.POST)
            if sign_in_form.is_valid():
                login(request, sign_in_form.get_user())
                messages.success(request, "Hesabınıza giriş yapıldı.")
                return redirect("dashboard")

    context = {
        **_base_context(settings_obj, request),
        "sign_in_form": sign_in_form,
        "sign_up_form": sign_up_form,
        "sign_in_values": _form_values(sign_in_form),
        "sign_up_values": _form_values(sign_up_form),
        "sign_in_errors": sign_in_form.errors,
        "sign_up_errors": sign_up_form.errors,
        "active_tab": active_tab,
    }
    return render(request, "main/account_auth.jinja", context, using="jinja2")


@login_required
def dashboard_page(request):
    settings_obj = _ensure_defaults()
    requests_qs = ProjectRequest.objects.filter(user=request.user)
    orders_qs = ProductOrder.objects.filter(email=request.user.email)
    context = {
        **_base_context(settings_obj, request),
        "requests_qs": requests_qs,
        "orders_qs": orders_qs,
        "display_name": request.user.first_name or request.user.username,
    }
    return render(request, "main/dashboard.jinja", context, using="jinja2")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, "Oturum kapatıldı.")
    return redirect("home")