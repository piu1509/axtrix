from django.shortcuts import render
from modules.gst.models import (
	Category, Products, 
	Customers, Vehicles, 
	Invoices)

from modules.gst.serializers import (
	CategorySerializer, ProductCreateSerializer, 
	ProductListSerializer, CustomerCreateSerializer, 
	CustomerListSerializer, VehicleCreateSerializer, 
	VehicleListSerializer, InvoiceCreateSerializer, 
	InvoiceListSerializer)

from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class CategoryCreateAPIView(CreateAPIView):
	"""
	API view for creating a new category instance.
	"""
	serializer_class = CategorySerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(
			data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"msg": "Category created successfully.",
				"data": serializer.data
				}, 
				status=status.HTTP_201_CREATED)
			return Response(serializer.errors,
				status=status.HTTP_400_BAD_REQUEST)


class ProductCreateAPIView(CreateAPIView):
	"""
	Handles the process of creating a product instance.
	"""
	serializer_class = ProductCreateSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(
			data=request.data)
		if serializer.is_valid():
			product = serializer.save()
			return Response({
				"msg": "Data created successfully.",
				"data": serializer.data
				}, 
				status=status.HTTP_201_CREATED)
		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(ListAPIView):
	"""
	Handles the process of listing out all the products.
	"""
	queryset = Products.objects.all()
	serializer_class = ProductListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [AllowAny]

	def get(self, request, *args, **kwargs):
		products = self.get_queryset()
		serializer = self.serializer_class(
			products, many=True)
		return Response({
			"products": serializer.data
			}, 
			status=status.HTTP_200_OK)


class ProductRetrieveAPIView(RetrieveAPIView):
	"""
	API view for retrieving the details of a product instance. 
	"""
	queryset = Products.objects.all()
	serializer_class = ProductListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [AllowAny]
	lookup_field = 'slug'

	def get(self, request, *args, **kwargs):
		product = self.get_object()
		serializer = self.serializer_class(product)
		return Response({
			"product":serializer.data
			}, 
			status=status.HTTP_200_OK)


class ProductUpdateAPIView(UpdateAPIView):
	"""
	Handles the process of updating a product instance.
	"""
	queryset = Products.objects.all()
	serializer_class = ProductCreateSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def put(self, request, *args, **kwargs):
		product = self.get_object()
		serializer = self.serializer_class(
			product, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"msg": "Data updated successfully.",
				"data":serializer.data
				}, 
				status=status.HTTP_200_OK)
		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class ProductDestroyAPIView(DestroyAPIView):
	"""
	Handles the process of deleting a product instance.
	"""
	queryset = Products.objects.all()
	serializer_class = ProductListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def delete(self, request, *args, **kwargs):
		product = self.get_object()
		product.delete()
		return Response({
			"msg":"Data deleted successfully."
			}, 
			status=status.HTTP_204_NO_CONTENT)


class CustomerCreateAPIView(CreateAPIView):
	"""
	Creates a customer instance.
	"""
	serializer_class = CustomerCreateSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(
			data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"msg": "Data created successfully.",
				"data": serializer.data
				}, 
				status=status.HTTP_201_CREATED)
		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class CustomerListAPIView(ListAPIView):
	"""
	Lists out all the customers.
	"""
	queryset = Customers.objects.all()
	serializer_class = CustomerListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		customers = self.get_queryset()
		serializer = self.serializer_class(
			customers, many=True)
		return Response({
			"customers": serializer.data
			}, 
			status=status.HTTP_200_OK)


class CustomerRetrieveAPIView(RetrieveAPIView):
	"""
	API view for retrieving the details of a customer.
	"""
	queryset = Customers.objects.all()
	serializer_class = CustomerListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def get(self, request, *args, **kwargs):
		customer = self.get_object()
		serializer = self.serializer_class(customer)
		return Response({
			"customer":serializer.data
			}, 
			status=status.HTTP_200_OK)


class CustomerUpdateAPIView(UpdateAPIView):
	"""
	Updates a customer instance.
	"""
	queryset = Customers.objects.all()
	serializer_class = CustomerCreateSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def put(self, request, *args, **kwargs):
		customer = self.get_object()
		serializer = self.serializer_class(
			customer, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"msg": "Data updated successfully.",
				"data":serializer.data
				}, 
				status=status.HTTP_200_OK)
		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class CustomerDestroyAPIView(DestroyAPIView):
	"""
	Deletes a customer instance.
	"""
	queryset = Customers.objects.all()
	serializer_class = CustomerListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def delete(self, request, *args, **kwargs):
		customer = self.get_object()
		customer.delete()
		return Response({
			"msg":"Data deleted successfully."
			}, 
			status=status.HTTP_204_NO_CONTENT)


class VehicleCreateAPIView(CreateAPIView):
	"""
	Creates a vehicle instance. 
	"""
	serializer_class = VehicleCreateSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(
			data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"msg": "Data created successfully.",
				"data": serializer.data
				}, 
				status=status.HTTP_201_CREATED)
		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class VehicleListAPIView(ListAPIView):
	"""
	Lists out all the vehicles.
	"""
	queryset = Vehicles.objects.all()
	serializer_class = VehicleListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		vehicles = self.get_queryset()
		serializer = self.serializer_class(
			vehicles, many=True)
		return Response({
			"vehicles": serializer.data
			}, 
			status=status.HTTP_200_OK)


class VehicleRetrieveAPIView(RetrieveAPIView):
	"""
	API view for retrieving the details of a vehicle instance.
	"""
	queryset = Vehicles.objects.all()
	serializer_class = VehicleListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def get(self, request, *args, **kwargs):
		vehicle = self.get_object()
		serializer = self.serializer_class(vehicle)
		return Response({
			"vehicle":serializer.data
			}, 
			status=status.HTTP_200_OK)


class VehicleUpdateAPIView(UpdateAPIView):
	"""
	Updates a specific vehicle instance.
	"""
	queryset = Vehicles.objects.all()
	serializer_class = VehicleCreateSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def put(self, request, *args, **kwargs):
		vehicle = self.get_object()
		serializer = self.serializer_class(
			vehicle, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"msg": "Data updated successfully.",
				"data":serializer.data
				}, 
				status=status.HTTP_200_OK)
		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class VehicleDestroyAPIView(DestroyAPIView):
	"""
	Deletes a specific vehicle instance.
	"""
	queryset = Vehicles.objects.all()
	serializer_class = VehicleListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def delete(self, request, *args, **kwargs):
		vehicle = self.get_object()
		vehicle.delete()
		return Response({
			"msg":"Data deleted successfully."
			}, 
			status=status.HTTP_204_NO_CONTENT)


class InvoiceCreateAPIView(CreateAPIView):
	"""
	Creates a new invoice instance.
	"""
	serializer_class = InvoiceCreateSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(
			data=request.data)
		if serializer.is_valid():
			invoice = serializer.save()
			data = {}
			data["invoice_name"] = invoice.invoice_name
			data["invoice_number"] = invoice.invoice_number
			data["customer"] = invoice.customer
			data["product"] = invoice.product
			data["vehicle"] = invoice.vehicle			
			return Response({
				"msg": "Data created successfully.",
				"data": data
				}, 
				status=status.HTTP_201_CREATED)
		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class InvoiceListAPIView(ListAPIView):
	"""
	Lists out all the invoices.
	"""
	queryset = Invoices.objects.all()
	serializer_class = InvoiceListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		invoices = self.get_queryset()
		serializer = self.serializer_class(
			invoices, many=True)
		return Response({
			"invoices": serializer.data
			}, 
			status=status.HTTP_200_OK)


class InvoiceRetrieveAPIView(RetrieveAPIView):
	"""
	API view for retrieving the details of an invoice instance.
	"""
	queryset = Invoices.objects.all()
	serializer_class = InvoiceListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def get(self, request, *args, **kwargs):
		invoice = self.get_object()
		serializer = self.serializer_class(invoice)
		return Response({
			"invoice":serializer.data
			}, 
			status=status.HTTP_200_OK)


class InvoiceUpdateAPIView(UpdateAPIView):
	"""
	Updates a specific invoice instance.
	"""
	queryset = Invoices.objects.all()
	serializer_class = InvoiceCreateSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def put(self, request, *args, **kwargs):
		invoice = self.get_object()
		serializer = self.serializer_class(
			invoice, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"msg": "Data updated successfully.",
				"data":serializer.data
				}, 
				status=status.HTTP_200_OK)
		return Response(serializer.errors, 
			status=status.HTTP_400_BAD_REQUEST)


class InvoiceDestroyAPIView(DestroyAPIView):
	"""
	Deletes the chosen invoice instance.
	"""
	queryset = Invoices.objects.all()
	serializer_class = InvoiceListSerializer
	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAuthenticated]
	lookup_field = 'slug'

	def delete(self, request, *args, **kwargs):
		invoice = self.get_object()
		invoice.delete()
		return Response({
			"msg":"Data deleted successfully."
			}, 
			status=status.HTTP_204_NO_CONTENT)
