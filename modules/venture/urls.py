from django.urls import path
from modules.venture import views

app_name = 'venture'

urlpatterns = [
	path('create_organisation/',
		views.CreateOrganisation.as_view(),
		name='create_organisation'),
	path('organisation_list/',
		views.OrganisationList.as_view(),
		name='organisation_list'),
	path('organisation_detail/<slug:slug>',
		views.OrganisationDetail.as_view(),
		name='organisation_detail'),
	path('update_organisation/<slug:slug>',
		views.UpdateOrganisation.as_view(),
		name='update_organisation'),
	path('delete_organisation/<slug:slug>',
		views.DeleteOrganisation.as_view(),
		name='delete_organisation'),
]
