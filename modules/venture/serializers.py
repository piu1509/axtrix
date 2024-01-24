from rest_framework import serializers
from rest_framework.response import Response
from modules.venture.models import Organisation


class CreateOrganisationSerializer(serializers.ModelSerializer):
	"""
		Serializer class for creating and updating an organisation.
	"""
	class Meta:
		model = Organisation
		fields = ['name','image','website',
		'founder','founded_on','address',
		'contact_no','organisation_type',
		'area_served','description']
					

class OrganisationListSerializer(serializers.ModelSerializer):
	"""
		Serializer class for listing out all organisations and 
		displaying the details of an organisation.
	"""
	class Meta:
		model = Organisation
		fields = ['gid','slug','name','image','website',
		'founder','founded_on','address',
		'contact_no','organisation_type',
		'area_served','description']