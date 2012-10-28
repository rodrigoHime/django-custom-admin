#! -*- encoding:utf-8 -*- 
from django.contrib import admin
from forms import *
# from django.http import HttpResponse, Http404
# from django.core.exceptions import ValidationError
# from models import *


class PecaAdmin(admin.ModelAdmin):

	list_display = ('created_at','nome', 'publicado_por',)
	search_fields = ('nome', 'publicado_por',)
	# list_filter = ('nome', 'created_at',)
	form = PecaAdminForm

	def save_model(self, request, obj, form, change):

		if not change:
			obj.publicado_por = request.user
		obj.save()

admin.site.register(Peca, PecaAdmin)