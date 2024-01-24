from rest_framework import serializers
from modules.department.models import (
    Department,
    Job,
    AppliedJob
    )


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Department model.
    """
    class Meta:
        model = Department
        fields = ['department_name', 'employee', 'organization','slug']


class CreateDepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Department model.
    """
    class Meta:
        model = Department
        fields = ['department_name', 'employee', 'organization']


class JobSerializer(serializers.ModelSerializer):
    """
        Serializer class for creating and updating a job post.
    """
    class Meta:
        model = Job
        fields = ['title','organization','job_poster','description','experience','salary','address','skills_required','vacancies','qualifications']

    # Validates experience field so that a valid experience is given.
    def validate_experience(self, data):
        try:
            experience = float(data)
            if experience<0:
                raise serializers.ValidationError("Enter valid experience.")
            if experience>20:
                raise serializers.ValidationError("We need an young professional.")
        except(ValueError, TypeError):
            raise serializers.ValidationError("Experience should be in year.")
        return data 

    # Validates salary field so that a valid salary amount is given.
    def validate_salary(self, value):
        try:
            salary = float(value)
            if salary<5000:
                raise serializers.ValidationError("Salary should be bigger amount.")
        except(ValueError, TypeError):
            raise serializers.ValidationError("Enter a valid salary amount.")
        return value
        

class JobListSerializer(serializers.ModelSerializer):
    """
        Serializer class for listing out all jobs and retrieving a job post detail.
    """
    class Meta:
        model = Job
        fields = ['gid','slug','title','organization','job_poster','description','experience','salary','address','skills_required','vacancies','qualifications','created_at']


class CreateAppliedJobSerializer(serializers.ModelSerializer):
    """
        Serializer class for applying to a job.
    """
    class Meta:
        model = AppliedJob
        fields = ['job','user','user_profile']


class AppliedJobSerializer(serializers.ModelSerializer):
    """
        Serializer class for displaying list of applied jobs and details of an applied job.
    """
    class Meta:
        model = AppliedJob
        fields = ['slug','job','user','user_profile','shortlisted','interview_status','result']


class ShortlistCandidateSerializer(serializers.ModelSerializer):
    """
        Serializer class for shortlisting a candidate.
    """
    class Meta:
        model = AppliedJob
        fields = ['shortlisted']


class InterviewStatusSerializer(serializers.ModelSerializer):
    """
        Serializer class to update interview status.
    """
    class Meta:
        model = AppliedJob
        fields = ['slug','job','user','user_profile','shortlisted','interview_status','result']
        read_only_fields = ['slug','job','user','user_profile','shortlisted','result',]


class SelectUserSerializer(serializers.ModelSerializer):
    """
        Serializer class to select candidates.
    """
    class Meta:
        model = AppliedJob
        fields = ['slug','job','user','user_profile','shortlisted','interview_status','result']
        read_only_fields = ['slug','job','user','user_profile','shortlisted','interview_status', 'result']
