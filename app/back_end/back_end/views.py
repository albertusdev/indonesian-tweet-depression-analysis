import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from back_end.apps import App


@require_http_methods(['POST'])
def get_depression_prediction(request):
    print(request.body)
    json_data = json.loads(request.body)
    tweet = json_data['tweet']
    result = App.classifier.predict(tweet)
    for key in result:
        if result[key]:
            result[key] = 'Terdeteksi Depresi'
        else:
            result[key] = 'Terdeteksi Normal'
    return JsonResponse(result)

