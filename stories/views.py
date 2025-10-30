from django.shortcuts import render


def default(request):
    return render(request, template_name="index.html", context={})
