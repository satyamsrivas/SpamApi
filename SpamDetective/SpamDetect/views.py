from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import CharField, IntegerField,Value
from .models import CustomUser, Contact, Spam
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import json







@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone_number = data.get('phone_number')
        password = data.get('password')
        email = data.get('email')


        # Check if phone number already exists
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'error': 'Phone number already registered'})

        # Create a new user
        user = CustomUser.objects.create_user(phone_number=phone_number, password=password, name=name, email=email)

        return JsonResponse({'success': 'User registered successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    






@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        checkUser = authenticate(phone_number = phone_number, password= password)

        if checkUser is not None:
            login(request, checkUser)
            messages.success(request, 'Logged in successfully.')
            return HttpResponse('Logged in successfully.')
        else:
            messages.error(request, 'Invalid credentials.')
            return HttpResponse('Invalid credentials.')
    else:
        return HttpResponse('Please use the login form.')




@login_required
def user_logout(request):
    logout(request)
    # return redirect(reverse('signin'))




@login_required
@csrf_exempt
def mark_as_spam(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')

        # Mark the phone number as spam
        Spam.objects.create(number=phone_number)

        return JsonResponse({'success': 'Number marked as spam'})
    else:
        return JsonResponse({'error': 'Invalid request method'})







@csrf_exempt
def search_by_name(request):
    if request.method == 'GET':
        name = request.GET.get('name')

        if name is None:
            return JsonResponse({'error': 'Invalid name'})

        query = Q(name__istartswith=name)
        user_results = (
            CustomUser.objects.filter(query)
            .annotate(spam_likelihood=Value(0, output_field=IntegerField()))
            .annotate(full_name=Concat('name', Value(' '), output_field=CharField()))
            .values('id', 'name', 'spam_likelihood')
        )

        contact_results = (
            Contact.objects.filter(query)
            .annotate(spam_likelihood=Value(0, output_field=IntegerField()))
        )
        
        print(contact_results)
        if contact_results is not None:
            response = [
                {
                    'name': result['full_name'] if 'full_name' in result else result['name'],
                    'phone_number': result['phone_number'],
                    'spam_likelihood': result['spam_likelihood'],
                    'email': result['email'] if hasattr(result, 'email') else None
                }
                for result in user_results.union(contact_results)
            ]
            print(response)
            return JsonResponse(response, safe=False)
        else:
            return JsonResponse({'Error': 'User Not Found'})
    else:
        return JsonResponse({'error': 'Invalid request method'})








@login_required
def search_by_phone_number(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number')

        # Check if a registered user exists with the given phone number
        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if user:
            result = {
                'name': user.name,
                'phone_number': user.phone_number,
                'spam_likelihood': 0
            }
            print(result)
            return JsonResponse(result)

        # If no registered user is found, search for contacts with the given phone number
        contacts = Contact.objects.filter(phone_number=phone_number)
        results = [
            {'name': contact.name, 'phone_number': contact.phone_number, 'spam_likelihood': 0}
            for contact in contacts
        ]

        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'})








@login_required
def display_details(request):

    data = json.loads(request.body)
    phone_number = data.get('phone_number')
    
    if not phone_number:
        return JsonResponse({'error': 'Phone number is required.'}, status=400)
    
    user = CustomUser.objects.filter(phone_number=phone_number).first()
    
    if not user:
        return JsonResponse({'error': 'User not found.'}, status=404)

    # Check if the requesting user is in the contact list of the searched user
    is_in_contact_list = Contact.objects.filter(user=request.user, phone_number=user.phone_number).exists()

    result = {
        'name': user.name,
        'phone_number': user.phone_number,
        'spam_likelihood': 0
    }

    if request.user.is_authenticated and is_in_contact_list:
        result['email'] = user.email

    return JsonResponse(result)

