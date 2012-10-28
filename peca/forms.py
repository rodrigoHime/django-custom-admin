#! -*- encoding:utf-8 -*- 
import re
from django import forms
from models import *

URL_PATTERN = re.compile(r'^(http[s]?://www\.youtube\.com/watch\?v='
						r'|http[s]?://youtu\.be/)([-a-z0-9A-Z_]+)')

class PecaAdminForm(forms.ModelForm):

    class Meta:
        model = Peca
        exclude = ('publicado_por', 'thumb_g', 'thumb_p',)

    def clean_url_video(self):
	    match = re.match(URL_PATTERN, self.cleaned_data.get('url_video', None))
	    if match:
	    	# print match.groups()[1]
	    	return self.cleaned_data['url_video']
	    else:
	    	raise forms.ValidationError("A URL informada não é do YouTube")