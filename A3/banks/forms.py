from django.forms import ModelForm
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from banks.models import Bank, Branch
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class BankForm(ModelForm):
    name = forms.CharField()
    swift_code = forms.CharField()
    description = forms.CharField()

    class Meta:
        model = Bank
        fields = ["name", "swift_code", "inst_num", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['swift_code'].required = False
        self.fields['inst_num'].required = False
        self.fields['description'].required = False

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        swift_code = cleaned_data.get("swift_code")
        inst_num = cleaned_data.get("inst_num")
        description = cleaned_data.get("description")

        if name == "":
            self.add_error("name", "This field is required")

        if swift_code == "":
            self.add_error("swift_code", "This field is required")

        if inst_num == "":
            self.add_error("inst_num", "This field is required")

        if description == "":
            self.add_error("description", "This field is required")

        return cleaned_data


class BranchForm(ModelForm):

    class Meta:
        model = Branch
        fields = ["name", "transit_num", "address", "email", "capacity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['transit_num'].required = False
        self.fields['address'].required = False
        self.fields['email'].required = False
        self.fields['capacity'].required = False

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        transit_num = cleaned_data.get("transit_num")
        address = cleaned_data.get("address")
        email = cleaned_data.get("email")
        capacity = cleaned_data.get("capacity")

        if name == "":
            self.add_error("name", "This field is required")

        if transit_num == "":
            self.add_error("transit_num", "This field is required")

        if address == "":
            self.add_error("address", "This field is required")

        if email == "":
            self.add_error("email", "This field is required")
        else:
            try:
                validate_email(email)
            except ValidationError:
                pass

        return cleaned_data
