from django.http import JsonResponse

def home(request):
    data ={
        "message":"Hello my name is vihsal",
        "status": True
    }
    return JsonResponse(data)
