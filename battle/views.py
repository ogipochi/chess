from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'battle/index.html', {})
@csrf_exempt
def waiting(request):
    username = request.POST["user-name"]
    context = {
        "username":username
    }
    return render(request,'battle/waiting.html',context)

def room(request, room_name):
    context = {
        'room_name_json': mark_safe(json.dumps(room_name))
    }
    return render(request, 'battle/room.html', context)



            
