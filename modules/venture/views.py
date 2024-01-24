from django.shortcuts import render
from modules.venture.models import Organisation
from rest_framework.response import Response
from rest_framework import status
from modules.venture.serializers import (
	CreateOrganisationSerializer,
	OrganisationListSerializer)
from rest_framework.generics import (
	CreateAPIView, 
	ListAPIView, 
	RetrieveAPIView, 
	UpdateAPIView, 
	DestroyAPIView)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreateOrganisation(CreateAPIView):
	"""
		Handles the process of creating a new organisation.
	"""
	queryset = Organisation.objects.all()
	serializer_class = CreateOrganisationSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"msg":"Data created successfully."},
				status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors,
				status=status.HTTP_400_BAD_REQUEST)


class OrganisationList(ListAPIView):
	"""
		Lists out all the organisations.
	"""
	queryset = Organisation.objects.all()
	serializer_class = OrganisationListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [AllowAny]

	def get(self, request):
		queryset = self.get_queryset()
		serializer = self.serializer_class(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class OrganisationDetail(RetrieveAPIView):
	"""
		Displays the details of a specific organisation.
	"""
	queryset = Organisation.objects.all()
	serializer_class = OrganisationListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [AllowAny]
	lookup_field = 'slug'

	def get(self, request, *args, **kwargs):
		organisation = self.get_object()		
		serializer = self.serializer_class(organisation)
		return Response(serializer.data)


class UpdateOrganisation(UpdateAPIView):
	"""
		Handles the process of updating the details of an organisation.
	"""
	queryset = Organisation.objects.all()
	serializer_class = CreateOrganisationSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def put(self, request, *args, **kwargs):
		organisation = self.get_object()
		serializer = self.serializer_class(organisation, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"msg":"Data updated successfully."})
		return Response(serializer.errors,
			status=status.HTTP_400_BAD_REQUEST)


class DeleteOrganisation(DestroyAPIView):
	"""
		Deletes a specific organisation.
	"""
	queryset = Organisation.objects.all()
	serializer_class = OrganisationListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def delete(self, request, *args, **kwargs):
		organisation = self.get_object()
		organisation.delete()
		return Response({"msg":"Data deleted successfully."},
			status=status.HTTP_204_NO_CONTENT)
