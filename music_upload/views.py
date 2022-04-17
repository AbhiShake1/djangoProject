import os.path

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from music_upload.models import Music


@csrf_exempt
def upload_music(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES['music']:
        import json
        post_data = request.POST
        title = post_data['title']
        artist = post_data['artist']
        file = request.FILES['music']
        try:
            music = Music.objects.create(title=title, artist=artist, file=file)
        except:
            return HttpResponse('This song already exists', status=403)
        return HttpResponse(json.dumps({
            'title': music.title,
            'artist': music.artist,
            'url': music.file.url,
        }))
    return HttpResponse(status=401)


@csrf_exempt
def get_music(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        import json
        requested_music = json.loads(request.body.decode())['title']
        try:
            music = Music.objects.get(title=requested_music)
        except MultipleObjectsReturned:
            music = Music.objects.get(title=requested_music)[0]
        except:
            return HttpResponse('The requested music does not exist', status=404)
        filename = music.file.url.split('/')[-1]
        response = HttpResponse(music.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
    return HttpResponse(status=401)


@csrf_exempt
def get_all_music(request):
    result = []
    music = Music.objects.all()
    for m in music:
        result.append({
            'title': m.title,
            'artist': m.artist,
            'filename': m.file.name
        })
    import json
    return HttpResponse(json.dumps(result))


@csrf_exempt
def delete_music(request: HttpRequest) -> HttpResponse:
    if request.method == 'DELETE':
        import json
        post_data: dict = json.loads(request.body.decode())
        file_name = os.path.join(settings.MUSIC_ROOT, post_data['title'])
        if os.path.exists(file_name):
            os.remove(file_name)
        Music.objects.get(title=post_data['title']).delete()
        files = os.listdir(settings.MUSIC_ROOT)
        return HttpResponse(json.dumps(files))
    return HttpResponse(status=401)
