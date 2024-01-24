from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from modules.frontend.admindashboard import views

app_name = 'admindashboard'

urlpatterns = [
    path('',views.Admin.as_view(), name='adminhome'),

    path('department_list/',
        views.DepartmentListTemplateView.as_view(),
        name='department_list'),
    path('department_detail/<slug:slug>',
        views.DepartmentDetailsTemplateView.as_view(),
        name='department_detail'),
    path('department_create/',
        views.DepartmentCreateTemplateView.as_view(),
        name='department_create'),
    path('department_update/<slug:slug>',
        views.DepartmentUpdateTemplateView.as_view(),
        name='department_update'),
    path('department_delete/<slug:slug>',
        views.DepartmentDeleteTemplateView.as_view(),
        name='department_delete'),

    path('job_list/',
        views.JobListTemplateView.as_view(),
        name='job_list'),
    path('job_detail/<slug:slug>',
        views.JobDetailsTemplateView.as_view(),
        name='job_detail'),
    path('job_update/<slug:slug>',
        views.JobUpdateTemplateView.as_view(),
        name='job_update'),
    path('job_delete/<slug:slug>',
        views.JobDeleteTemplateView.as_view(),
        name='job_delete'),

    path('interview_pending_list/<slug:slug>',
        views.InterviewPendingListTemplateView.as_view(),
        name='interview_pending_list'),
    path('interview_completed_list/<slug:slug>',
        views.InterviewCompletedListTemplateView.as_view(),
        name='interview_completed_list'),

    path('selected_user_list/<slug:slug>',
        views.SelectedUserListTemplateView.as_view(),
        name='selected_user_list'),
    path('selected_user_details/<slug:slug>',
        views.SelectedUserDetailsTemplateView.as_view(),
        name='selected_user_details'),

    path('ventures_list/',views.VenturesListView.as_view(), name='ventures'),
    path('ventures_detail/<slug:slug>/',views.VenturesDetailView.as_view(), name='ventures_detail'),
    path('ventures_delete/<slug:slug>/',views.VenturesDeleteView.as_view(), name='ventures_delete'),
    path('job_create/',views.JobCreateView.as_view(), name='job_create'),
    path('apply_job_create/',views.ApplyJobCreateView.as_view(), name='apply_job_create'),
    path('apply_job_list/',views.ApplyJobListView.as_view(), name='apply_job_list'),
    path('apply_job_detail/<slug:slug>/',views.ApplyJobDetailView.as_view(), name='apply_job_detail'),
    path('shortlisted_user/<slug:slug>/',views.ShortListView.as_view(), name='shortlist_user'),
    path('shortlisted_user_list/<slug:slug>/',views.ShortListCandidateListView.as_view(), name='shortlisted_user_list'),
    path('shortlisted_user_detail/<slug:slug>/',views.ShortListDetailView.as_view(), name='shortlisted_user_detail'),
    path('zoom_link_create/', views.ZoomLinkCreateAPIView.as_view(), name='zoom_link_create'),
    path('zoom_meet_update/<slug:slug>/', views.ZoomMeetingUpdateView.as_view(), name='zoom_meet_update'),
    path('zoom_link_update/<slug:slug>/', views.ZoomStatusUpdateView.as_view(), name='zoom_link_update'),
    path('zoom_link_list/', views.ZoomLinkListView.as_view(), name='zoom_link_list'),


    path('update_interview_status/<slug:slug>',
        views.UpdateInterviewStatusTemplateView.as_view(),
        name='update_interview_status'),
    path('select_user/<slug:slug>',
        views.SelectUserTemplateView.as_view(),
        name='select_user'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
