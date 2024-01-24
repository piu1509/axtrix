from rest_framework.test import APITestCase
from rest_framework import status
from modules.venture.models import Organisation
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()


class OrganisationModelAndViewTest(APITestCase):

	# Set up of the test cases.
	def setUp(self):
		self.user = User.objects.create_user('username', 'Pas$w0rd')
		
		self.organisation = Organisation.objects.create(name='BB organisation', website='bb.com', founder='123e4567-e89b-12d3-a456-426614174000', founded_on='2015-05-09', address='ABC-complex, D-block', contact_no='9846727293', headquarter='Delhi', organisation_type='private company', area_served='state wide', description='lorem ipsum dolar met')

		self.organisation_create_url = reverse(
			'venture:create_organisation')

		self.organisation_list_url = reverse(
			'venture:organisation_list')

		self.organisation_retrieve_url = reverse(
			'venture:organisation_detail',
			kwargs={'slug':self.organisation.slug})

		self.organisation_update_url = reverse(
			'venture:update_organisation',
			kwargs={'slug':self.organisation.slug})

		self.organisation_destroy_url = reverse(
			'venture:delete_organisation',
			kwargs={'slug':self.organisation.slug})

		self.client.force_authenticate(user=self.user)

	# Tests Organisation model.
	def test_venture_model(self):		
		self.assertEquals(str(self.organisation), 'BB organisation')
		self.assertEquals(self.organisation.slug, 'bb-organisation')

	# Tests organisation creating view.	
	def test_organisation_create_view(self):
		data = {
		"name":"CD organisation",
		"website":"cd.org",
		"founder":"123e4567-e89b-12d3-a456-426614174000",
		"founded_on":"2012-02-02",
		"address":"BG-Block, SD Road",
		"contact_no":"9933106215",
		"headquarter":"Bengaluru",
		"organisation_type":"govt.",
		"area_served":"national",
		"description":"lorem ipsum dolar"
		}
		response = self.client.post(self.organisation_create_url, data)
		self.assertEquals(response.status_code, status.HTTP_201_CREATED)

	# Tests organisation's list view.
	def test_organisation_list_view(self):
		response = self.client.get(self.organisation_list_url)
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	# Tests organisation retrieve view.
	def test_organisation_retrieve_view(self):
		response = self.client.get(self.organisation_retrieve_url)
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	# Tests organisation update view.
	def test_organisation_update_view(self):
		data = {
		"name":"BASE organisation",
		"website":"base.org",
		"founder":"123e4567-e89b-12d3-a456-426614174000",
		"founded_on":"2012-02-02",
		"address":"BG-Block, SD Road",
		"contact_no":"9933106215",
		"headquarter":"Bengaluru",
		"organisation_type":"govt.",
		"area_served":"national",
		"description":"lorem ipsum dolar"
		}
		response = self.client.put(self.organisation_update_url, data)
		self.assertEquals(response.status_code, status.HTTP_200_OK)

	# Tests organisation destroy view.
	def test_organisation_destroy_view(self):
		response = self.client.delete(self.organisation_destroy_url)		
		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(
            Organisation.objects.filter(slug=self.organisation.slug).exists()
        )
