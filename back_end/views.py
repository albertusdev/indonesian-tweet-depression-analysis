import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from back_end.apps import App


@require_http_methods(['POST', 'OPTIONS'])
def get_depression_prediction(request):
    if request.method == "OPTIONS" or request.method == "":
        allowed_methods = ['post', 'options']
        response = HttpResponse()
        response['allow'] = ','.join(allowed_methods)
        return response

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


def retrain(request):
    App.start()
    return JsonResponse({"message": "Finish retraining"})
