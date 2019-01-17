from django.forms import ModelForm

from reg_log.models import Users


class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = (
            'uid',
            'name',
            'tel',
            'pwd',
        )