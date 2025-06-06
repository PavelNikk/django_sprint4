from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    title = models.CharField(_("Заголовок"), max_length=256)
    description = models.TextField(_("Описание"))
    slug = models.SlugField(
        _("Идентификатор"),
        unique=True,
        help_text=_(
            "Идентификатор страницы для URL; разрешены символы \
латиницы, цифры, дефис и подчёркивание."
        ),
    )
    is_published = models.BooleanField(
        _("Опубликовано"),
        default=True,
        help_text=_("Снимите галочку, чтобы скрыть публикацию."),
    )
    created_at = models.DateTimeField(_("Добавлено"), auto_now_add=True)

    class Meta:
        verbose_name = _("категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(_("Название места"), max_length=256)
    is_published = models.BooleanField(
        _("Опубликовано"),
        default=True,
        help_text=_("Снимите галочку, чтобы скрыть публикацию."),
    )
    created_at = models.DateTimeField(_("Добавлено"), auto_now_add=True)

    class Meta:
        verbose_name = _("местоположение")
        verbose_name_plural = _("Местоположения")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(_("Заголовок"), max_length=256)
    text = models.TextField(_("Текст"))
    pub_date = models.DateTimeField(
        _("Дата и время публикации"),
        help_text=_(
            "Если установить дату и время в будущем — \
можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Автор публикации"),
        related_name="posts",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Местоположение"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Категория"),
    )
    is_published = models.BooleanField(
        _("Опубликовано"),
        default=True,
        help_text=_("Снимите галочку, чтобы скрыть публикацию."),
    )
    created_at = models.DateTimeField(_("Добавлено"), auto_now_add=True)
    image = models.ImageField(upload_to="posts_images/", blank=True)

    @property
    def short_text(self):
        return self.text[:100)

    class Meta:
        verbose_name = _("публикация")
        verbose_name_plural = _("Публикации")
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(
        "Текст комментария",
        max_length=500,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="comments",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.text
