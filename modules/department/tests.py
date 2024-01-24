from modules.department.models import Department, Job
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()


class DepartmentModelAndViewTest(APITestCase):

	# Set up for the test cases.
	def setUp(self):
		self.user = User.objects.create_user(
			'username','Pas$w0rd')

		self.department = Department.objects.create(
			department_name="hr",
			employee="a24a6ea4-ce75-4665-a070-57453082c256",
			organization="123e4567-e89b-12d3-a456-426614174000")

		self.department_create_url = reverse(
			'department:department_create')

		self.department_list_url = reverse(
			'department:department_list')

		self.department_retrieve_url = reverse(
			'department:department_retrieve',
			kwargs={'slug':self.department.slug})

		self.department_update_url = reverse(
			'department:department_update',
			kwargs={'slug':self.department.slug})

		self.department_destroy_url = reverse(
			'department:department_delete',
			kwargs={'slug':self.department.slug})

		self.client.force_authenticate(user=self.user)

	# Tests Department model.
	def test_department_model(self):
		self.assertEquals(self.department.slug, 'hr')

	# Tests department create view.
	def test_department_create_view(self):
		data = {
		"department_name":"hr",
		"employee":"a24a6ea4-ce75-4665-a070-57453082c256",
		"organization":"123e4567-e89b-12d3-a456-426614174000"
		}
		response = self.client.post(self.department_create_url,data)
		self.assertEquals(response.status_code, status.HTTP_201_CREATED)

	# Tests department list view.
	def test_department_list_view(self):
		response = self.client.get(self.department_list_url)
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	# Tests department retrieve view.
	def test_department_retrieve_view(self):
		response = self.client.get(self.department_retrieve_url)
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	# Tests department update view.
	def test_department_update_view(self):
		data = {
		"department_name":"developer",
		"employee":"a24a6ea4-ce75-4665-a070-57453082c256",
		"organization":"123e4567-e89b-12d3-a456-426614174000"
		}
		response = self.client.put(self.department_update_url, data)
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	# Tests department destroy view.
	def test_department_destroy_view(self):
		response = self.client.delete(self.department_destroy_url)
		self.assertFalse(
            Department.objects.filter(slug=self.department.slug).exists()
        )
		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
		

class JobModelAndViewTest(APITestCase):

	# Set up for the test cases.
	def setUp(self):
		self.user = User.objects.create_user('username', 'Pas$w0rd')

		self.job = Job.objects.create(title='Software developer',
			organization='123e4567-e89b-12d3-a456-426614174000',
			job_poster='a24a6ea4-ce75-4665-a070-57453082c256',
			description='dolar amet lorem ipsum',
			experience='3.5',
			salary='35000',
			skills_required='python, django',
			address='ABC-complex, D-block',
			vacancies='3',
			qualifications='B.Tech')

		self.job_create_url = reverse('department:create_job')

		self.job_list_url = reverse('department:job_list')

		self.job_retrieve_url = reverse('department:job_detail', kwargs={'slug':self.job.slug})

		self.job_update_url = reverse('department:update_job', kwargs={'slug':self.job.slug})

		self.job_destroy_url = reverse('department:delete_job', kwargs={'slug':self.job.slug})

		self .client.force_authenticate(user=self.user)

	# Tests Job model.
	def test_job_model(self):		
		self.assertEquals(str(self.job), 'Software developer')
		self.assertEquals(self.job.slug, 'software-developer')

	# Tests job create view.
	def test_job_create_view(self):
		data = {
		"title":"Graphic designer",
		"organization":"123e4567-e89b-12d3-a456-426614174000",
		"job_poster":"a24a6ea4-ce75-4665-a070-57453082c256",
		"description":"lorem ipsum dolar amet",
		"experience":"2.5",
		"salary":"30000",
		"skills_required":"UI, UX",
		"address":"ABC-complex, D-block",
		"vacancies":"2",
		"qualifications":"Graduate"
		}
		response = self.client.post(self.job_create_url, data)
		self.assertEquals(response.status_code, status.HTTP_201_CREATED)

	# Tests job list view.
	def test_job_list_view(self):
		response = self.client.get(self.job_list_url)
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	# Tests job retrieve view.
	def test_job_retrieve_view(self):
		response = self.client.get(self.job_retrieve_url)
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	# Tests job update view.
	def test_job_update_view(self):
		data = {
		"title":"Software developer",
		"organization":"123e4567-e89b-12d3-a456-426614174000",
		"job_poster":"a24a6ea4-ce75-4665-a070-57453082c256",
		"description":"lorem ipsum dolar amet",
		"experience":"2.5",
		"salary":"30000",
		"skills_required":"python, django, django Rest API",
		"address":"ABC-complex, D-block",
		"vacancies":"2",
		"qualifications":"B.Tech"
		}
		response = self.client.put(self.job_update_url, data)
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	# Tests job destroy view.
	def test_job_destroy_view(self):
		response = self.client.delete(self.job_destroy_url)
		self.assertFalse(
            Job.objects.filter(slug=self.job.slug).exists()
        )
		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
		