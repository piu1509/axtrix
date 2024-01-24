from django.http import Http404
from rest_framework import generics, status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
    )
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from modules.department.serializers import (
    CreateDepartmentSerializer,
    DepartmentSerializer,
    JobSerializer,
    JobListSerializer,
    CreateAppliedJobSerializer,
    AppliedJobSerializer,
    ShortlistCandidateSerializer,
    InterviewStatusSerializer,
    SelectUserSerializer
    )
from modules.department.models import (
    Department,
    Job,
    AppliedJob
    )


class DepartmentCreateApi(generics.CreateAPIView):
    """
    API view for creating department instances.
    """
    serializer_class = CreateDepartmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentListApi(generics.ListAPIView):
    """
    API view for listing department instances.
    """
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Department.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            {
                "success": True,
                "message": "Data list retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class DepartmentRetrieveApi(generics.RetrieveAPIView):
    """
    API view for retrieving department instances.
    """
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_object(self, slug):
        try:
            return Department.objects.get(slug=slug)
        except Department.DoesNotExist:
            raise Http404
    
    def get(self, request, slug, format=None):
        Department = self.get_object(slug)
        serializer = DepartmentSerializer(Department)
        return Response(
            {
                "success": True,
                "message": "Data retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class DepartmentUpdateApi(generics.UpdateAPIView):
    """
    API view for updating department instances.
    """
    serializer_class = CreateDepartmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_object(self, slug):
        try:
            return Department.objects.get(slug=slug)
        except Department.DoesNotExist:
            raise Http404
    
    def get(self, request, slug, format=None):
        Department = self.get_object(slug)
        serializer = DepartmentSerializer(Department)
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


class DepartmentDestroyApi(generics.DestroyAPIView):
    """
    API view for deleting department instances.
    """
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_object(self, slug):
        try:
            return Department.objects.get(slug=slug)
        except Department.DoesNotExist:
            raise Http404
    
    def get(self, request, slug, format=None):
        Department = self.get_object(slug)
        serializer = DepartmentSerializer(Department)
        return Response(serializer.data)

    def delete(self, request, slug):
        instance = Department.objects.get(slug=slug)
        instance.delete()
        return Response(
            {
                "message": "Data deleted successfully", 
            }, 
            status=status.HTTP_204_NO_CONTENT
        )


class CreateJobApi(CreateAPIView):
    """
        Handles the process of creating a new job.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg":"Data created successfully",
                "data":serializer.data
                }, 
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class JobListApi(ListAPIView):
    """
        Handles the process of listing out jobs.
    """
    queryset = Job.objects.all()
    serializer_class = JobListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        jobs = self.get_queryset()
        serializer = self.serializer_class(jobs, many=True)
        return Response({"job-list":serializer.data},
            status=status.HTTP_200_OK)


class JobDetailApi(RetrieveAPIView):
    """
        Displays the details of a specific job.
    """
    queryset = Job.objects.all()
    serializer_class = JobListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        job = self.get_object()
        serializer = self.serializer_class(job)
        return Response({"job-details":serializer.data},
            status=status.HTTP_200_OK)


class UpdateJobApi(UpdateAPIView):
    """
        Handles the process of updating the details of a job.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):     
        job = self.get_object()
        serializer = self.serializer_class(job)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        job = self.get_object()
        serializer = self.serializer_class(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg":"Data updated successfully.",
                "updated-job":serializer.data
                },
                status=status.HTTP_200_OK)
        return Response(serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class DeleteJobApi(DestroyAPIView):
    """
        Deletes a specific job.
    """
    queryset = Job.objects.all()
    serializer_class = JobListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        job = self.get_object()
        serializer = self.serializer_class(job)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        job = self.get_object()
        job.delete()
        return Response({"msg":"Data deleted successfully."},
            status=status.HTTP_204_NO_CONTENT)


class CreateAppliedJobApi(CreateAPIView):
    """
        Handles the process of applying for a specific job by an user.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = CreateAppliedJobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            applied_job = self.get_queryset().get(
                user=request.data['user'],job=request.data['job'])
            if applied_job:
                return Response({"msg":"You have already applied."})
        except:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                instance.interview_status = 'pending'
                instance.save()
                return Response({
                    "msg":"Data created successfully.",
                    "data":serializer.data
                    },
                    status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )


class AppliedJobDetailApi(RetrieveAPIView):
    """
        Displays the details of an applied job.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = AppliedJobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        try:
            applied_job = self.get_object()
            serializer = self.serializer_class(applied_job)
            return Response({"applied-job-details":serializer.data},
                status=status.HTTP_200_OK)
        except:
            return Response({"msg":"Data not found."},
                status=status.HTTP_204_NO_CONTENT)


class AppliedJobListApi(ListAPIView):
    """
        Lists out all applied jobs.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = AppliedJobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            applied_jobs = self.get_queryset()
            serializer = self.serializer_class(applied_jobs, many=True)
            return Response({"applied-jobs-list":serializer.data},
                status=status.HTTP_200_OK)
        except:
            return Response({"msg":"Applied job list not found."},
                status=status.HTTP_204_NO_CONTENT)

  
class ShortlistOrDisallowCandidate(UpdateAPIView):
    """
        Handles the process of shortlisting and not shortlisting a candidate.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = ShortlistCandidateSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        try:
            candidate = self.get_object()
            serializer = self.serializer_class(candidate)
            return Response(serializer.data)
        except:
            return Response({"msg":"Candidate does not exist."},
                status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        candidate = self.get_object()
        serializer = self.serializer_class(
            candidate, data=request.data)
        if serializer.is_valid():
            candidate_status = serializer.save()
            if candidate_status.shortlisted == True:
                return Response(
                    {"msg":"The candidate is shortlisted"})
            else:
                return Response(
                    {"msg":"The candidate is not shortlisted"})


class ShortlistedCandidateList(ListAPIView):
    """
        Lists out all the shortlisted candidate.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = AppliedJobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        candidate_list = self.get_queryset().filter(
            shortlisted=True, job=self.kwargs['slug'])
        serializer = self.serializer_class(candidate_list, many=True)
        return Response({"shortlisted-candidate-list":serializer.data},
            status=status.HTTP_200_OK)


class RetrieveShortlistedCandidate(RetrieveAPIView):
    """
        Retrieves the details of a shortlisted candidate.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = AppliedJobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        try:
            candidate = self.get_queryset().get(slug=self.kwargs['slug'], 
                shortlisted=True)
            serializer = self.serializer_class(candidate)
            return Response({"candidate-details":serializer.data},
                status=status.HTTP_200_OK)
        except:
            return Response(
                {"msg":"Candidate is either not shortlisted or does not exist."},
                status=status.HTTP_204_NO_CONTENT)


class AppliedJobListInterviewPending(ListAPIView):
    """
        Lists out the applied jobs whose interview is pending.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = AppliedJobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        job_list = self.get_queryset().filter(job=self.kwargs['slug'], shortlisted=True, interview_status='pending')
        serializer = self.serializer_class(job_list, many=True)
        return Response({"Applied joblist with interview status pending for job {} are".format(self.kwargs['slug']):serializer.data},
            status=status.HTTP_200_OK)


class AppliedJobListInterviewCompleted(ListAPIView):
    """
        Lists out the applied jobs whose interview is completed.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = AppliedJobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        job_list = self.get_queryset().filter(job=self.kwargs['slug'], shortlisted=True, interview_status='completed')
        serializer = self.serializer_class(job_list, many=True)
        return Response({"Applied joblist with interview status completed for job {} are".format(self.kwargs['slug']):serializer.data},
            status=status.HTTP_200_OK)


class UpdateInterviewStatus(UpdateAPIView):
    """
    Updating the interview status of applied job of a particular user.
    """
    queryset = AppliedJob.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    serializer_class = InterviewStatusSerializer  

    def get_object(self, slug):
        try:
            return AppliedJob.objects.get(slug=slug)
        except AppliedJob.DoesNotExist:
            raise Http404

    def put(self, request, slug, format=None):
        instance = self.get_object(slug)
        serializer = self.get_serializer(instance, data=request.data)
        if instance.shortlisted == True:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Interview Status updated successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
        return Response({"message": "Candidate is not shortlisted",},
                status=status.HTTP_400_BAD_REQUEST,)


class SelectUserJobListApi(ListAPIView):
    """
        Lists out all selected users of a particular job.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = AppliedJobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            selected_user_job = self.get_queryset().filter(result=True, job=self.kwargs['slug'])
            serializer = self.serializer_class(selected_user_job, many=True)

            selected_users = []
            for data in serializer.data:
                detail = {}
                detail['slug'] = data['slug']
                detail['Job' ] = data['job']
                detail['User' ] = data['user']
                detail['UserProfile' ] = data['user_profile']
                detail['Shortlisted' ] = data['shortlisted']
                detail['Interview_status' ] = data['interview_status']
                detail['Result' ] = data['result']
                selected_users.append(detail)

            return Response({"Selected-Users-list":selected_users},
                status=status.HTTP_200_OK)
        except:
            return Response({"msg":"Applied job list not found."},
                status=status.HTTP_204_NO_CONTENT)


class DetailSelectUser(RetrieveAPIView):
    """
        Detail of selected user of a applied job.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = AppliedJobSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):

        applied_job = self.get_object()
        if applied_job.result == True:
            serializer = self.serializer_class(applied_job)

            detail = {}
            detail['Job' ] = serializer.data['job']
            detail['User' ] = serializer.data['user']
            detail['UserProfile' ] = serializer.data['user_profile']
            detail['Shortlisted' ] = serializer.data['shortlisted']
            detail['Interview_status' ] = serializer.data['interview_status']
            detail['Result' ] = serializer.data['result']

            return Response({"Selected-user-detail":detail},
                               status=status.HTTP_200_OK
                            )
        else:
            return Response({"msg":"This candidate is not selected"},
                status=status.HTTP_204_NO_CONTENT)


class SelectUser(UpdateAPIView):
    """
    Selecting a particular user after interview.
    """
    queryset = AppliedJob.objects.all()
    serializer_class = SelectUserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_object(self, slug):
        try:
            return AppliedJob.objects.get(slug=slug)
        except AppliedJob.DoesNotExist:
            raise Http404

    def put(self, request, slug, format=None):
        instance = self.get_object(slug)
        if instance.interview_status == 'completed':
            if self.request.GET['selected'] == 'true':
                instance.result = True
                instance.save()
            else:
                instance.result = False
                instance.save()
            return Response({
                    "success": True,
                    "message": "Data updated successfully",},
                status=status.HTTP_200_OK,)

        return Response({"message": "Interview is not completed",},
                status=status.HTTP_400_BAD_REQUEST,)
