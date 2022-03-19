import os.path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, HttpRequest
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload_music(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES['music']:
        upload: InMemoryUploadedFile = request.FILES['music']
        fss = FileSystemStorage()
        file = fss.save(os.path.join(settings.MUSIC_ROOT, upload.name), upload)
        return HttpResponse(fss.url(file))
    return HttpResponse(status=401)


@csrf_exempt
def get_music(request: HttpRequest) -> HttpResponse:
    files = os.listdir(settings.MUSIC_ROOT)
    import json
    return HttpResponse(json.dumps(files))


@csrf_exempt
def delete_music(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        import json
        post_data: dict = json.loads(request.body.decode())
        file_name = os.path.join(settings.MUSIC_ROOT, post_data['file_name'])
        if os.path.exists(file_name):
            os.remove(file_name)
        files = os.listdir(settings.MUSIC_ROOT)
        return HttpResponse(json.dumps(files))
    return HttpResponse(status=401)
