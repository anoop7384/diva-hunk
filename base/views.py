from django.shortcuts import render, redirect
from .models import Diva, Hunk, Voter
from .forms import VoterRegisterForm
from .email import sendEmailOTP
from itertools import chain

# Create your views here.


def home(request):
    divas = Diva.objects.all()
    hunks = Hunk.objects.all()
    context = {
        'divas': divas,
        'hunks': hunks
    }
    
    return render(request, 'base/home.html', context)


def divaHunkList(request):
    context = {
        'diva': [],
        'hunk': [],
        'message': "",
        'isdiva':False,
    }
    searchquery = request.GET.get('search')
    if searchquery!=None and searchquery!="":
        searchDiva=Diva.objects.filter(name__icontains=searchquery)
        searchHunk=Hunk.objects.filter(name__icontains=searchquery)
        if searchDiva:
            context.update(diva=searchDiva)
        elif searchHunk:
            context.update(hunk=searchHunk)
        else:
            context.update(message="No match found")
            return render(request, 'base/list.html',context)
    else:
        
        if("Hunk" in request.GET):
            results=Hunk.objects.all()
            context.update(hunk=results)
        else :
            results=Diva.objects.all() 
            context.update(diva=results)
            context.update(isdiva=True)
    
    return render(request, 'base/list.html',context)


def divaRegistration(request, pk):
    candidate = Diva.objects.get(pk=pk)
    context = {
        'type': "Diva",
        'candidate': candidate,
        'form': {},
        'message': "",
        'disabled':False,
        'name':'',
        'contactno':'',
        'email':'',
    }
    if (request.method == 'POST'):
        form = VoterRegisterForm(request.POST)
        if not form.is_valid():
            context.update(form=form,message='form is invalid')
            return render(request, 'base/register.html', context)
        context.update(form=form)
        # voter = form.save(commit=False)
        
        if 'sendOTP' in request.POST:
            voter = form.save(commit=False)
            find = Voter.objects.filter(email=voter.email)
            if (find.count() >= 1):
                if (find[0].diva):
                    context.update(message='Only one vote from one email')
                    return render(request, 'base/register.html', context)
            else:
                voter.save()
            sendEmailOTP(voter.email)
            context.update(message='OTP sent successfully')
            context.update(disabled='True')
            context.update(name=request.POST['name'])
            context.update(contactno=request.POST['contactno'])
            context.update(email=request.POST['email'])
            return render(request, 'base/register.html', context)

        if 'verify' in request.POST:
            email = request.POST['email']
            otp =  request.POST['otp_1']+request.POST['otp_2']+request.POST['otp_3']+request.POST['otp_4']

            find = Voter.objects.filter(email=email)
            if not find.exists():
                context.update(message='Email does not match')
                return render(request, 'base/register.html', context)

            if find[0].otp != otp:
                context.update(message='wrong otp')
                context.update(disabled='True')
                context.update(name=request.POST['name'])
                context.update(contactno=request.POST['contactno'])
                context.update(email=request.POST['email'])
                return render(request, 'base/register.html', context)
            
            candidate.votes+=1
            candidate.save()
            find.update(diva=candidate)
        return redirect('thanks')
    else:
        form = VoterRegisterForm()
    context.update(form=form)
    return render(request, 'base/register.html', context)


def hunkRegistration(request, pk):
    candidate = Hunk.objects.get(pk=pk)
    context = {
        'type': "Hunk",
        'candidate': candidate,
        'form': {},
        'message': "",
        'disabled':False,
        'name':'',
        'contactno':'',
        'email':'',
    }
    if (request.method == 'POST'):
        form = VoterRegisterForm(request.POST)
        if not form.is_valid():
            context.update(form=form,message='form is invalid')
            return render(request, 'base/register.html', context)
        context.update(form=form)
        #voter = form.save(commit=False)
        if 'sendOTP' in request.POST:
            voter = form.save(commit=False)
            find = Voter.objects.filter(email=voter.email)
            if (find.count() >= 1):
                if (find[0].hunk):
                    context.update(message='Only one vote from one email')
                    return render(request, 'base/register.html', context)
            else:
                voter.save()
            sendEmailOTP(voter.email)
            context.update(message='OTP sent successfully')
            context.update(disabled='True')
            context.update(name=request.POST['name'])
            context.update(contactno=request.POST['contactno'])
            context.update(email=request.POST['email'])
            return render(request, 'base/register.html', context)

        if 'verify' in request.POST:
            email = request.POST['email']
            otp =  request.POST['otp_1']+request.POST['otp_2']+request.POST['otp_3']+request.POST['otp_4']
            
            find = Voter.objects.filter(email=email)
            if not find.exists():
                context.update(message='Email dose not match')
                return render(request, 'base/register.html', context)

            if find[0].otp != otp:
                context.update(message='wrong otp')
                context.update(message='OTP sent successfully')
                context.update(disabled='True')
                context.update(name=request.POST['name'])
                context.update(contactno=request.POST['contactno'])
                context.update(email=request.POST['email'])
                return render(request, 'base/register.html', context)
            
            candidate.votes+=1
            candidate.save()
            find.update(hunk=candidate)
        return redirect('thanks')
    else:
        form = VoterRegisterForm()
    context.update(form=form)
    return render(request, 'base/register.html', context)

def thanksdiva(request):
    return render(request, 'base/thanks_diva.html')

def thankshunk(request):
    return render(request, 'base/thanks_hunk.html')