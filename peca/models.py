# -*- encoding: utf-8 -*-
import re
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from cStringIO import StringIO
import os

IMAGE_SIZES = { 'img_principal' 	: (531, 400),
                'thumb_g' 			: (184, 184),
                'thumb_p' 			: (92, 92) }

class Peca(models.Model):

	TIPO_CONTEUDO = (
        ('I', 'Imagem'),
        ('V', 'Video'),
    )

	nome 					= models.CharField(u'Nome da peça',max_length=100)
	txt_principal			= models.TextField(u'Texto da peça')
	txt_thumb_g 			= models.CharField(u'Texto da thumb grande', max_length=100)
	txt_thumb_p 			= models.CharField(u'Texto da thumb pequena', max_length=100)
	url_video 				= models.URLField(u'Url do video', max_length=100)
	img_principal			= models.ImageField(u'Imagem Principal', upload_to='original/%Y/%m/', max_length=100)
	thumb_g 			 	= models.ImageField(u'Thumb grande', upload_to='thumb_g/%Y/%m/',max_length=100, null=True)
	thumb_p 		 		= models.ImageField(u'Thumb pequena', upload_to='thumb_p/%Y/%m/',max_length=100, null=True)
	tipo_conteudo 			= models.CharField(u'Tipo', max_length=2, choices=TIPO_CONTEUDO)
	created_at 				= models.DateTimeField(u'Criado em', auto_now = True)
	publicado_por 			= models.ForeignKey(User, null=True, blank=True)
	slug					= models.SlugField(max_length=100, blank=True, unique=True)

	def __unicode__(self):
		return self.nome
		
	class Meta():
		verbose_name = u'Peça'
    	verbose_name_plural = u'Peças'

	def save(self):
		if self.img_principal:
			image = Image.open(self.img_principal)
			if image.mode not in ('L', 'RGB'):
				image = image.convert('RGB')
	        # for field_name, size in IMAGE_SIZES.iteritems():
	        # field = getattr(self, field_name)
	        temp_handle = StringIO()

	        img_tmp = image.resize(IMAGE_SIZES['img_principal'], Image.ANTIALIAS)
	    	img_tmp.save(temp_handle, 'png')
	    	temp_handle.seek(0)
	    	suf = SimpleUploadedFile(os.path.split(self.img_principal.name)[-1], temp_handle.read(), content_type='image/png')
	        self.img_principal.save(suf.name, suf, save=False)

	        img_tmp = image.resize(IMAGE_SIZES['thumb_g'], Image.ANTIALIAS)
	        temp_handle = StringIO()
	    	img_tmp.save(temp_handle, 'png')
	    	temp_handle.seek(0)
	    	suf = SimpleUploadedFile(os.path.split(self.img_principal.name)[-1], temp_handle.read(), content_type='image/png')
	        self.thumb_g.save(suf.name, suf, save=False)

	        img_tmp = image.resize(IMAGE_SIZES['thumb_p'], Image.ANTIALIAS)
	        temp_handle = StringIO()
	    	img_tmp.save(temp_handle, 'png')
	    	temp_handle.seek(0)
	    	suf = SimpleUploadedFile(os.path.split(self.img_principal.name)[-1], temp_handle.read(), content_type='image/png')
	        self.thumb_p.save(suf.name, suf, save=False)
		if False:
			pass
		else:
			super(Peca, self).save()

			
# SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify

def peca_pre_save(signal, instance, sender, **kwargs):
	if not instance.slug:
		slug = slugify(instance.nome)
		novo_slug = slug 
		contador = 0
		while Peca.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
			contador += 1
			novo_slug = '%s-%d' % (slug, contador)
		instance.slug = novo_slug
signals.pre_save.connect(peca_pre_save, sender=Peca) 
	
		
