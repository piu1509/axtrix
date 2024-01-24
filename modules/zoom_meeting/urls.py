from django.urls import path
from .views import ZoomLinkCreateAPIView, ZoomLinkListAPIView, ZoomLinkRetrieveApi, ZoomMeetingUpdateApi, ZoomLinkUpdateApi, ZoomLinkDestroyApi, ZoomCompletedAPIView, ZoomListAPIView
from .views import OfferLetterAPIView, ConvertPdfAPIView

app_name = 'zoom_meeting'

urlpatterns = [
    path('zoom_link_create/', ZoomLinkCreateAPIView.as_view(), name='zoom_link_create'),
    path('zoom_meet_update/<slug:slug>/', ZoomMeetingUpdateApi.as_view(), name='zoom_meet_update'),
    path('zoom_link_update/<slug:slug>/', ZoomLinkUpdateApi.as_view(), name='zoom_link_update'),
    path('zoom_link_list/', ZoomLinkListAPIView.as_view(), name='zoom_link_list'),
    path('zoom_link_retrieve/<slug:slug>/', ZoomLinkRetrieveApi.as_view(), name='zoom_link_retrieve'),
    path('zoom_link_delete/<slug:slug>/', ZoomLinkDestroyApi.as_view(), name='zoom_link_delete'),
    path('offer_letter/<slug:slug>/', OfferLetterAPIView.as_view(), name='offer_letter'),
    path('convert_pdf/', ConvertPdfAPIView.as_view(), name='convert_pdf'),
    path('zoom_list/<slug:slug>/', ZoomListAPIView.as_view(), name='zoom_list'),
    path('zoom_completed_list/<slug:slug>/', ZoomCompletedAPIView.as_view(), name='zoom_completed_list'),
]
