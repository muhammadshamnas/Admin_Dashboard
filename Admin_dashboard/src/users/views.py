from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import UserRequest
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, redirect


class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/login.html", {})

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        # user = User.objects.filter(email=email, password=password)
        print()
        # user = authenticate(request, email=email, password=password)
        user = User.objects.get(email=email)
        if user.check_password(password):
            login(request, user)
            return redirect('/')
        # form is not valid or user is not authenticated
        return render(request, 'theme/login.html')





class RegisterView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/register.html", {})

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Check if the required fields are provided
        if not username or not password or not email:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)

        # Create the user
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        # Additional custom logic if needed

        return render(request, "theme/index.html", {})
        
        




class ForgotPasswordView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/forgot-password.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/forgot-password.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ChartsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/charts.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class TablesView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/tables.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/forgot-password.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ButtonsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/buttons.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class CardsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/cards.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class PageNotFoundView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/404.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class BlankView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/blank.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ColorsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-color.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class BordersView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-border.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class AnimationsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-animation.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class OthersView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-other.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})



class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "users/dashboard.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})

class UserRequestListSubmitView(APIView):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/user_request_form.html')

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        description = request.data.get('description')


        user_request = UserRequest()
        user_request.name = name
        user_request.user_id = request.user
        user_request.description = description
        user_request.status = False
        user_request.save()
    # Assign values to other fields 
        user_requests = UserRequest.objects.all()
        context = {'user_requests': user_requests}
        return render(request, 'users/user_request_list.html',context)

class UserRequestListView(TemplateView):
    template_name = 'users/user_request_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            user_requests = UserRequest.objects.all()
        else:
            user_requests = UserRequest.objects.filter(user_id=self.request.user.id)


        context['user_requests'] = user_requests
        return context

    def post(self, request, *args, **kwargs):
        request_id = request.POST.get('request_id')
        user_request = get_object_or_404(UserRequest, id=request_id)
        user_request.status = True
        user_request.save()
        user_requests = UserRequest.objects.all()
        context = {'user_requests': user_requests}
        return render(request, 'users/user_request_list.html',context)

