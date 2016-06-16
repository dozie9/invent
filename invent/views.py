from django.shortcuts import render, HttpResponse, HttpResponseRedirect, RequestContext, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import time, datetime
from .forms import *
from .models import *

# Create your views here.

def signup(request):
    form = SignForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        profile = form.cleaned_data['profile']
        state = form.cleaned_data['state']
        local = form.cleaned_data['local']
        try:
            user = User.objects.create_user(username,email,password)
            MemberType.objects.create(profile=profile,user=user)
            Location.objects.create(state=state,local_govt=local, user=user)
        except:
            pass
        return HttpResponse("<h3>Success</h3>")
    else:
        form = SignForm()

    return render_to_response('signup.html', locals(), RequestContext(request))

def logins(request):
    if request.user.is_active:
        check = MemberType.objects.get(user=request.user)
        if check.profile == "U":
            return UserHome(request)
        else:
            return SuperHome(request)
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                check = MemberType.objects.get(user=request.user)
                if check.profile == 'U':
                    return UserHome(request)
                else:
                    return SuperHome(request)
            else:
                return HttpResponse("Details found but not active")
        else:
            return HttpResponse("Username and Password invalid")

    return render_to_response('login.html', locals(), RequestContext(request))

@login_required()
def FirstUser(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        vol = form.cleaned_data['volume']
        per = form.cleaned_data['perLitre']
        amount = form.cleaned_data['amount']
        try:
            get = PerLitre.objects.get(user=request.user)
            get2 = Invent.objects.get(user=request.user)
            get.perLitre = per; get.date = datetime.date
            get2.invent = vol; get2.amount = amount; get2.date = datetime.date
            get.save(); get2.save()
        except:
            PerLitre.objects.create(perLitre=per, user=request.user)
            Invent.objects.create(invent=vol, amount=amount,user=request.user)
        return UserHome(request)
    else:
        form = UserForm(request.POST or None)

    return render_to_response('user/first.html', locals(), RequestContext(request))

@login_required()
def UserHome(request):
    time = datetime.datetime.now()
    try:
        get = Invent.objects.get(user=request.user)
    except:
        return FirstUser(request)
    openv = Invent.objects.get(user=request.user)
    per = PerLitre.objects.get(user=request.user)
    locate = Location.objects.get(user=request.user)
    his = History.objects.filter(locale=locate, date__gte=datetime.date.today()).order_by('date')
    form = SalesForms(request.POST or None)
    if request.POST:
        info = request.POST
        ids = info.values()
    else: ids = None
    if form.is_valid():
        litres = form.cleaned_data['litres']
        if ids[2] == "S":
            open = int(openv.invent)-int(litres)
            amount = int(litres)*int(per.perLitre)
            real = openv.amount+amount
            History.objects.create(total_volume=open,sold_volume=litres,total_amount=real,amount=amount,
                                   types=ids[2], date=datetime.time,locale=locate)
            openv.invent = open; openv.date = datetime.date; openv.amount = real
            openv.save()
        else:
            open = int(openv.invent)+(litres)
            amount = int(litres)*int(per.perLitre)
            real = openv.amount-amount
            History.objects.create(total_volume=open,sold_volume=litres,total_amount=real,amount=amount,
                                   types=ids[2], date=datetime.time,locale=locate)
            openv.invent = open; openv.date = datetime.date; openv.amount = real
            openv.save()
        return HttpResponseRedirect("../")
    else:
        form = SalesForms()
    return render_to_response('user/home.html', locals(), RequestContext(request))

@login_required()
def UserHistory(request):
    time = datetime.date.today()
    locate = Location.objects.get(user=request.user)
    his = History.objects.filter(locale=locate)
    return render_to_response('user/history.html', locals(), RequestContext(request))

def SuperHome(request):
    date = datetime.date.today()
    states = Location.objects.all()
    sales = History.objects.all()[:5]

    return render_to_response('super/home.html', locals(),RequestContext(request))

def SuperState(request,state):
    date = datetime.date.today()
    states = Location.objects.get(state=state)
    sales = History.objects.filter(locale=states)
    return render_to_response('super/state.html', locals(),RequestContext(request))

def Logout(request):
    logout(request)
    return HttpResponseRedirect("../")

