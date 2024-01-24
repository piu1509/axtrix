from django.urls import path
from modules.department.views import (
    DepartmentCreateApi, DepartmentListApi,
    DepartmentRetrieveApi, DepartmentUpdateApi,
    DepartmentDestroyApi, CreateJobApi,
    JobListApi, JobDetailApi,
    UpdateJobApi, DeleteJobApi,
    CreateAppliedJobApi, AppliedJobDetailApi,
    AppliedJobListApi, ShortlistOrDisallowCandidate,
    ShortlistedCandidateList, RetrieveShortlistedCandidate,
    AppliedJobListInterviewPending, AppliedJobListInterviewCompleted, UpdateInterviewStatus,
    SelectUserJobListApi, DetailSelectUser, SelectUser
    )

app_name = 'department'

urlpatterns = [
    # End points for CRUD operations of Department model.
    path('department_create/', DepartmentCreateApi.as_view(), name='department_create'),
    path('department_list/', DepartmentListApi.as_view(), name='department_list'),
    path('department_retrieve/<slug:slug>/', DepartmentRetrieveApi.as_view(), name='department_retrieve'),
    path('department_update/<slug:slug>/', DepartmentUpdateApi.as_view(), name='department_update'),
    path('department_delete/<slug:slug>/', DepartmentDestroyApi.as_view(), name='department_delete'),

    # End points for CRUD operations of Job model.
    path('create_job/',
        CreateJobApi.as_view(),
        name='create_job'),
    path('job_list/',
        JobListApi.as_view(),
        name='job_list'),
    path('job_detail/<slug:slug>',
        JobDetailApi.as_view(),
        name='job_detail'),
    path('update_job/<slug:slug>',
        UpdateJobApi.as_view(),
        name='update_job'),
    path('delete_job/<slug:slug>',
        DeleteJobApi.as_view(),
        name='delete_job'),

    # End points for CRUD operations of Applied Job model.
    path('create_applied_job/',
        CreateAppliedJobApi.as_view(),
        name='create_applied_job'),
    path('applied_job_detail/<slug:slug>',
        AppliedJobDetailApi.as_view(),
        name='applied_job_detail'),
    path('applied_job_list/',
        AppliedJobListApi.as_view(),
        name='applied_job_list'),

    # End point for shortlisting a candidate for interview.
    path('shortlist_candidate/<slug:slug>',
        ShortlistOrDisallowCandidate.as_view(),
        name='shortlist'),
    path('shortlisted_candidate_list/<slug:slug>',
        ShortlistedCandidateList.as_view(),
        name='shortlisted_candidate_list'),
    path('shortlisted_candidate_detail/<slug:slug>',
        RetrieveShortlistedCandidate.as_view(),
        name='shortlisted_candidate_detail'),

    path('applied_jobs_interview_pending/<slug:slug>',
        AppliedJobListInterviewPending.as_view(),
        name='applied_jobs_interview_pending'),
    path('applied_jobs_interview_completed/<slug:slug>',
        AppliedJobListInterviewCompleted.as_view(),
        name='applied_jobs_interview_completed'),
    path('interview_status/<slug:slug>/',
        UpdateInterviewStatus.as_view(),
        name='interview_status'),

    path('select_user_list/<slug:slug>/',
        SelectUserJobListApi.as_view(),
        name='select_user_list'),
    path('select_user_detail/<slug:slug>/',
        DetailSelectUser.as_view(),
        name='select_user_detail'),
    path('select_user/<slug:slug>/',
        SelectUser.as_view(),
        name='select_user'),
]
