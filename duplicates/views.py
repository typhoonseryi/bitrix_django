from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

@method_decorator(csrf_exempt, name='dispatch')
class FindDuplicates(View):

    def post(self, request):
        domain = request.POST.get('domain')
        auth = request.POST.get('auth')
        if domain and auth:

            method = 'crm.company.list'
            payload = {
                'auth': auth,
                'select': ['TITLE'],
            }
            url = 'https://' + domain + '/rest/' + method + '.json'

            try:
                resp_data = requests.get(url, params=payload)

                try:
                    json_data = resp_data.json()
                    companies = [ i['TITLE'] for i in json_data['result'] ]
                except (json.decoder.JSONDecodeError, KeyError):
                    response = JsonResponse({'error': 'unexpected API response'}, status=400)
                    response['Access-Control-Allow-Origin'] = 'https://typhoonseryi.000webhostapp.com'
                    response['Access-Control-Allow-Methods'] = 'POST'
                    return response

                next_count = json_data.get('next')

                while next_count:

                    payload['start'] = next_count

                    try:
                        resp_data = requests.get(url, params=payload)

                        try:
                            json_data = resp_data.json()
                            companies.extend([ i['TITLE'] for i in json_data['result'] ])
                        except (json.decoder.JSONDecodeError, KeyError):
                            response = JsonResponse({'error': 'unexpected API response'}, status=400)
                            response['Access-Control-Allow-Origin'] = 'https://typhoonseryi.000webhostapp.com'
                            response['Access-Control-Allow-Methods'] = 'POST'
                            return response

                        next_count = json_data.get('next')

                    except requests.exceptions.RequestException:
                        response = JsonResponse({'error': 'requests exceptions occured'}, status=504)
                        response['Access-Control-Allow-Origin'] = 'https://typhoonseryi.000webhostapp.com'
                        response['Access-Control-Allow-Methods'] = 'POST'
                        return response

                duplicates = [ i for i in set(companies) if companies.count(i) > 1 ]
                response = JsonResponse({'result': duplicates, 'total': len(companies)}, status=200)

            except requests.exceptions.RequestException:
                response = JsonResponse({'error': 'requests exceptions occured'}, status=504)
                response['Access-Control-Allow-Origin'] = 'https://typhoonseryi.000webhostapp.com'
                response['Access-Control-Allow-Methods'] = 'POST'
                return response

        else:
            response = JsonResponse({'error': 'not enough given parameters'}, status=400)

        response['Access-Control-Allow-Origin'] = 'https://typhoonseryi.000webhostapp.com'
        response['Access-Control-Allow-Methods'] = 'POST'
        return response