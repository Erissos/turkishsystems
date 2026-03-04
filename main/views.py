from django.shortcuts import get_object_or_404, render

from .models import (
    NavLink,
    PortfolioItem,
    PricingPackage,
    Product,
    ProductFAQ,
    ProductOrder,
    ProductPackage,
    ProductReview,
    Service,
    SiteSettings,
    SocialLink,
    Stat,
)


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
                NavLink(label="Ürünler", url="/urunler/", order=3),
                NavLink(label="Referanslar", url="/portfolyo/", order=4),
                NavLink(label="İş Birliği Başlat", url="/iletisim/", is_primary=True, order=5),
            ]
        )
    else:
        default_link_map = {
            "Kurumsal": "/kurumsal/",
            "Hizmetler": "/hizmetler/",
            "Ürünler": "/urunler/",
            "Portfolyo": "/portfolyo/",
            "Referanslar": "/portfolyo/",
            "İş Birliği Başlat": "/iletisim/",
        }
        for link in NavLink.objects.all():
            if link.label in default_link_map and link.url.startswith("#"):
                link.url = default_link_map[link.label]
                link.save(update_fields=["url"])
        if not NavLink.objects.filter(label="Ürünler").exists():
            NavLink.objects.create(label="Ürünler", url="/urunler/", order=3)

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
                    title="Sosyal Medya Yönetimi",
                    description=(
                        "Marka kimliğinize uygun içerik planlama, yaratıcı tasarım "
                        "ve veri odaklı kampanya yönetimi ile sosyal medya varlığınızı "
                        "ölçeklenebilir bir büyüme kanalına dönüştürüyoruz."
                    ),
                    bullet_one="İçerik Takvimi ve Kreatif Üretim",
                    bullet_two="Reklam Yönetimi ve Performans Raporlama",
                    icon_class="fa-solid fa-hashtag",
                    accent_class="blue",
                    order=1,
                ),
                Service(
                    title="Web Siteleri",
                    description=(
                        "Kurumsal vitrinden dönüşüm odaklı satış sitelerine kadar, "
                        "hızlı, SEO uyumlu ve yönetilebilir web çözümleri geliştiriyoruz."
                    ),
                    bullet_one="Modern Arayüz ve Güçlü Altyapı",
                    bullet_two="SEO ve Hız Optimizasyonu",
                    icon_class="fa-solid fa-globe",
                    accent_class="purple",
                    order=2,
                ),
                Service(
                    title="Mobil Uygulamalar",
                    description=(
                        "iOS ve Android platformları için kullanıcı deneyimi yüksek, "
                        "ölçeklenebilir ve sürdürülebilir mobil uygulamalar üretiyoruz."
                    ),
                    bullet_one="Native ve Cross-Platform Geliştirme",
                    bullet_two="Yayın, Bakım ve Sürüm Süreçleri",
                    icon_class="fa-solid fa-mobile-screen-button",
                    accent_class="pink",
                    order=3,
                ),
                Service(
                    title="Otomasyon Sistemi",
                    description=(
                        "Tekrarlayan iş süreçlerini dijitalleştirerek operasyonel verimliliği "
                        "artıran, ölçülebilir ve ölçeklenebilir otomasyon altyapıları kuruyoruz."
                    ),
                    bullet_one="İş Akışı ve Süreç Otomasyonu",
                    bullet_two="Raporlama ve Entegrasyon Altyapısı",
                    icon_class="fa-solid fa-robot",
                    accent_class="blue",
                    order=4,
                ),
                Service(
                    title="Sunucu Yönetimi",
                    description=(
                        "Sunucu kurulumundan izleme ve güvenliğe kadar tüm altyapı operasyonlarını "
                        "proaktif yaklaşımla yönetiyor, kesintisiz hizmet sağlıyoruz."
                    ),
                    bullet_one="Kurulum, İzleme ve Performans Yönetimi",
                    bullet_two="Güvenlik, Yedekleme ve Süreklilik",
                    icon_class="fa-solid fa-server",
                    accent_class="purple",
                    order=5,
                ),
                Service(
                    title="Kurumsal Kaynak Uygulamaları",
                    description=(
                        "İşletmenize özel ERP, CRM ve kaynak planlama çözümleri geliştirerek "
                        "ekipler arası veri akışını tek merkezde birleştiriyoruz."
                    ),
                    bullet_one="ERP/CRM Geliştirme ve Özelleştirme",
                    bullet_two="Departmanlar Arası Entegre Veri Akışı",
                    icon_class="fa-solid fa-building",
                    accent_class="pink",
                    order=6,
                ),
            ]
        )
    else:
        _SRV_DEFAULTS = [
            {
                "title": "Sosyal Medya Yönetimi",
                "description": (
                    "Marka kimliğinize uygun içerik planlama, yaratıcı tasarım "
                    "ve veri odaklı kampanya yönetimi ile sosyal medya varlığınızı "
                    "ölçeklenebilir bir büyüme kanalına dönüştürüyoruz."
                ),
                "bullet_one": "İçerik Takvimi ve Kreatif Üretim",
                "bullet_two": "Reklam Yönetimi ve Performans Raporlama",
                "icon_class": "fa-solid fa-hashtag",
                "accent_class": "blue",
            },
            {
                "title": "Web Siteleri",
                "description": (
                    "Kurumsal vitrinden dönüşüm odaklı satış sitelerine kadar, "
                    "hızlı, SEO uyumlu ve yönetilebilir web çözümleri geliştiriyoruz."
                ),
                "bullet_one": "Modern Arayüz ve Güçlü Altyapı",
                "bullet_two": "SEO ve Hız Optimizasyonu",
                "icon_class": "fa-solid fa-globe",
                "accent_class": "purple",
            },
            {
                "title": "Mobil Uygulamalar",
                "description": (
                    "iOS ve Android platformları için kullanıcı deneyimi yüksek, "
                    "ölçeklenebilir ve sürdürülebilir mobil uygulamalar üretiyoruz."
                ),
                "bullet_one": "Native ve Cross-Platform Geliştirme",
                "bullet_two": "Yayın, Bakım ve Sürüm Süreçleri",
                "icon_class": "fa-solid fa-mobile-screen-button",
                "accent_class": "pink",
            },
            {
                "title": "Otomasyon Sistemi",
                "description": (
                    "Tekrarlayan iş süreçlerini dijitalleştirerek operasyonel verimliliği "
                    "artıran, ölçülebilir ve ölçeklenebilir otomasyon altyapıları kuruyoruz."
                ),
                "bullet_one": "İş Akışı ve Süreç Otomasyonu",
                "bullet_two": "Raporlama ve Entegrasyon Altyapısı",
                "icon_class": "fa-solid fa-robot",
                "accent_class": "blue",
            },
            {
                "title": "Sunucu Yönetimi",
                "description": (
                    "Sunucu kurulumundan izleme ve güvenliğe kadar tüm altyapı operasyonlarını "
                    "proaktif yaklaşımla yönetiyor, kesintisiz hizmet sağlıyoruz."
                ),
                "bullet_one": "Kurulum, İzleme ve Performans Yönetimi",
                "bullet_two": "Güvenlik, Yedekleme ve Süreklilik",
                "icon_class": "fa-solid fa-server",
                "accent_class": "purple",
            },
            {
                "title": "Kurumsal Kaynak Uygulamaları",
                "description": (
                    "İşletmenize özel ERP, CRM ve kaynak planlama çözümleri geliştirerek "
                    "ekipler arası veri akışını tek merkezde birleştiriyoruz."
                ),
                "bullet_one": "ERP/CRM Geliştirme ve Özelleştirme",
                "bullet_two": "Departmanlar Arası Entegre Veri Akışı",
                "icon_class": "fa-solid fa-building",
                "accent_class": "pink",
            },
        ]
        existing_services = list(Service.objects.order_by("order", "id"))
        for i, d in enumerate(_SRV_DEFAULTS, start=1):
            if i <= len(existing_services):
                srv = existing_services[i - 1]
                updated = False
                for field, val in d.items():
                    if getattr(srv, field) != val:
                        setattr(srv, field, val)
                        updated = True
                if srv.order != i:
                    srv.order = i
                    updated = True
                if updated:
                    srv.save()
            else:
                Service.objects.create(order=i, **d)

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

    if not Product.objects.exists():
        product = Product.objects.create(
            name="Kurumsal E-Ticaret Platformu",
            slug="kurumsal-e-ticaret-platformu",
            short_description="Yüksek trafikli, ödeme ve stok yönetimi içeren uçtan uca e-ticaret çözümü.",
            detailed_features="Çoklu mağaza ve bayi yönetimi\nCanlı stok ve dinamik fiyatlama\nİleri seviye raporlama panelleri\nÖdeme ve kargo entegrasyonları\nRBAC tabanlı yetkilendirme\nKurumsal ERP/CRM veri senkronizasyonu\nWebhook ve event-driven mimari\nSEO ve performans optimizasyonu",
            order=1,
            is_active=True,
        )

        ProductPackage.objects.bulk_create(
            [
                ProductPackage(
                    product=product,
                    name="Temel",
                    price="₺29.900",
                    description="MVP ve ilk satışa çıkış için ideal başlangıç paketi.",
                    features="Ürün kataloğu ve sipariş akışı\nAdmin paneli\nÖdeme sistemi entegrasyonu\n1 ay teknik destek",
                    ask_details_on_order=False,
                    order=1,
                ),
                ProductPackage(
                    product=product,
                    name="Profesyonel",
                    price="₺69.900",
                    description="Büyüyen operasyonlar için gelişmiş otomasyon ve entegrasyon paketi.",
                    features="Gelişmiş kampanya motoru\nKargo/ERP/CRM entegrasyonları\nPerformans optimizasyonu\n3 ay teknik destek",
                    is_highlighted=True,
                    ask_details_on_order=True,
                    order=2,
                ),
                ProductPackage(
                    product=product,
                    name="Kurumsal",
                    price="Özel Teklif",
                    description="Yüksek SLA ve özel iş akışları gerektiren kurumlara tam kapsamlı çözüm.",
                    features="Çoklu marka/çoklu ülke desteği\nÖzelleştirilmiş rol ve onay süreçleri\n7/24 izleme\nSLA güvenceli destek",
                    ask_details_on_order=True,
                    order=3,
                ),
            ]
        )

        ProductReview.objects.bulk_create(
            [
                ProductReview(
                    product=product,
                    full_name="Merve A.",
                    role="E-Ticaret Operasyon Yöneticisi",
                    comment="Sipariş ve stok süreçlerimiz çok daha yönetilebilir hale geldi. Ekip hem teknik hem iletişimde çok güçlüydü.",
                    order=1,
                ),
                ProductReview(
                    product=product,
                    full_name="Onur T.",
                    role="Dijital Dönüşüm Direktörü",
                    comment="Kurumsal entegrasyonlarımız sorunsuz ilerledi. Özellikle raporlama tarafında ciddi verim aldık.",
                    order=2,
                ),
            ]
        )

        ProductFAQ.objects.bulk_create(
            [
                ProductFAQ(
                    product=product,
                    question="Kurulum ne kadar sürede tamamlanır?",
                    answer="Proje kapsamına göre 3-10 hafta arasında üretime alınır.",
                    order=1,
                ),
                ProductFAQ(
                    product=product,
                    question="Mevcut sistemlerimizle entegrasyon mümkün mü?",
                    answer="Evet. ERP, CRM, ödeme ve kargo servislerine özel entegrasyon katmanı geliştiriyoruz.",
                    order=2,
                ),
            ]
        )

    # Keep services mirrored as product cards so they are visible under /urunler/ as well.
    max_product_order = Product.objects.order_by("-order", "-id").first()
    next_order = (max_product_order.order if max_product_order else 0) + 1
    for service in Service.objects.order_by("order", "id"):
        defaults = {
            "short_description": service.description,
            "detailed_features": f"{service.bullet_one}\n{service.bullet_two}",
            "order": next_order,
            "is_active": True,
        }
        product_obj, created = Product.objects.get_or_create(name=service.title, defaults=defaults)
        if created:
            next_order += 1
            continue

        updated = False
        if product_obj.short_description != service.description:
            product_obj.short_description = service.description
            updated = True
        desired_features = f"{service.bullet_one}\n{service.bullet_two}"
        if product_obj.detailed_features != desired_features:
            product_obj.detailed_features = desired_features
            updated = True
        if not product_obj.is_active:
            product_obj.is_active = True
            updated = True
        if updated:
            product_obj.save()

    # Complete missing product detail sections for all products.
    for product_obj in Product.objects.all().order_by("order", "id"):
        default_packages = [
            {
                "name": "Başlangıç",
                "price": "₺19.900",
                "description": "Hızlı kurulum ve temel ihtiyaçlar için başlangıç paketi.",
                "features": "Kurulum ve temel yapılandırma\nTemel kullanıcı akışı\nYayın desteği",
                "is_highlighted": False,
                "ask_details_on_order": False,
                "order": 1,
            },
            {
                "name": "Profesyonel",
                "price": "₺49.900",
                "description": "Gelişmiş özellikler ve entegrasyon gerektiren projeler için.",
                "features": "Gelişmiş modül ve entegrasyonlar\nPerformans iyileştirmeleri\nÖncelikli teknik destek",
                "is_highlighted": True,
                "ask_details_on_order": True,
                "order": 2,
            },
            {
                "name": "Kurumsal",
                "price": "Özel Teklif",
                "description": "Kurumlara özel kapsam, SLA ve ölçeklenebilir mimari.",
                "features": "Özel mimari planlama\nSLA odaklı destek modeli\nSüreçlere özel uyarlama",
                "is_highlighted": False,
                "ask_details_on_order": True,
                "order": 3,
            },
        ]

        for pkg_defaults in default_packages:
            same_name_qs = ProductPackage.objects.filter(
                product=product_obj,
                name=pkg_defaults["name"],
            ).order_by("id")

            if same_name_qs.exists():
                pkg = same_name_qs.first()
                # Remove duplicate rows with the same package name for this product.
                for duplicate_pkg in same_name_qs[1:]:
                    duplicate_pkg.delete()

                package_updated = False
                for field in (
                    "price",
                    "description",
                    "features",
                    "is_highlighted",
                    "ask_details_on_order",
                    "order",
                ):
                    if getattr(pkg, field) != pkg_defaults[field]:
                        setattr(pkg, field, pkg_defaults[field])
                        package_updated = True
                if package_updated:
                    pkg.save()
            else:
                ProductPackage.objects.create(product=product_obj, **pkg_defaults)

        if not product_obj.reviews.exists():
            ProductReview.objects.bulk_create(
                [
                    ProductReview(
                        product=product_obj,
                        full_name="Ayşe K.",
                        role="Operasyon Müdürü",
                        comment=f"{product_obj.name} çözümü ile süreçlerimiz daha düzenli ve ölçülebilir hale geldi.",
                        order=1,
                        is_published=True,
                    ),
                    ProductReview(
                        product=product_obj,
                        full_name="Mehmet D.",
                        role="Teknoloji Yöneticisi",
                        comment="Kurulum ve devreye alma süreci planlı ilerledi, ekip hızlı geri dönüş sağladı.",
                        order=2,
                        is_published=True,
                    ),
                ]
            )

        default_faqs = [
            {
                "question": "Bu ürün ne kadar sürede devreye alınır?",
                "answer": "Kapsama göre ortalama 2-8 hafta içinde canlıya alınır.",
                "order": 1,
                "is_active": True,
            },
            {
                "question": "Mevcut sistemlerimizle entegre olur mu?",
                "answer": "Evet, API ve veri aktarım katmanlarıyla mevcut sistemlerinize entegre edilebilir.",
                "order": 2,
                "is_active": True,
            },
        ]

        for faq_defaults in default_faqs:
            same_question_qs = ProductFAQ.objects.filter(
                product=product_obj,
                question=faq_defaults["question"],
            ).order_by("id")

            if same_question_qs.exists():
                faq_obj = same_question_qs.first()
                # Remove repeated FAQ rows with the same question for this product.
                for duplicate_faq in same_question_qs[1:]:
                    duplicate_faq.delete()

                faq_updated = False
                for field in ("answer", "order", "is_active"):
                    if getattr(faq_obj, field) != faq_defaults[field]:
                        setattr(faq_obj, field, faq_defaults[field])
                        faq_updated = True
                if faq_updated:
                    faq_obj.save()
            else:
                ProductFAQ.objects.create(product=product_obj, **faq_defaults)

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
    }
    return render(request, "main/services.jinja", context, using="jinja2")


def portfolio_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj),
        "portfolio_items": PortfolioItem.objects.all(),
    }
    return render(request, "main/portfolio_list.jinja", context, using="jinja2")


def products_page(request):
    settings_obj = _ensure_defaults()
    context = {
        **_base_context(settings_obj),
        "products": Product.objects.filter(is_active=True),
    }
    return render(request, "main/products_list.jinja", context, using="jinja2")


def product_detail(request, slug: str):
    settings_obj = _ensure_defaults()
    product = get_object_or_404(Product, slug=slug, is_active=True)
    packages = product.packages.all()
    reviews = product.reviews.filter(is_published=True)
    faqs = product.faqs.filter(is_active=True)

    order_success = False
    order_error = ""

    if request.method == "POST":
        package_id = request.POST.get("package_id", "").strip()
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        detail_note = request.POST.get("detail_note", "").strip()

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
            order_success = True

    context = {
        **_base_context(settings_obj),
        "product": product,
        "packages": packages,
        "reviews": reviews,
        "faqs": faqs,
        "order_success": order_success,
        "order_error": order_error,
    }
    return render(request, "main/product_detail.jinja", context, using="jinja2")


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
