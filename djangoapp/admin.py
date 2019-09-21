# email for admin site is : user@email.com
# password for admin site is: adminpass
# username : swagdaddy

from django.contrib import admin
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from djangoapp.models import MyUser



# to register the custom user model
class UserCreationForm(forms.ModelForm):
    """
        A form for creating all the users. includes a required field plus a repeated password
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'phone_num' ,'email', 'date_of_birth')

    def clean_password2(self):
        """
        Check that the two password entries match
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("passwords don't match")
        return password2
    
    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    for updating users. Includes all the fields but replaces
    the password field with admin's password hash display field
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'phone_num', 'email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        # regardless of what the user provides, return the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'phone_num', 'email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('phone_num', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_num', 'email', 'date_of_birth', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new user admin
admin.site.register(MyUser, UserAdmin)
# and since we are not using django's built-in permissions, unregister the group model from admin
admin.site.unregister(Group)
