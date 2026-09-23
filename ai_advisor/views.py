import os
from dotenv import load_dotenv
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cohere
from properties.models import Property
from .models import InvestmentReport
from django.utils import timezone

load_dotenv()

class GenerateAIReportView(APIView):
    def post(self, request, property_id):
        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

        api_key = os.getenv('COHERE_API_KEY', 'lCDWiOzxiB33hKB21T9mACYuoshqov1zGZfT9qnR')

        if not api_key:
            return Response({
                'error': 'Cohere API key is missing.'
            }, status=status.HTTP_400_BAD_REQUEST)

        co = cohere.ClientV2(api_key=api_key)

        rooms_val = getattr(property_obj, 'bedrooms', getattr(property_obj, 'rooms', 'N/A'))
        crime_val = getattr(property_obj, 'crime_rate', getattr(property_obj, 'crim', 'N/A'))

        prompt_text = f"""
        You are a top-tier Real Estate Investment Consultant. Analyze the following property and generate a concise report:
        - Title: {property_obj.title}
        - Type: {property_obj.property_type}
        - City: {property_obj.city}
        - Asking Price: ${property_obj.asking_price}
        - Rooms: {rooms_val}
        - Crime Rate Score: {crime_val}

        Please provide:
        1. Risk Assessment (Low Risk, Moderate, or High Risk with a short reason).
        2. Market Analysis Summary (2-3 sentences).
        3. Top 2 Negotiation Strategies for the buyer.
        """

        try:
            response = co.chat(
                model="command-r-08-2024",
                messages=[
                    {"role": "system", "content": "You are a professional Real Estate Investment Advisor."},
                    {"role": "user", "content": prompt_text}
                ]
            )

            ai_text = response.message.content[0].text

            report = InvestmentReport.objects.create(
                property=property_obj,
                risk_score='Automated Risk Calculated',
                ai_market_summery=ai_text,
                negotiation_tips='Included in Report',
                created_at=timezone.now()
            )

            return Response({
                'success': True,
                'property_id': property_id,
                'ai_report': ai_text,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Cohere API Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required(login_url='login-ui')
def ai_report_ui_view(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        view = GenerateAIReportView.as_view()
        response = view(request, property_id=property_id)

        if response.status_code in [200, 201]:
            messages.success(request, "AI Report generated successfully!")
        else:
            err_msg = response.data.get('error', 'There was an issue generating the report.')
            messages.error(request, f"Error: {err_msg}")

    report = InvestmentReport.objects.filter(property=property_obj).last()

    return render(request, 'ai_advisor/ai_report.html', {
        'property': property_obj,
        'report': report
    })