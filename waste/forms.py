from django import forms


class ImageUploadFileForm(forms.Form):
    file = forms.ImageField()
