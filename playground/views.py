from django.http import HttpResponse

def playground_home(request):
    return HttpResponse('<h1>Playground Home</h1>')