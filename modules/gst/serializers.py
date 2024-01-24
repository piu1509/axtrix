from modules.gst.models import (
	Category, Products, 
	Customers, Vehicles, 
	Invoices)
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
	"""
	Serializer class for creating a category.
	"""
	class Meta:
		model = Category
		fields = ['name']


class ProductCreateSerializer(serializers.ModelSerializer):
	"""
	Serializer class for creating and updating a product.
	"""
	category = CategorySerializer()

	class Meta:
		model = Products
		fields = ['employee','product_name','image','image_url','description','gst_price','gst_percentage','hsn_sac','category','stock']


class ProductListSerializer(serializers.ModelSerializer):
	"""
	Serializer class for listing and detailing out product.
	"""
	class Meta:
		model = Products
		fields = ['slug','employee','product_name','image','image_url','description','gst_price','gst_percentage','hsn_sac','category','stock']


class CustomerCreateSerializer(serializers.ModelSerializer):
	"""
	Serializer class for creating and updating a customer.
	"""
	class Meta:
		model = Customers
		fields = ['customer_name', 'address', 'phone_number', 'customer_gst']

	def validate_phone_number(self, phone_number):
		numbers = ['+','-','0','1','2','3','4','5','6','7','8','9']
		for number in phone_number:
			if number not in numbers:
				raise serializers.ValidationError('The phone number is not valid.')
		return phone_number


class CustomerListSerializer(serializers.ModelSerializer):
	"""
	Serializer class for listing and detailing out customer.
	"""
	class Meta:
		model = Customers
		fields = ['slug', 'customer_name', 'address', 'phone_number', 'customer_gst']


class VehicleCreateSerializer(serializers.ModelSerializer):
	"""
	Serializer class for creating and updating a vehicle.
	"""
	class Meta:
		 model = Vehicles
		 fields = ['vehicle_name','vehicle_number','owner','driver','image','image_url']


class VehicleListSerializer(serializers.ModelSerializer):
	"""
	Serializer class for listing and detailing out vehicle.
	"""
	class Meta:
		 model = Vehicles
		 fields = ['slug','vehicle_name','vehicle_number','owner','driver','image','image_url']


class InvoiceCreateSerializer(serializers.ModelSerializer):
	"""
	Serializer class for creating and updating a invoice.
	"""
	customer = CustomerCreateSerializer()
	product = ProductCreateSerializer()
	vehicle = VehicleCreateSerializer()

	class Meta:
		model = Invoices
		fields = ['invoice_name','invoice_number','customer','product','vehicle']

	def create(self, validated_data):
		customer_data = validated_data.pop('customer')		
		customer_gst_number = customer_data['customer_gst']
		try:
			print('88888888888888')
			customer = Customers.objects.get(customer_gst=customer_gst_number)
		except:
			print('999999999999999999')
			customer = Customers.objects.create(**customer_data)
		product_data = validated_data.pop('product')		
		name_of_product = product_data['product_name']
		category_data = product_data.pop('category')
		category_name = category_data['name']
		try:
			print('777777777777777777')
			product = Products.objects.get(product_name=name_of_product)
		except:
			print('66666666666666666')
			try:
				category = Category.objects.get(name=category_name)
			except:
				category = Category.objects.create(**category_data)
			product = Products.objects.create(category=category.gid, **product_data)
		vehicle_data = validated_data.pop('vehicle')
		number_of_vehicle = vehicle_data['vehicle_number']
		try:
			print('44444444444444444444')
			vehicle = Vehicles.objects.get(vehicle_number=number_of_vehicle)
		except:
			print('33333333333333333333')
			vehicle = Vehicles.objects.create(**vehicle_data)			
		invoice = Invoices.objects.create(customer=customer.gid, product=product.gid, vehicle=vehicle.gid, **validated_data)
		return invoice


class InvoiceListSerializer(serializers.ModelSerializer):
	"""
	Serializer class for listing and detailing out invoice.
	"""
	class Meta:
		model = Invoices
		fields = ['slug','invoice_name','invoice_number','customer','product','vehicle']