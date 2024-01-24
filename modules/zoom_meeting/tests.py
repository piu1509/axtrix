import requests
import json
import base64

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ZoomMeeting


# Model Test Cases

class ZoomMeetingModelTest(TestCase):
    """
    Test Cases for the ZoomMeeting model.
    """
    def create_meeting(self):
        zoom_meeting = ZoomMeeting.objects.create(
            meeting_title="Testing Meeting",
            meeting_description="This is a test meeting 2.",
            meeting_date="2023-05-02",
            meeting_time="13:00:00",
            meeting_duration="1 hour",
            email="test2@example.com",
            status="Pending",
            job="45bb630b-d024-4810-b6f4-46845965a350",
        )
        return zoom_meeting

    def test_create_meeting(self):
        """
        Test Case for creating of ZoomMeeting object.
        """
        meet = self.create_meeting()
        self.assertTrue(isinstance(meet, ZoomMeeting))
    
    def test_unique_slug(self):
        """
        Test Case for unique_slug.
        """
        zoom_meeting1 = ZoomMeeting.objects.create(
            meeting_title='Test Meeting 1',
            meeting_date='2023-05-01',
            meeting_time='12:00:00',
        )
        zoom_meeting2 = ZoomMeeting.objects.create(
            meeting_title='Test Meeting 2',
            meeting_date='2023-05-01',
            meeting_time='13:00:00',
        )
        self.assertNotEqual(zoom_meeting1.slug, zoom_meeting2.slug)
    
    def test_delete_zoom_meeting(self):
        """
        Test Case for deletion of ZoomMeeting object.
        """
        zoom_meeting = ZoomMeeting.objects.create(
            meeting_title='Test Meeting',
            meeting_date='2023-05-01',
            meeting_time='12:00:00',
        )
        zoom_meeting.delete()
        with self.assertRaises(ZoomMeeting.DoesNotExist):
            ZoomMeeting.objects.get(id=zoom_meeting.id)


# APIViews Test Cases

class ZoomMeetingApiTest(APITestCase):
    """
    Test cases for ZoomMeetingApiViews
    """
    def setUp(self):
        """
        setUp Function for user creation and authentication.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.zoom_meeting = ZoomMeeting.objects.create(
            meeting_title="Test Meeting",
            meeting_description="This is a test meeting.",
            meeting_date="2023-05-01",
            meeting_time="14:00:00",
            meeting_duration="1 hour",
            email="test@example.com",
            status="Pending",
            job="45bb630b-d024-4810-b6f4-46845965a350",
        )
        self.zoom_meeting_create_url = reverse(
            "zoom_meeting:zoom_link_create"
        )
        self.zoom_meeting_list_url = reverse(
            "zoom_meeting:zoom_link_list"
        )
        self.zoom_meeting_retrieve_url = reverse(
            "zoom_meeting:zoom_link_retrieve", kwargs={"slug": self.zoom_meeting.slug}
        )
        self.zoom_meeting_update_url = reverse(
            "zoom_meeting:zoom_meet_update", kwargs={"slug": self.zoom_meeting.slug}
        )
        self.zoom_meeting_delete_url = reverse(
            "zoom_meeting:zoom_link_delete", kwargs={"slug": self.zoom_meeting.slug}
        )
        
        self.client.force_authenticate(user=self.user)

    def test_create_zoom_meeting(self):
        """
        Test case for ZoomLinkCreateApiView
        """
        data = {
            "meeting_title": "Test Meeting 1",
            "meeting_description": "This is a test meeting.",
            "meeting_date": "2023-05-01",
            "meeting_time": "12:00:00",
            "meeting_duration": "30 minutes",
            "email": "test@example.com",
            "status": "Pending",
            "job": "45bb630b-d024-4810-b6f4-46845965a349",
        }
        response = self.client.post(self.zoom_meeting_create_url, data, format='json' )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['data']['zoom_meeting_link'])
        self.assertIsNotNone(response.data['data']['zoom_meeting_password'])
        self.assertEqual(response.data["message"], "Zoom Link Sent")

    def test_list_zoom_meeting(self):
        """
        Test case for ZoomLinkListApiView
        """
        self.zoom_meeting = ZoomMeeting.objects.create(
            meeting_title="Test Meeting 2",
            meeting_description="This is a 2nd test meeting.",
            meeting_date="2023-05-01",
            meeting_time="14:00:00",
            meeting_duration="1 hour",
            email="test@example.com",
            status="Pending",
            job="45bb630b-d024-4810-b6f4-46845965a350",
        )
        response = self.client.get(self.zoom_meeting_list_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Data list retrieved successfully")

    def test_retrieve_zoom_meeting(self):
        """
        Test case for ZoomLinkListApiView
        """
        response = self.client.get(self.zoom_meeting_retrieve_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Data retrieved successfully")
        self.assertEqual(response.data['data']['meeting_title'], 'Test Meeting')
    
    def test_update_zoom_meeting(self):
        """
        Test case for ZoomLinkUpdateApiView
        """
        data = {
            "meeting_title": "Updated Meeting",
            "meeting_description": "This is an updated meeting.",
            "meeting_date": "2023-05-01",
            "meeting_time": "12:00:00",
            "meeting_duration": "30 minutes",
            "email": "test@example.com",
            "status": "Pending",
            "job": "45bb630b-d024-4810-b6f4-46845965a349",
        }
        response = self.client.put(self.zoom_meeting_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "Updated Zoom Meeting successfully")
        self.assertEqual(response.data["data"]["meeting_title"], "Updated Meeting")

    def test_delete_zoom_meeting(self):
        """
        Test case for ZoomLinkDestroyApiView
        """
        response = self.client.delete(self.zoom_meeting_delete_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            ZoomMeeting.objects.filter(slug=self.zoom_meeting.slug).exists()
        )
