from django.shortcuts import render
from .models import Story


def default(request):
    story = Story.objects.filter(published_at__isnull=False).order_by('-published_at').first()
    return render(request, template_name="index.html", context={'story': story})
