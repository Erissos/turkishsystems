from django.conf import settings
from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField(blank=True)
    brand_name = models.CharField(max_length=120)
    brand_highlight = models.CharField(max_length=120, blank=True)

    hero_badge_year = models.CharField(max_length=10)
    hero_badge_text = models.CharField(max_length=200)
    hero_heading_line_one = models.CharField(max_length=200)
    hero_heading_highlight_one = models.CharField(max_length=200)
    hero_heading_line_two = models.CharField(max_length=200)
    hero_heading_highlight_two = models.CharField(max_length=200)
    hero_subtitle = models.TextField()
    primary_cta_label = models.CharField(max_length=120)
    primary_cta_url = models.CharField(max_length=200)
    secondary_cta_label = models.CharField(max_length=120)
    secondary_cta_url = models.CharField(max_length=200)

    services_title = models.CharField(max_length=200)
    portfolio_title = models.CharField(max_length=200)

    contact_title = models.CharField(max_length=200)
    contact_body = models.TextField()
    contact_button_label = models.CharField(max_length=120)
    contact_button_url = models.CharField(max_length=200)
    contact_whatsapp_url = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_linkedin_url = models.CharField(max_length=200, blank=True)

    footer_intro = models.TextField()
    footer_copyright = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.brand_name


class NavLink(models.Model):
    label = models.CharField(max_length=120)
    url = models.CharField(max_length=200)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.label


class Stat(models.Model):
    value = models.CharField(max_length=50)
    label = models.CharField(max_length=120)
    color_class = models.CharField(max_length=40, default="text-white")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.value} - {self.label}"


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    bullet_one = models.CharField(max_length=200)
    bullet_two = models.CharField(max_length=200)
    icon_class = models.CharField(max_length=80)
    accent_class = models.CharField(max_length=40, default="blue")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.title


class PortfolioItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True)
    client_name = models.CharField(max_length=160, blank=True)
    industry = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=120, blank=True)
    delivery_year = models.CharField(max_length=20, blank=True)
    scope_summary = models.CharField(max_length=220, blank=True)
    highlight_metric = models.CharField(max_length=120, blank=True)
    challenge = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    results = models.TextField(blank=True)
    technologies = models.TextField(blank=True, help_text="Her satıra bir teknoloji yazın")
    project_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_live = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.title

    @property
    def image_url(self) -> str:
        if self.image:
            return self.image.url
        return ""

    def get_absolute_url(self) -> str:
        from django.urls import reverse

        if self.slug:
            return reverse("portfolio_detail", kwargs={"slug": self.slug})
        return reverse("portfolio_detail_id", kwargs={"pk": self.pk})

    def get_technology_list(self) -> list[str]:
        return [item.strip() for item in self.technologies.split("\n") if item.strip()]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Reference(models.Model):
    portfolio_item = models.ForeignKey(
        PortfolioItem,
        on_delete=models.SET_NULL,
        related_name="references",
        null=True,
        blank=True,
    )
    company_name = models.CharField(max_length=160)
    person_name = models.CharField(max_length=120)
    role = models.CharField(max_length=160, blank=True)
    quote = models.TextField()
    outcome = models.CharField(max_length=200, blank=True)
    sector = models.CharField(max_length=120, blank=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.company_name} - {self.person_name}"


class SocialLink(models.Model):
    label = models.CharField(max_length=120)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.label


class PricingPackage(models.Model):
    name = models.CharField(max_length=120)
    price = models.CharField(max_length=80)
    description = models.TextField()
    features = models.TextField(help_text="Her satıra bir özellik yazın")
    is_highlighted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.name

    def get_features_list(self) -> list[str]:
        return [feature.strip() for feature in self.features.split("\n") if feature.strip()]


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.TextField()
    detailed_features = models.TextField(help_text="Her satıra bir detaylı özellik yazın")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        from django.urls import reverse

        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_detailed_features_list(self) -> list[str]:
        return [item.strip() for item in self.detailed_features.split("\n") if item.strip()]


class ProductPackage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="packages")
    name = models.CharField(max_length=120)
    price = models.CharField(max_length=80)
    description = models.TextField()
    features = models.TextField(help_text="Her satıra bir paket özelliği yazın")
    is_highlighted = models.BooleanField(default=False)
    ask_details_on_order = models.BooleanField(
        default=False,
        help_text='Açıksa, sipariş formunda "Detayları belirtin" alanı görünür.',
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.product.name} - {self.name}"

    def get_features_list(self) -> list[str]:
        return [item.strip() for item in self.features.split("\n") if item.strip()]


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    full_name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    comment = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.product.name} - {self.full_name}"


class ProductFAQ(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.product.name} - {self.question[:60]}"


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    package = models.ForeignKey(
        ProductPackage,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    detail_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.product.name} sipariş - {self.full_name}"


class ProjectRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ("portal", "Müşteri portalı"),
        ("web", "Kurumsal web platformu"),
        ("automation", "Operasyon otomasyonu"),
        ("integration", "Entegrasyon ve API"),
        ("mobile", "Mobil ve saha uygulaması"),
        ("consulting", "Danışmanlık ve analiz"),
    ]
    BUDGET_CHOICES = [
        ("not_sure", "Henüz net değil"),
        ("lt_50", "50.000 TL altı"),
        ("50_150", "50.000 - 150.000 TL"),
        ("150_500", "150.000 - 500.000 TL"),
        ("500_plus", "500.000 TL+"),
    ]
    TIMELINE_CHOICES = [
        ("urgent", "0-2 hafta"),
        ("month", "2-4 hafta"),
        ("quarter", "1-3 ay"),
        ("long_term", "3 ay+"),
    ]
    STATUS_CHOICES = [
        ("new", "Yeni"),
        ("reviewing", "İnceleniyor"),
        ("planned", "Planlandı"),
        ("closed", "Kapatıldı"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="project_requests",
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    company_name = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPE_CHOICES)
    budget_range = models.CharField(max_length=30, choices=BUDGET_CHOICES, blank=True)
    timeline = models.CharField(max_length=30, choices=TIMELINE_CHOICES, blank=True)
    project_scope = models.TextField()
    systems_note = models.TextField(blank=True)
    wants_portal_access = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} - {self.get_request_type_display()}"
