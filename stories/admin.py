from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Story, Writer


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ["name", "story_count", "id"]
    search_fields = ["name"]
    ordering = ["name"]

    def story_count(self, obj):
        """Display the number of stories for this writer."""
        count = obj.stories.count()
        url = reverse("admin:stories_story_changelist") + f"?writer__id__exact={obj.id}"
        return format_html('<a href="{}">{} stories</a>', url, count)

    story_count.short_description = "Stories"


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "writer",
        "excerpt_preview",
        "is_published",
        "published_at",
        "created_at",
    ]
    list_filter = [
        "created_at",
        "published_at",
        "writer",
    ]
    search_fields = ["title", "content", "excerpt", "writer__name"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "slug_preview"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("title", "slug", "slug_preview", "writer")}),
        ("Content", {"fields": ("excerpt", "content")}),
        (
            "Publishing",
            {
                "fields": ("published_at",),
                "description": "Set published_at to publish this story",
            },
        ),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    actions = ["publish_stories", "unpublish_stories"]

    def excerpt_preview(self, obj):
        """Show a short preview of the excerpt."""
        if obj.excerpt:
            return obj.excerpt[:50] + "..." if len(obj.excerpt) > 50 else obj.excerpt
        return "-"

    excerpt_preview.short_description = "Excerpt"

    def is_published(self, obj):
        """Show if story is published with a colored indicator."""
        if obj.published_at and obj.published_at <= timezone.now():
            return format_html('<span style="color: green;">●</span> Published')
        return format_html('<span style="color: gray;">○</span> Draft')

    is_published.short_description = "Status"

    def slug_preview(self, obj):
        """Show the slug as a readonly field."""
        if obj.slug:
            return obj.slug
        return "-"

    slug_preview.short_description = "Current Slug"

    def publish_stories(self, request, queryset):
        """Bulk action to publish selected stories."""
        updated = queryset.filter(published_at__isnull=True).update(
            published_at=timezone.now()
        )
        self.message_user(request, f"{updated} story(ies) were successfully published.")

    publish_stories.short_description = "Publish selected stories"

    def unpublish_stories(self, request, queryset):
        """Bulk action to unpublish selected stories."""
        updated = queryset.update(published_at=None)
        self.message_user(
            request, f"{updated} story(ies) were successfully unpublished."
        )

    unpublish_stories.short_description = "Unpublish selected stories"

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related("writer")


# Alternative: If you want a simpler admin configuration
#
# @admin.register(Writer)
# class WriterAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']
#
#
# @admin.register(Story)
# class StoryAdmin(admin.ModelAdmin):
#     list_display = ['title', 'writer', 'created_at', 'published_at']
#     list_filter = ['created_at', 'published_at', 'writer']
#     search_fields = ['title', 'content']
#     prepopulated_fields = {'slug': ('title',)}
#     date_hierarchy = 'created_at'
