from django.shortcuts import render
# from django.template import RequestContext

# Create your views here.
# from django.shortcuts import render, HttpResponse
# from channels.layers import get_channel_layer
# import json

# # Create your views here.
def home(request):

    # data = {
    #     'room_name': "broadcast"
    # }
    return render(request, 'index/index.html')