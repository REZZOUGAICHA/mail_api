from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JsonToPdfSerializer
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
import os

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class JsonToPdfView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = JsonToPdfSerializer(data=request.data)
        if serializer.is_valid():
            json_data = serializer.validated_data['data']
            template_path = os.path.join(settings.BASE_DIR, 'api', 'templates', 'DocTemplate.pdf')

            # Create a buffer for the overlay PDF
            packet = BytesIO()
            overlay_canvas = canvas.Canvas(packet, pagesize=letter)
            # Map the JSON data to the respective places on the template
            overlay_canvas.drawString(225, 402, json_data.get('order_id', ''))
            overlay_canvas.drawString(200, 375, str(json_data.get('order_number', '')))
            overlay_canvas.drawString(200, 348, str(json_data.get('auth_code', '')))
            overlay_canvas.drawString(245, 322, json_data.get('date', ''))
            overlay_canvas.drawString(190, 295, str(json_data.get('amount', '')))
            overlay_canvas.drawString(180, 268, 'CIB')  # Dunno how to know 
            overlay_canvas.save()

            packet.seek(0)
            new_pdf = PdfReader(packet)
            overlay_page = new_pdf.pages[0]

            output = BytesIO()
            pdf_writer = PdfWriter()
            template_pdf = PdfReader(template_path)
            template_page = template_pdf.pages[0]
            template_page.merge_page(overlay_page)
            pdf_writer.add_page(template_page)
            pdf_writer.write(output)
            output.seek(0)

            # Ensure the MyPdfs directory exists
            pdf_dir = os.path.join(settings.BASE_DIR, 'api', 'MyPdfs')
            os.makedirs(pdf_dir, exist_ok=True)

            # Get the order_id and create the PDF filename
            order_id = json_data.get('order_id', 'default_order_id')
            pdf_filename = f'pay_{order_id}.pdf'

            # Save the PDF to the MyPdfs directory (dunno why it's not working X)
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            with open(pdf_path, 'wb') as f:
                f.write(output.read())

            return Response({'pdf_path': pdf_path}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
