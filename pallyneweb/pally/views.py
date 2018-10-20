from django.shortcuts import render
from django.http import HttpResponse

# Pallyne Views
def index(request):
    #videos = PallyneVideo.objects.all()[0:4]
    #context_dict = {'recentvideos': videos }
    context_dict = {}
    return render(request, 'pally/index.html', context=context_dict)
