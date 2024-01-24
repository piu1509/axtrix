from rest_framework import serializers
from modules.zoom_meeting.models import ZoomMeeting


class ZoomMeetingSerializer(serializers.ModelSerializer):
    """
    Serializer for ZoomMeeting model.
    """
    class Meta:
        model = ZoomMeeting
        fields = ['meeting_title', 'meeting_description', 'meeting_date', 'meeting_time', 'meeting_duration', 'email', 'status', 'job', 'zoom_meeting_link', 'zoom_meeting_password']
        read_only_fields = [ 'zoom_meeting_link', 'zoom_meeting_password']


class ZoomMeetingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for ZoomMeetingUpdate model.
    """
    class Meta:
        model = ZoomMeeting
        fields = ['meeting_title', 'meeting_description', 'meeting_date', 'meeting_time', 'meeting_duration', 'email', 'status', 'job', 'zoom_meeting_link', 'zoom_meeting_password']
        read_only_fields = [ 'meeting_title', 'meeting_description', 'meeting_date', 'meeting_time', 'meeting_duration', 'email', 'job', 'zoom_meeting_link', 'zoom_meeting_password']
