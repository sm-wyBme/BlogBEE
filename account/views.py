import profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from account.models import Account
from django.conf import settings
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, AccountImageForm
from base.models import Blog

from django.core.files.storage import default_storage, FileSystemStorage
import os
import cv2
import json
import base64 #convert image to base64 format
# import requests
from django.core import files

TEMP_PROFILE_IMAGE_NAME = 'temp_profile_image.png' #Temporary cache image

#register user
def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        context = {'message': f'You are already authenticated as {user.email}' }
        return render(request, 'message.html', context)

    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email = email, password = raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form


    return render(request, 'account/register.html', context)

#login user
def login_view(request, *args, **kwargs):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect('home')
        else:
            context['login_form'] = form
    
    return render(request, 'account/login.html', context)

#logout
def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('home')

#user profile
def user_profile(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    try:
        user = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        context = {'message': 'Account does not exist'}
        return render(request, 'message.html', context)

    context['user'] = user

    blogs = user.blog_set.all()
    context['blogs'] = blogs
    return render(request, 'account/user-profile.html', context)

#edit account view
@login_required(login_url='login')
def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = kwargs.get('user_id')
    try:
        account = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        context = {'message': 'Something went wrong' }
        return render(request, 'message.html', context)
        
    if account.pk != request.user.pk:
        context = {'message': 'You are not allowed to update this account' }
        return render(request, 'message.html', context)

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user, request=request) #request.FILES is needed for image files
        if form.is_valid():
            # delete old profile image so the name is preserved
            # account.profile_image.delete()
            form.save()
            return redirect('account:view', user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user, request=request, initial = {
                    'id': account.pk,
                    'email': account.email,
                    'username': account.username,
                    'bio' : account.bio,
                    'name': account.name,
                    # 'profile_image': account.profile_image,
                    'hide_email': account.hide_email,
                }
            )
            context['form'] = form
            
    else: #loading the page for the first time
        form = AccountUpdateForm(request= request, initial = {
                'id': account.pk,
                'email': account.email,
                'username': account.username,
                'bio': account.bio,
                'name': account.name,
                # 'profile_image': account.profile_image,
                'hide_email': account.hide_email,
            }
        )
        context['form'] = form
    
    context['user'] = account# context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE    #maximum image size
    return render(request, 'account/update-account.html', context)


#update profile image with
def update_profile_image(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = kwargs.get('user_id')
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        context = {'message': 'You are not allowed to update this account' }
        return render(request, 'message.html', context)
    
    context = {}

    if request.method == 'POST':
        form = AccountImageForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            # account.profile_image.delete()
            form.save()
            return redirect('account:view', user_id=account.pk)
        else:
            form = AccountImageForm ( request.POST, instance=request.user, 
                initial = {
                    "id": account.pk,
                    "profile_image": account.profile_image
                }
            )
            context['form'] = form
    else:
        form = AccountImageForm(
                initial = {
                    "id": account.pk,
                    "profile_image": account.profile_image
                }
            )
        context['form'] = form

    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'account/edit-profile-pic.html', context)


def save_temp_profile_image_from_base64String(imageString, user):
	INCORRECT_PADDING_EXCEPTION = "Incorrect padding" #stackoverflow lookit up (exception)
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
			os.mkdir(settings.TEMP + "/" + str(user.pk))
		url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_PROFILE_IMAGE_NAME)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imageString)
		with storage.open('', 'wb+') as destination: #write image to the local storage
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		# workaround for an issue (padding info may get lost durinf encoding and decoding)
        # https://stackoverflow.com/questions/40729276/base64-incorrect-padding-error-using-python
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4) #adding a fix
			return save_temp_profile_image_from_base64String(imageString, user)
	return None


def crop_image(request, *args, **kwargs):
	payload = {}
	user = request.user
	if request.POST and user.is_authenticated:
		try:
			imageString = request.POST.get("image") #encode image to the base64 version and send it for cropping
			url = save_temp_profile_image_from_base64String(imageString, user) #save locally on the server
			img = cv2.imread(url)

            #type convertion
			cropX = int(float(str(request.POST.get("cropX"))))
			cropY = int(float(str(request.POST.get("cropY"))))
			cropWidth = int(float(str(request.POST.get("cropWidth"))))
			cropHeight = int(float(str(request.POST.get("cropHeight"))))
			if cropX < 0:
				cropX = 0
			if cropY < 0: # There is a bug with cropperjs. x, y can be negative.
				cropY = 0
			crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth] #opencv crop function

			cv2.imwrite(url, crop_img)

			# delete the old image
			user.profile_image.delete()

			# Save the cropped image to user model
			user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
			user.save()

			payload['result'] = "success"
			payload['cropped_profile_image'] = user.profile_image.url

			# delete temp file
			os.remove(url)

		except Exception as e:
			print("exception: " + str(e))
			payload['result'] = "error"
			payload['exception'] = str(e)
	return HttpResponse(json.dumps(payload), content_type="application/json")