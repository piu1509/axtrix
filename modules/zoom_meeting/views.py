import weasyprint

from django.http import Http404, HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datetime import datetime
from zoomus import ZoomClient

from weasyprint import HTML, CSS

from modules.zoom_meeting.serializers import ZoomMeetingSerializer, ZoomMeetingUpdateSerializer
from modules.zoom_meeting.models import ZoomMeeting
from modules.department.models import AppliedJob


class ZoomLinkCreateAPIView(generics.CreateAPIView):
    """
	HRs can send zoom link via mail to a candidate.
	"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ZoomMeetingSerializer

    def post(self, request):
        serializer = ZoomMeetingSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            client = ZoomClient(settings.ZOOM_API_KEY, settings.ZOOM_API_SECRET)
            start_time = datetime.combine(data['meeting_date'], data['meeting_time'])
            response = client.meeting.create(user_id='me', topic=data['meeting_title'], start_time=start_time)
            meeting_info = response.json()
            join_url = meeting_info.get('join_url')
            password = meeting_info.get('password')
            subject = 'Interview Round'
            message = f'Here is the link to your Zoom meeting: {join_url}\n\nTopic: {data["meeting_title"]}\nDescription: {data["meeting_description"]}\nDate: {start_time.strftime("%m/%d/%Y")}\nTime: {start_time.strftime("%I:%M %p")}\nDuration: {data["meeting_duration"]} \n\n Hiring Team '
            recipient_list = [data['email']]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            serializer.validated_data['zoom_meeting_link'] = join_url
            serializer.validated_data['zoom_meeting_password'] = password
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Zoom Link Sent",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZoomMeetingUpdateApi(generics.UpdateAPIView):
    """
    API view for updating ZoomLink instances.
    """
    serializer_class = ZoomMeetingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_object(self, slug):
        try:
            return ZoomMeeting.objects.get(slug=slug)
        except ZoomMeeting.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        Department = self.get_object(slug)
        serializer = ZoomMeetingSerializer(Department)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        instance = self.get_object(slug)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.validated_data
            client = ZoomClient(settings.ZOOM_API_KEY, settings.ZOOM_API_SECRET)
            start_time = datetime.combine(data['meeting_date'], data['meeting_time'])
            response = client.meeting.create(user_id='me', topic=data['meeting_title'], start_time=start_time)
            meeting_info = response.json()
            join_url = meeting_info.get('join_url')
            password = meeting_info.get('password')
            subject = 'Interview Round'
            message = f'Here is the link to your Zoom meeting: {join_url}\n\nTopic: {data["meeting_title"]}\nDescription: {data["meeting_description"]}\nDate: {start_time.strftime("%m/%d/%Y")}\nTime: {start_time.strftime("%I:%M %p")}\nDuration: {data["meeting_duration"]} \n\n Hiring Team '
            recipient_list = [data['email']]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            serializer.validated_data['zoom_meeting_link'] = join_url
            serializer.validated_data['zoom_meeting_password'] = password
            return Response(
                {
                    "success": True,
                    "message": "Updated Zoom Meeting successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZoomLinkUpdateApi(generics.UpdateAPIView):
    """
    API view for updating ZoomLink Interview status instances.
    """
    serializer_class = ZoomMeetingUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_object(self, slug):
        try:
            return ZoomMeeting.objects.get(slug=slug)
        except ZoomMeeting.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        Department = self.get_object(slug)
        serializer = ZoomMeetingUpdateSerializer(Department)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        instance = self.get_object(slug)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Data updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZoomLinkListAPIView(generics.ListAPIView):
    """
    API view for listing ZoomMeeting instances.
    """
    serializer_class = ZoomMeetingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = ZoomMeeting.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Data list retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ZoomLinkRetrieveApi(generics.RetrieveAPIView):
    """
    API view for retrieving ZoomMeeting instances.
    """
    serializer_class = ZoomMeetingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_object(self, slug):
        try:
            return ZoomMeeting.objects.get(slug=slug)
        except ZoomMeeting.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        Department = self.get_object(slug)
        serializer = ZoomMeetingSerializer(Department)
        return Response(
            {
                "success": True,
                "message": "Data retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )



class ZoomLinkDestroyApi(generics.DestroyAPIView):
    """
    API view for deleting ZoomLink instances.
    """
    serializer_class = ZoomMeetingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def delete(self, request, slug):
        instance = ZoomMeeting.objects.get(slug=slug)
        zoom = instance.meeting_title
        instance.delete()
        return Response(
            {
                "message": "Data deleted successfully",
                "data":zoom,
            }, 
            status=status.HTTP_204_NO_CONTENT
        )


class OfferLetterAPIView(APIView):
    """
    APIView that gives a HTML Template to create a offer letter.
    """
    def get(self, request, slug):
        selecteduser = AppliedJob.objects.get(slug=slug)
        if selecteduser.result == True :
            return render(request, 'offerLetter/offer.html', {'slug':slug})
        return Response(
            {
                "message": "Candidate's status is still pending.",
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


class ConvertPdfAPIView(APIView):
    """
    APIView to convert template to pdf and send mail with pdf(offer letter).
    """
    def post(self, request):
        if request.POST.get('convert') == 'view1':
            response = self.generate_pdf(request)
            return response

        elif request.POST.get('send_offer_letter') == 'view2':
            slug = request.POST.get('slug')
            email = request.POST.get('mail_id')

            email = EmailMessage(
                'Offer letter',
                'Hi, \n\n Hope You are doing well, \n\n Your interview feedback is quite promising. So we would like to offer you a position in our company. \n\n Please find the offer letter attached with this mail. \n\n Thank You, \n\n Hiring Team.',
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            response = self.generate_pdf(request)
            email.attach('offer_letter.pdf', response.content, 'application/pdf')
            email.send(fail_silently=False)

            return Response(
                {
                    "success": True,
                    "message": "Email with offer letter sent successfully",
                },
                status=status.HTTP_200_OK,
            )
        return HttpResponse()

    def generate_pdf(self, request):
        context = {
            'emp_name': request.POST['emp_name'],
            'date': request.POST['date'],
            'position': request.POST['position'],
            'location': request.POST['location'],
            'pre_company': request.POST['pre_company'],
            'candidate_name' : request.POST['candidate_name'],
            'today_date' : request.POST['today_date'],
        }
        html = render_to_string('offerLetter/pdf_change.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline:filename= "{}.pdf"'.format(
            "name")
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
            CSS(string='body { font-size: 13px }')])
        return response


class ZoomListAPIView(generics.ListAPIView):
    """
    List out ZoomMeetings of a particular applied job that are pending.
    """
    serializer_class = ZoomMeetingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = ZoomMeeting.objects.filter(status='Pending', job=self.kwargs['slug'])
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Data list retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ZoomCompletedAPIView(generics.ListAPIView):
    """
    List out ZoomMeetings of a particular applied job that are completed.
    """
    serializer_class = ZoomMeetingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = ZoomMeeting.objects.filter(status='Completed', job=self.kwargs['slug'])
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Data list retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
