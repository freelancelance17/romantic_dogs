from django.db import models
from django.utils.text import slugify


class Story(models.Model):
    # Basic story information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    writer = models.ForeignKey(
        "stories.Writer", on_delete=models.CASCADE, related_name="stories"
    )

    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, help_text="Excerpt")
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Stories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    #
    # def get_absolute_url(self):
    #     from django.urls import reverse
    #
    #     return reverse("story_detail", kwargs={"slug": self.slug})


class Writer(models.Model):

    name = models.CharField(blank=False, null=False, max_length=30)
