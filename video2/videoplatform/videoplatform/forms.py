from django import forms
from .models import *
from .utils import *

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

class UserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    videoFile = forms.FileField()
    thumbnailFile = forms.FileField()
    description = forms.CharField(max_length=1000, widget=forms.Textarea)


class SubscribeForm1(forms.Form):
    email = forms.EmailField()
    

class SubscribeForm2(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(SubscribeForm2, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                {'password': ["passwords don't match"]}
                
            )

class SubscribeForm3(forms.Form):
    password = forms.CharField()
    

class ChangeBannerForm(forms.Form):
    bannerFile = forms.FileField()

class ChangeProfilePhotoForm(forms.Form):
    bannerFile = forms.FileField()


class VideoEdit(forms.ModelForm):
    thumbnailFile = forms.FileField(required=False)

    class Meta:
        model = Video
        fields = ['title', 'description', 'thumbnailFile']
        widgets = {
            'description': forms.Textarea(),
        }

    def save(self, commit=True):
        print("SAVE--------")
        instance = super(VideoEdit, self).save(commit=False)
        creator_name = "Logan"
        if self.thumbnailFile:
            thumbnail_key = get_url(instance.title + creator_name + self.thumbnailFile.name)
            upload_s3(self.thumbnailFile, "thumbnails/" + thumbnail_key)
            instance.thumbnail = thumbnail_key
        instance.save()
        # self.
        # instance.course = self.course
        # instance.user = self.user
        # if commit:
        #     instance.save()
        return instance

