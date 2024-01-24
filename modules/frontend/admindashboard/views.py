from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from modules.department.models import Department, Job, AppliedJob
import requests
from decouple import config

username = config('username')
password = config('password')

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from modules.venture.models import Organisation
from modules.department.models import Job
from modules.department.models import AppliedJob
from modules.zoom_meeting.models import ZoomMeeting
from decouple import config

username1 = config('USERNAME')
password1 = config('PASSWORD')

class Admin(View):
    """
        Renders the admin dashboard template.
    """
    def get(self, request):
        return render(request, 'admindashboard/adminhome.html')


class DepartmentListTemplateView(View):
    """
        Calls the department list API view and renders the data in template. 
    """
    def get(self, request, *args, **kwargs):
        response = requests.get(
            'http://localhost:8000/department/department_list/',
            auth=(username, password))
        context = response.json()['data']
        paginator = Paginator(context, 5)
        page = request.GET.get('page', 1)
        try:
            departments = paginator.page(page)
        except PageNotAnInteger:
            departments = paginator.page(1)
        except EmptyPage:
            departments = paginator.page(paginator.num_pages)
        return render(
            request,
            'department/department_list.html',
            {'data_list':departments})


class DepartmentDetailsTemplateView(View):
    """
        Calls the department retrieve API view and renders the details in template.
    """
    def get(self, request, *args, **kwargs):
        response = requests.get(
            'http://localhost:8000/department/department_retrieve/'+str(self.kwargs['slug'])+'/',
            auth=(username, password))
        context = response.json()
        return render(
            request,
            'department/department_detail.html',
            {'data':context['data']})
        

class DepartmentCreateTemplateView(View):
    """
        Renders the department create form in template using input fields and creates department through calling the department create API view by the data posted in the template. 
    """
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'department/department_create.html')

    def post(self, request, *args, **kwargs):
        data = {
        "organization":request.POST['organization'],
        "department_name":request.POST['department_name'],
        "employee":request.POST['employee']
        }
        response = requests.post(
            'http://localhost:8000/department/department_create/',
            data=data,
            auth=(username, password))
        return redirect('admindashboard:department_list')


class DepartmentUpdateTemplateView(View):
    """
        Renders the department update form in template using input fields and updates department through calling the department update API view by the data posted in the template. 
    """
    def get(self, request, *args, **kwargs):
        department = get_object_or_404(
            Department,
            slug=self.kwargs['slug'])
        return render(
            request,
            'department/department_update.html',
            { 'department':department})

    def post(self, request, *args, **kwargs):
        data = {
        "organization":request.POST['organization'],
        "department_name":request.POST['department_name'],
        "employee":request.POST['employee']
        }
        response = requests.put(
            'http://localhost:8000/department/department_update/'+str(self.kwargs['slug'])+'/',
            data=data,
            auth=(username, password))
        return redirect(
            'admindashboard:department_detail',
            slug=self.kwargs['slug'])


class DepartmentDeleteTemplateView(View):
    """
        Deletes the chosen department by calling the department delete API view.
    """
    def get(self, request, *args, **kwargs):
        department = get_object_or_404(
            Department,
            slug=self.kwargs['slug'])
        return render(
            request,
            'department/department_delete.html',
            {'department':department})

    def post(self, request, *args, **kwargs):
        response = requests.delete(
            'http://localhost:8000/department/department_delete/'+str(self.kwargs['slug'])+'/',
            auth=(username, password))
        return redirect('admindashboard:department_list')


class JobListTemplateView(View):
    """
        Calls the Job list API view and renders the list data to template.
    """
    def get(self, request, *args, **kwargs):
        response = requests.get(
            'http://localhost:8000/department/job_list/')
        context = response.json()['job-list']
        paginator = Paginator(context, 5)
        page = request.GET.get('page', 1)
        try:
            job_list = paginator.page(page)
        except PageNotAnInteger:
            job_list = paginator.page(1)
        except EmptyPage:
            job_list = paginator.page(paginator.num_pages)
        return render(
            request,
            'job/job_list.html',
            {'job_list':job_list})


class JobDetailsTemplateView(View):
    """
        Calls the Job retrieve API view and renders the details to template.
    """
    def get(self, request, *args, **kwargs):
        response = requests.get(
            'http://localhost:8000/department/job_detail/'+str(self.kwargs['slug']))
        context = response.json()
        return render(
            request,
            'job/job_detail.html',
            {'job':context['job-details']})


class JobUpdateTemplateView(View):
    """
        Renders the job update form using input fields into a template and update job through calling the Job update API view by the data posted in the template.
    """
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(
            Job,
            slug=self.kwargs['slug'])
        return render(
            request, 
            'job/job_update.html',
            {'job':job})

    def post(self, request, *args, **kwargs):
        data = {
        "title":request.POST['title'],
        "organization":request.POST['organization'],
        "job_poster":request.POST['job_poster'],
        "address":request.POST['address'],
        "description":request.POST['description'],
        "skills_required":request.POST['skills_required'],
        "experience":request.POST['experience'],
        "salary":request.POST['salary'],
        "qualifications":request.POST['qualifications'],
        "vacancies":request.POST['vacancies']
        }
        response = requests.put(
            'http://localhost:8000/department/update_job/'+str(self.kwargs['slug']), 
            data=data, 
            auth=(username, password))
        return redirect(
            'admindashboard:job_detail', 
            slug=self.kwargs['slug'])


class JobDeleteTemplateView(View):
    """
        Deletes a specific job by calling Job destroy API view.
    """
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(
            Job, 
            slug=self.kwargs['slug'])
        return render(
            request, 
            'job/job_delete.html', 
            {'job':job})

    def post(self, request, *args, **kwargs):
        response = requests.delete(
            'http://localhost:8000/department/delete_job/'+str(self.kwargs['slug']), 
            auth=(username, password))
        return redirect('admindashboard:job_list')


class InterviewPendingListTemplateView(View):
    """
        Call the Interview pending list API view and renders the list into a template.
    """
    def get(self, request, *args, **kwargs):
        response = requests.get(
            'http://localhost:8000/department/applied_jobs_interview_pending/'+str(self.kwargs['slug']),
            auth=(username, password))
        user_list = response.json()['Applied joblist with interview status pending for job {} are'.format(self.kwargs['slug'])]
        paginator = Paginator(user_list, 5)
        page = request.GET.get('page', 1)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(
            request, 
            'apply_job/interview_pending_list.html', 
            {'pending_users':users})


class InterviewCompletedListTemplateView(View):
    """
        Calls the Interview completed list API view and renders the list into a template.
    """
    def get(self, request, *args, **kwargs):
        response = requests.get(
            'http://localhost:8000/department/applied_jobs_interview_completed/'+str(self.kwargs['slug']), 
            auth=(username, password))
        user_list = response.json()['Applied joblist with interview status completed for job {} are'.format(self.kwargs['slug'])]
        paginator = Paginator(user_list, 5)
        page = request.GET.get('page', 1)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(
            request, 
            'apply_job/interview_completed_list.html', 
            {'completed_users':users})


class SelectedUserListTemplateView(View):
    """
        Calls the selected user list API view and renders the list into a template.
    """
    def get(self, request, *args, **kwargs):
        response = requests.get(
            'http://localhost:8000/department/select_user_list/'+str(self.kwargs['slug']), 
            auth=(username, password))
        user_list = response.json()['Selected-Users-list']
        paginator = Paginator(user_list, 5)
        page = request.GET.get('page', 1)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(
            request, 
            'apply_job/selected_user_list.html', 
            {'selected_users':users})


class SelectedUserDetailsTemplateView(View):
    """
        Call the selected user retrieve API view and renders the details into a template.
    """
    def get(self, request, *args, **kwargs):
        response = requests.get(
            'http://localhost:8000/department/select_user_detail/'+str(self.kwargs['slug']), 
            auth=(username, password))
        user = response.json()['Selected-user-detail']
        return render(
            request, 
            'apply_job/selected_user_details.html', 
            {'user':user})
        

class VenturesListView(ListView):
    """
    class to show venture list
    """
    model = Organisation
    template_name = "ventures/ventures_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        result = requests.get('http://127.0.0.1:8000/venture/organisation_list/')
        context['ventures_list'] = result.json()
        return context


class VenturesDetailView(DetailView):
    """
    class to show venture details
    """
    model = Organisation
    template_name = "ventures/ventures_detail.html"

    # function to get context data
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']  # Get the slug from the URL parameters
        result = requests.get(f'http://127.0.0.1:8000/venture/organisation_detail/{slug}')
        context['ventures_detail'] = result.json()
        return context


class VenturesDeleteView(DeleteView):
    """
    class to delete a venture
    """
    model = Organisation
    fields = '__all__'
    template_name = "ventures/ventures_delete.html"

    # function to get context data
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']  # Get the slug from the URL parameters
        venture = Organisation.objects.get(slug=slug)
        context['name'] = venture.name
        return context

    def post(self, request,  *args, **kwargs):
        slug = self.kwargs['slug']  # Get the slug from the URL parameters
        username = username1
        password = password1

        # Sending a POST request to the specified URL/API with the job data
        url = (f'http://127.0.0.1:8000/venture/delete_organisation/{slug}')
        response = requests.delete(url, auth=(username, password))

        # Checking the response status and handling accordingly
        if response.status_code == 204:
            return redirect("admindashboard:ventures")
        else:
            return HttpResponse("Error occurred while deleting the organization.")


class JobCreateView(CreateView):
    """
    class based view to create job
    """
    model = Job
    fields = "__all__"
    template_name = "job/job_create.html"

    def get(self, request,  *args, **kwargs):
        return render(request, 'job/job_create.html')

    def post(self, request,  *args, **kwargs):
        # Getting the html form data from the request
        title = request.POST.get('title')
        organization = request.POST.get('organization')
        job_poster = request.POST.get('job_poster')
        description = request.POST.get('description')
        experience = request.POST.get('experience')
        salary = request.POST.get('salary')
        skills_required = request.POST.get('skills_required')
        address = request.POST.get('address')
        vacancies = request.POST.get('vacancies')
        qualifications = request.POST.get('qualifications')

        # Getting the data from the job object
        job_data = {
            "title": title,
            "organization": organization,
            "job_poster": job_poster,
            "description": description,
            "experience": experience,
            "salary": salary,
            "skills_required": skills_required,
            "address": address,
            "vacancies": vacancies,
            "qualifications": qualifications
        }
        username = username1
        password = password1

        # Sending a POST request to the specified URL/API with the job data
        url = "http://127.0.0.1:8000/department/create_job/"
        response = requests.post(url, data=job_data, auth=(username, password))

        # Checking the response status and handling accordingly
        if response.status_code == 201:
            return redirect("admindashboard:job_list")
        else:
            return HttpResponse("Error occurred while creating the job.")


class ApplyJobCreateView(CreateView):
    """
    class based view to create apply_job
    """
    model = AppliedJob
    fields = "__all__"
    template_name = "apply_job/apply_job_create.html"

    def get(self, request,  *args, **kwargs):
        return render(request, 'apply_job/apply_job_create.html')

    def post(self, request,  *args, **kwargs):
        # Getting the html form data from the request
        job = request.POST.get('job')
        user = request.POST.get('user')
        user_profile = request.POST.get('user_profile')
        apply_job = {
            "job": job,
            "user": user,
            "user_profile": user_profile,
        }

        username = username1
        password = password1

        # Sending a POST request to the specified URL/API with the job data
        url = "http://127.0.0.1:8000/department/create_applied_job/"
        response = requests.post(url, data=apply_job, auth=(username, password))

        # Checking the response status and handling accordingly
        if response.status_code == 201:
            return redirect("admindashboard:apply_job_list")
        else:
            return HttpResponse("Error occurred while applying for the job.")


class ApplyJobListView(ListView):
    """
    class to show apply_job list
    """
    model = AppliedJob
    template_name = "apply_job/apply_job_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        username = username1
        password = password1
        url = "http://127.0.0.1:8000/department/applied_job_list/"
        result = requests.get(url, auth=(username, password))
        context['apply_job_list'] = result.json()['applied-jobs-list']
        return context


class ApplyJobDetailView(DetailView):
    """
    class to show apply_job details
    """
    model = AppliedJob
    template_name = "apply_job/apply_job_detail.html"

    # function to get context data
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']  # Getting the slug from the URL parameters
        username = username1
        password = password1
        url = f'http://127.0.0.1:8000/department/applied_job_detail/{slug}'
        result = requests.get(url, auth=(username, password))
        context['apply_job_detail'] = result.json()['applied-job-details']
        return context


class ShortListView(ListView):
    """
    class to shortlist or remove from shortlist candidate
    """
    model = AppliedJob
    template_name = "apply_job/shortlist_user.html"

    def get_context_data(self, *args, **kwargs):
        """
        To get the shortlist status of applied-job/candidate
        """
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']  # Get the slug from the URL parameters
        username = username1
        password = password1
        url = f'http://127.0.0.1:8000/department/shortlist_candidate/{slug}'
        result = requests.get(url, auth=(username, password))
        context['shortlist_user'] = result.json()['shortlisted']
        context['slug_param'] = slug
        return context

    def post(self, request, *args, **kwargs):
        """
        To change the shortlist status of applied-job/candidate
        """
        slug = self.kwargs['slug']  # Getting the slug from the URL parameters
        username = username1
        password = password1
        url1 = f'http://127.0.0.1:8000/department/shortlist_candidate/{slug}'
        if 'remove_shortlist' in request.POST:
            shortlist_status = {
                "shortlisted": False,
            }
            result1 = requests.put(url1, data=shortlist_status, auth=(username, password))
        elif 'add_shortlist' in request.POST:
            shortlist_status = {
                "shortlisted": True,
            }
            result1 = requests.put(url1, data=shortlist_status, auth=(username, password))
        return redirect("admindashboard:shortlisted_user_detail", slug=slug)  # Redirecting to a success page or desired URL


class ShortListDetailView(DetailView):
    """
    class to show details of shortlisted user
    """
    model = AppliedJob
    template_name = "apply_job/shortlisted_user_detail.html"

    # function to get context data
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']  # Get the slug from the URL parameters
        username = username1
        password = password1
        url = f'http://127.0.0.1:8000/department/shortlisted_candidate_detail/{slug}'
        result = requests.get(url, auth=(username, password))
        if result.status_code == 204 :
            context['shortlisted_candidate_details'] = None
        else:
            context['shortlisted_candidate_details'] = result.json()['candidate-details']
        return context


class ShortListCandidateListView(ListView):
    """
    class to show list of shortlisted users
    """
    model = AppliedJob
    template_name = "apply_job/shortlisted_user_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']  # Get the slug from the URL parameters
        username = username1
        password = password1
        url = f'http://127.0.0.1:8000/department/shortlisted_candidate_list/{slug}'
        result = requests.get(url, auth=(username, password))
        context['shortlisted_list'] = result.json()['shortlisted-candidate-list']
        return context


class ZoomLinkCreateAPIView(CreateView):
    """
    Class to create zoom meetings and send the link in mail.
    """
    model = ZoomMeeting
    fields = "__all__"
    template_name = "zoom_meeting/zoom_meeting_create.html"

    def post(self, request,  *args, **kwargs):
        # Getting the html form data from the request
        meeting_title = request.POST.get('meeting_title')
        meeting_description = request.POST.get('meeting_description')
        meeting_date = request.POST.get('meeting_date')
        meeting_time = request.POST.get('meeting_time')
        meeting_duration = request.POST.get('meeting_duration')
        email = request.POST.get('email')
        status = request.POST.get('status')
        job = request.POST.get('job')

        # Getting the data from the job object
        meet_data = {
            "meeting_title": meeting_title,
            "meeting_description": meeting_description,
            "meeting_date": meeting_date,
            "meeting_time": meeting_time,
            "meeting_duration": meeting_duration,
            "email": email,
            "status": status,
            "job": job,
        }
        username = username1
        password = password1

        # Sending a POST request to the specified URL/API with the job data
        url = "http://127.0.0.1:8000/zoom_meeting/zoom_link_create/"
        response = requests.post(url, data=meet_data, auth=(username, password))

        # Checking the response status and handling accordingly
        if response.status_code == 201:
            return redirect("admindashboard:zoom_link_list")
        else:
            return HttpResponse("Error occurred while creating the job.")


class ZoomLinkListView(ListView):
    """
    class to show zoom meetings list
    """
    model = ZoomMeeting
    template_name = "zoom_meeting/zoom_meeting_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        username = username1
        password = password1
        url = f'http://127.0.0.1:8000/zoom_meeting/zoom_link_list/'
        result = requests.get(url, auth=(username, password))
        context['zoom_meeting_list'] = result.json()['data']
        return context


class ZoomMeetingUpdateView(UpdateView):
    """
    Class for updating zoom meeting.
    """
    model = ZoomMeeting
    fields = '__all__'
    template_name = "zoom_meeting/zoom_meeting_update.html"

    def get(self, request, *args, **kwargs):
        meet = get_object_or_404( ZoomMeeting, slug=self.kwargs['slug'])
        return render(request, 'zoom_meeting/zoom_meeting_update.html', { 'meet':meet})

    def post(self, request, *args, **kwargs):
        username = username1
        password = password1
        slug = self.kwargs['slug']  # Get the slug from the URL parameters
        data = {
            "meeting_title":request.POST['meeting_title'],
            "meeting_description":request.POST['meeting_description'],
            "meeting_date":request.POST['meeting_date'],
            "meeting_time":request.POST['meeting_time'],
            "meeting_duration":request.POST['meeting_duration'],
            "email":request.POST['email'],
            "status":request.POST['status'],
            "job":request.POST['job']
        }
        url = f'http://127.0.0.1:8000/zoom_meeting/zoom_meet_update/{slug}/'
        response = requests.put(url, data=data, auth=(username, password))
        return redirect('admindashboard:zoom_link_list')


class ZoomStatusUpdateView(UpdateView):
    """
    Class for updating zoom meeting's status.
    """
    model = ZoomMeeting
    fields = '__all__'
    template_name = "zoom_meeting/zoom_status_update.html"

    def get(self, request, *args, **kwargs):
        meet = get_object_or_404( ZoomMeeting, slug=self.kwargs['slug'])
        return render(request, 'zoom_meeting/zoom_status_update.html', { 'meet':meet})

    def post(self, request, *args, **kwargs):
        username = username1
        password = password1
        slug = self.kwargs['slug']  # Get the slug from the URL parameters
        data = {
            "status":request.POST['status'],
        }
        url = f'http://127.0.0.1:8000/zoom_meeting/zoom_link_update/{slug}/'
        response = requests.put(url, data=data, auth=(username, password))
        return redirect('admindashboard:zoom_link_list')

class UpdateInterviewStatusTemplateView(View):
    """
        Calls the Update interview status view and changes the interview status of an applied job.
    """
    def get(self, request, *args, **kwargs):
        return render(
            request, 
            'apply_job/interview_status.html')

    def post(self, request, *args, **kwargs):
        applied_job = get_object_or_404(
            AppliedJob, 
            slug=self.kwargs['slug'])
        data = {
        "interview_status":request.POST['interview_status']
        }
        response = requests.put(
            'http://localhost:8000/department/interview_status/'+str(self.kwargs['slug'])+'/', 
            data=data, 
            auth=(username, password))
        return redirect(
            'admindashboard:interview_completed_list', 
            slug=applied_job.job)


class SelectUserTemplateView(View):
    """
        Calls the select user API view and selects an user whose interview is completed.
    """
    def get(self, request, *args, **kwargs):
        return render(
            request, 
            'apply_job/select_user.html')

    def post(self, request, *args, **kwargs):
        applied_job = get_object_or_404(
            AppliedJob, 
            slug=self.kwargs['slug'])
        response = requests.put(
            'http://localhost:8000/department/select_user/'+str(self.kwargs['slug'])+'/?selected=true', 
            auth=(username, password))
        return redirect(
            'admindashboard:selected_user_list', 
            slug=applied_job.job)
