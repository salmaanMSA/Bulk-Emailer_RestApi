from rest_framework import serializers
from ..models import UserRegisteration
import re
from django.contrib.auth.password_validation import validate_password


class RegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegisteration
        fields = ['first_name', 'last_name', 'username', 'email_id', 'role', 'mobile_no', 'password']

    def validate_first_name(self, value):

        if value.isalpha()!=True:
            raise serializers.ValidationError('First Name Should Only contain Alphabets')

        elif value.isnumeric()==True:
            raise serializers.ValidationError('First Name Should Only contain Alphabets')

        return value

    def validate_last_name(self, value):

        if value.isalpha()!=True:
            raise serializers.ValidationError('Last Name should only contain Alphabets')

        elif value.isnumeric()==True:
            raise serializers.ValidationError('Last Name should only contain Alphabets')

        return value

    def validate_username(self, value):

        if value is None:
            raise serializers.ValidationError('Username cannot be Empty')

        elif value.isnumeric()==True:
            raise serializers.ValidationError('Username Cannot be Fully Integer')

        return value

    def validate_email_id(self, value):

        if value is None:
            raise serializers.ValidationError('Email-ID Cannot be Empty')

        elif not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",value):
            raise serializers.ValidationError('Email-ID Must be a Valid One')

        return value

    def validate_mobile_no(self,value):

        if value is None:
            raise serializers.ValidationError('Mobile Number Cannot be Empty')

        # elif not isinstance(value, int):
        #     raise serializers.ValidationError('Mobile Number should contain only numeric character')

        return value

    def validate_password(self, value):

        validate_password(value, self.instance)
        return value
