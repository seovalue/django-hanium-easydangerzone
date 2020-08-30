from django import forms

# -*- coding: utf-8 -*-

class UploadDocumentForm(forms.Form):
    file = forms.FileField()