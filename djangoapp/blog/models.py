from django.db import models
from utils.rands import slugify_new
from django.contrib.auth.models import User
from utils.images import resize_image
from django_summernote.models import AbstractAttachment
from django.urls import reverse
# Create your models here.


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )  # tipo id da tag

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )  # tipo id da tag

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class PostManager(models.Manager):
    # self is objects! like a Post method that already do this filtering (check views!)
    def get_published(self):
        return self.filter(is_published=True).order_by('-id')


class Page(models.Model):

    objects = PostManager()
    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True,
        default="",
        null=False,
        blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title)

        return super().save(*args, **kwargs)

    is_published = models.BooleanField(default=False,
                                       help_text='This field needs to be on to exhibit this page!')
    content = models.TextField()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        if not self.is_published:
            return reverse("blog:index")

        return reverse("blog:page", args=(self.slug,))


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True,
        default="",
        null=False,
        blank=True,
        max_length=255,
    )
    excert = models.CharField(max_length=150,)
    # author = User
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False,
                                       help_text='This field needs to be on to exhibit this post!')

    cover = models.ImageField(upload_to='posts/%Y/%m',
                              blank=True,
                              default='',
                              )

    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Show image also inside post content'
    )
    # muitos posts numa categoria!! cat pai, post filho
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, default=None,)
    tags = models.ManyToManyField(Tag, blank=True, default='')

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        # para relacao invertida/inversa - user.post_set.all() -> user.post_create_by.QUERYSET!
        related_name='post_created_by'
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title)

        current_cover_name = str(self.cover.name)
        # senao tiver ele nao guard pq é sobreescrito o metodo
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            # true - optimize, 70 - percentage
            resize_image(self.cover, 900, True, 70)
        return super_save

    def __str__(self) -> str:
        return self.title

    # change in admin - button to see in site
    # desta forma posso usar nos proprios templates para ir buscar o post em vez
    # de fazer blog:post post.slug -> post.get_absolute_url
    def get_absolute_url(self):
        if not self.is_published:
            return reverse("blog:index")

        return reverse("blog:post", args=(self.slug,))


class PostAttachment(AbstractAttachment):  # override da classe
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save
