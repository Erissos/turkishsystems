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

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SocialLink(models.Model):
    label = models.CharField(max_length=120)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.label


class PricingPackage(models.Model):
    name = models.CharField(max_length=120)  # e.g. Start, Scale, Enterprise
    price = models.CharField(max_length=80)  # e.g. ₺9.900/ay, Özel teklif
    description = models.TextField()
    features = models.TextField(help_text="Her satıra bir özellik yazın")
    is_highlighted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.name

    def get_features_list(self) -> list[str]:
        return [f.strip() for f in self.features.split("\n") if f.strip()]
