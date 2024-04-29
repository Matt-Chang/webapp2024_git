from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Points, PointsTransfer, PaymentRequest,UserProfile

class PointsInline(admin.TabularInline):
    model = Points
    can_delete = False
    verbose_name_plural = 'points'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PointsInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Points)
admin.site.register(PointsTransfer)
admin.site.register(PaymentRequest)
admin.site.register(UserProfile)


from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile
from django import forms

class UserAdminForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['bio'].initial = self.instance.userprofile.bio

    def save(self, commit=True):
        user = super(UserAdminForm, self).save(commit=False)
        if commit:
            user.save()
            user.userprofile.bio = self.cleaned_data['bio']
            user.userprofile.save()
        return user

class CustomUserAdmin(BaseUserAdmin):
    form = UserAdminForm
    add_form = UserAdminForm

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('bio',)}),
    )

