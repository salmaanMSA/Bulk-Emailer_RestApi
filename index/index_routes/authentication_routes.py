from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..index_serializers.register_serializers import RegisterationSerializer
from ..index_models.customUser_models import CustomUser
from ..index_models.register_models import UserRegisteration
from rest_framework import status
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from ..utils import token_generator
from django.core.mail import EmailMessage
from django.views import View


@api_view(['POST'])
def registeration(request):

    serializer = RegisterationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        email = data["email_id"]
        password = data["password"]
        res = {'msg': 'Data Created Successfully and Please Check Your Registered EmailID For Account Validation'}

        user = UserRegisteration.objects.get(email_id=email)

        custom_user = CustomUser.objects.create_user(user_id=user ,email=email, password=password)

        """
            Generating token for link 
        """
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

        """
            Sending Email to the Registered User for Account Validation 
        """
        activate_url = 'http://' + domain + link
        email_subject = "Activate Your Account"
        email_body = 'Hello' + '' + user.first_name + '' \
                                                      '\nPlease use this link to verify your Account\n' + activate_url
        email = EmailMessage(
            email_subject,
            email_body,
            'noreply@semycolon.com',
            [email],
        )
        email.send(fail_silently=False)

        return Response(res, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_profile(request, id):

    records = UserRegisteration.objects.get(id=id)

    serializers = RegisterationSerializer(records, many=False)

    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_profile(request, id):

    rec = UserRegisteration.objects.get(id=id)

    serializers = RegisterationSerializer(instance=rec, data=request.data)

    if serializers.is_valid():
        serializers.save()
        x = {'msg':'Records Updated Successfully'}
        return Response(x, status=status.HTTP_201_CREATED)

    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_profile(request, id):

    rec= UserRegisteration.objects.get(id=id)
    rec.delete()

    return Response("Record Deleted Sucessfully")


class VerificationView(View):

    def get(self, request, uidb64, token):

        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user =UserRegisteration.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login' + '?message=' + 'User Already Activated')
            """
                If User is Active then Redirecting the User to Login Page
            """
            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            #messages.success(request, 'Account Activated Successfully')
            return redirect('login')

        except Exception as e:
            pass

        return redirect('login')

def login(request):
    return render(request, 'login.html')