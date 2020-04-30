from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterform,UserUpdateForm,ProfileUpdateForm
from . models import profile
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') #dictionary
            messages.success(request,f'account created for {username}')
            return redirect('login')

    else:
        form = UserRegisterform()
        messages.error(request,"please fill in the correct info")
    return render(request,'users/register.html',{'form':form})

@login_required()
def prof(request):
    if(request.method=='POST'):
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'your account has been updated successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'users/profile.html',context)
