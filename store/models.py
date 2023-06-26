from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class TicketType(models.Model):
    """
    TicketType Table will provide a list of the different types
    of Tickets that are for sale.
    """

    name = models.CharField(verbose_name=_("Ticket Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Ticket Type")
        verbose_name_plural = _("Ticket Types")

    def __str__(self):
        return self.name


class TicketSpecification(models.Model):
    """
    The Ticket Specification Table contains Ticket
    specifiction or features for the Ticket types.
    """

    ticket_type = models.ForeignKey(TicketType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Ticket Specification")
        verbose_name_plural = _("Ticket Specifications")

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """
    The Ticket table contining all Ticket items.
    """

    ticket_type = models.ForeignKey(TicketType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 9999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999.99."),
            },
        },
        max_digits=6,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 9999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999.99."),
            },
        },
        max_digits=6,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name=_("Ticket visibility"),
        help_text=_("Change ticket visibility"),
        default=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def get_absolute_url(self):
        return reverse("store:ticket_detail", args=[self.slug])

    def __str__(self):
        return self.title


class TicketSpecificationValue(models.Model):
    """
    The Ticket Specification Value table holds each of the
    tickets individual specification or bespoke features.
    """

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    specification = models.ForeignKey(TicketSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Ticket specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Ticket Specification Value")
        verbose_name_plural = _("Ticket Specification Values")

    def __str__(self):
        return self.value


class TicketImage(models.Model):
    """
    The Ticket Image table.
    """

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="ticket_image")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a ticket image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Ticket Image")
        verbose_name_plural = _("Ticket Images")
