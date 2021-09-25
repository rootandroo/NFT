from .models import Collection
from django import forms
from .services import is_policy_id
from django.core.exceptions import ValidationError



class PopulateForm(forms.Form):
    name = forms.CharField(label='Project Name', max_length=56)
    policy_id = forms.CharField(widget=forms.Textarea)

    def clean(self):
        error = []
        cleaned_data = super().clean()
        policy_id_list = cleaned_data.get('policy_id').split()
        name = cleaned_data.get('name')

        for policy_id in policy_id_list:            
            if not is_policy_id(policy_id):
                error.append(f'Invalid policy_id: {policy_id}')
            elif Collection.objects.filter(policy_id=policy_id).exists():
                error.append(f'Policy_id already exists: {policy_id}')

        if error:
            raise(ValidationError(error))
        else:
            return {'name': name, 'policy_id_list': policy_id_list}