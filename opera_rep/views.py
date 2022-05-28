from django.shortcuts import render


# handel 404 pages (template in templates/err)
def handler404(request, exception):
    return render(request, 'err/404.html', status=404)


# handel 500 pages (template in templates/err)
def handler500(request):
    return render(request, 'err/500.html', status=500)
