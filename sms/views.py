from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from django.shortcuts import render
import json

@csrf_exempt
def send_sms(request):
    if request.method == 'POST':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            message_body = data.get('message')

            print(phone_number,settings.TWILIO_PHONE_NUMBER)
            if not phone_number or not message_body:
                return JsonResponse({'status': 'error', 'message': 'Phone number and message are required'}, status=400)

            # Initialize Twilio client
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)

            # Send SMS
            message = client.messages.create(
                body=message_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            # Respond with success
            return JsonResponse({'status': 'success', 'message_sid': message.sid})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def home(request):
    context = {}
    return render(request, 'main.html', context=context)
