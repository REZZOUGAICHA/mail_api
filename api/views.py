# gmailapp/views.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SendEmailSerializer
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import os

@method_decorator(csrf_exempt, name='dispatch')
class SendEmailView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = 'Successful Payment'
            from_email = settings.FROM_EMAIL  #change it apres to ane 

            # just fro test :') 
            confirmation_data = {
    'order_number': 'ORD123456',
    'amount': 1200,
    'currency': 'DZ',
    'auth_code': 'AUTH987654',
    'cardholder_name': 'Aisha',
    'order_status': 'Completed',
    'error_code': '00',
    'error_message': 'Transaction Successful',
    'action_code': '00',
    'action_code_description': 'Approved',
    'expiration': '12/2025',
    'deposit_amount': 1200,
    'ip': '192.168.1.1',
    'pan': '**** **** **** 1234',
    'date': '2024-08-16 12:34:56',
    'order_id': 'TXN789123',
}


            #when satim api works , uncomment this line
            
            #confirmation_data = request.data.get('confirmation_data', {})
            print("Confirmation Data:", confirmation_data)
            
            # Render the HTML content
            html_content = render_to_string('template.html', confirmation_data)
            
            # Call JsonToPdfView to generate PDF
            pdfgen_url = settings.PDFGEN_API_URL
            
            # Call JsonToPdfView to generate PDF
            pdf_response = requests.post(
                pdfgen_url,  
                json={'data': confirmation_data}
            )
            
            if pdf_response.status_code == 200:
                pdf_path = pdf_response.json().get('pdf_path')
                
                msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
                msg.attach_alternative(html_content, "text/html")
                msg.attach_file(pdf_path)
                msg.send()
                
                # Clean up the generated PDF
                os.remove(pdf_path)
                
                return Response({'status': 'email sent!'})
            else:
                return Response({'error': 'Failed to generate PDF'}, status=pdf_response.status_code)
        
        return Response(serializer.errors, status=400)
