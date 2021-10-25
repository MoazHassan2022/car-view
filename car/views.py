from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from urllib.parse import urlparse, parse_qs
import re
import unittest
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, InvalidPage

def home(request):
    return render(request, "home.html")


def add(request):
    videoID = ""
    if request.method == 'GET':
        return render(request, "add.html")
    elif request.method == 'POST':
        x = request.POST
        name = x["name"]
        cars = Car.objects.all()
        found = False
        for ca in cars:
            if ca.name == name:
                found = True
        if found:
            return render(request, "add.html", {"message":"هذا الاسم موجود من قبل"})
        video = x["video_url"]
        image = request.POST['image']
        logo = request.POST['logo']
        details = x["details"]
        flaws = x["flaws"]
        date1 = x["date"]
        motorSt = x["motorSt"]
        price = x["price"]
        if price == "":
            price = 0
        modelText = x["modelText"]
        sortText = x["sortText"]
        models = CarModel.objects.all()
        sorts = Sort.objects.all()
        modelNotFound = True
        sortNotFound = True
        for m in models:
            if m.modelText.lower() == modelText.lower():
                modelNotFound = False
        for s in sorts:
            if s.sortText.lower() == sortText.lower():
                sortNotFound = False
        if modelNotFound:
            if modelText:
                m = CarModel(modelText=modelText)
                m.save()
        if sortNotFound:
            if sortText:
                s = Sort(sortText=sortText)
                s.save()

        if video:
            r = re.compile('(?:(?:https?\:\/\/)?(?:www\.)?(?:youtube|youtu)(?:(?:\.com|\.be)\/)(?:embed\/)?(?:watch\?)?(?:feature=player_embedded)?&?(?:v=)?([0-z]{11}|[0-z]{4}(?:\-|\_)[0-z]{4}|.(?:\-|\_)[0-z]{9}))')
            videoID = r.match(video).groups()[0]
        c = Car(name=name, video=video, image=image, details=details, videoID=videoID, date=date1, flaws=flaws, logo=logo, motorSt=motorSt, price=price, modelText=modelText, sortText=sortText)
        c.save()
        return render(request, "add.html")


def edit(request, id):
    c = Car.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST
        cars = Car.objects.all()
        if r.get('name') != '':
            found = False
            for ca in cars:
                if (ca.name == r.get('name')) and (ca.id != id):
                    found = True
            if found:
                return HttpResponseRedirect("../../list-admin")
            c.name = r.get('name')
        if r.get('details') != '':
            c.details = r.get('details')
        if r.get('image') != '':
            c.image = r.get('image')
        if r.get('logo') != '':
            c.logo = r.get('logo')
        if r.get('video_url') != '':
            c.video = r.get('video_url')
            rv = re.compile('(?:(?:https?\:\/\/)?(?:www\.)?(?:youtube|youtu)(?:(?:\.com|\.be)\/)(?:embed\/)?(?:watch\?)?(?:feature=player_embedded)?&?(?:v=)?([0-z]{11}|[0-z]{4}(?:\-|\_)[0-z]{4}|.(?:\-|\_)[0-z]{9}))')
            c.videoID = rv.match(c.video).groups()[0]
        if r.get('date') != '':
            c.date = r.get('date')
        if r.get('flaws') != '':
            c.flaws = r.get('flaws')
        if r.get('motorSt') != '':
            c.motorSt = r.get('motorSt')
        if r.get('price') != '':
            c.price = r.get('price')
        if r.get('modelText') != '':
            modelText = r.get('modelText')
            models = CarModel.objects.all()
            modelNotFound = True
            for m in models:
                if m.modelText.lower() == modelText.lower():
                    modelNotFound = False
            if modelNotFound:
                if modelText:
                    if c.modelText:
                        n = CarModel.objects.get(modelText=c.modelText)
                        n.delete()
                    m = CarModel(modelText=modelText)
                    m.save()
            c.modelText = modelText
        if r.get('sortText') != '':
            sortText = r.get('sortText')
            sorts = Sort.objects.all()
            sortNotFound = True
            for s in sorts:
                if s.sortText.lower() == sortText.lower():
                    sortNotFound = False
            if sortNotFound:
                if sortText:
                    s = Sort(sortText=sortText)
                    s.save()
            c.sortText = sortText

        c.save()
        return HttpResponseRedirect("../../list-admin")
    elif request.method == 'GET':
        return render(request, "edit.html", {
            "car": c
        })


def delete(request, id):
    c = Car.objects.get(id=id)
    c.delete()
    return HttpResponseRedirect("../../list-admin")


def list_cars_admin(request):
    cars = Car.objects.all()
    allModels = CarModel.objects.order_by('modelText')
    allSorts = Sort.objects.order_by('sortText')
    if request.method == 'GET':
        paginator = Paginator(cars, 150)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            cars1 = paginator.page(page)
        except(EmptyPage, InvalidPage):
            cars1 = paginator.page(paginator.num_pages)
        return render(request, "listAdmin.html", {
            "cars": cars1,
            "models":allModels,
            "sorts":allSorts
        })

    elif request.method == 'POST':
        motorSt = request.POST["motorSt"]
        search = request.POST["search"]
        model = request.POST["model"]
        sort = request.POST["sort"]
        date = request.POST["date"]
        if motorSt:
            carsMotors = []
            if search:
                if model:
                    if sort:
                        if date:
                            for c in cars:
                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()) and (date == c.date):
                                    carsMotors.append(c)
                        else:
                            for c in cars:
                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)
                    else:
                        if date:
                            for c in cars:
                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()) and (date == c.date):
                                    carsMotors.append(c)
                        else:
                            for c in cars:
                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()):
                                    carsMotors.append(c)
                else:
                    if date:
                        if sort:
                            for c in cars:
                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        sort.lower() == c.sortText.lower()) and (date == c.date):
                                    carsMotors.append(c)
                        else:
                            for c in cars:
                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (date == c.date):
                                    carsMotors.append(c)
                    else:
                        if sort:
                            for c in cars:
                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)
                        else:
                            for c in cars:
                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()):
                                    carsMotors.append(c)
            else:
                if model:
                    if date:
                        if sort:
                            for c in cars:
                                if (motorSt == c.motorSt) and (sort.lower() == c.sortText.lower()) and (date == c.date) and (
                                        model.lower() == c.modelText.lower()):
                                    carsMotors.append(c)
                        else:
                            for c in cars:
                                if (motorSt == c.motorSt) and (model.lower() == c.modelText.lower()) and (date == c.date):
                                    carsMotors.append(c)
                    else:
                        if sort:
                            for c in cars:
                                if (motorSt == c.motorSt) and (model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)
                        else:
                            for c in cars:
                                if (motorSt == c.motorSt) and (model.lower() == c.modelText.lower()):
                                    carsMotors.append(c)
                else:
                    if date:
                        if sort:
                            for c in cars:
                                if (motorSt == c.motorSt) and (sort.lower() == c.sortText.lower()) and (date == c.date):
                                    carsMotors.append(c)
                        else:
                            for c in cars:
                                if (motorSt == c.motorSt) and (date == c.date):
                                    carsMotors.append(c)
                    else:
                        if sort:
                            for c in cars:
                                if (motorSt == c.motorSt) and (sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)
                        else:
                            for c in cars:
                                if motorSt == c.motorSt:
                                    carsMotors.append(c)
            paginator = Paginator(carsMotors, 150)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "listAdmin.html", {
                "cars": cars1,
                "models": allModels,
                "sorts": allSorts
            })
        elif search:
            carSearch = []
            if model:
                if sort:
                    if date:
                        for c in cars:
                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()) and (
                                    sort.lower() == c.sortText.lower()) and (date == c.date):
                                carSearch.append(c)
                    else:
                        for c in cars:
                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()):
                                carSearch.append(c)
                else:
                    if date:
                        for c in cars:
                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()) and (date == c.date):
                                carSearch.append(c)
                    else:
                        for c in cars:
                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()):
                                carSearch.append(c)
            else:
                if date:
                    if sort:
                        for c in cars:
                            if (search.lower() in c.name.lower()) and (sort.lower() == c.sortText.lower()) and (date == c.date):
                                carSearch.append(c)
                    else:
                        for c in cars:
                            if (search.lower() in c.name.lower()) and (date == c.date):
                                carSearch.append(c)
                else:
                    if sort:
                        for c in cars:
                            if (search.lower() in c.name.lower()) and (sort.lower() == c.sortText.lower()):
                                carSearch.append(c)
                    else:
                        for c in cars:
                            if search.lower() in c.name.lower():
                                carSearch.append(c)
            paginator = Paginator(carSearch, 150)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "listAdmin.html", {
                "cars": cars1,
                "models": allModels,
                "sorts": allSorts
            })
        elif model:
            carsModels = []
            if sort:
                if date:
                    for c in cars:
                        if (model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()) and (date == c.date):
                            carsModels.append(c)
                else:
                    for c in cars:
                        if (model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()):
                            carsModels.append(c)
            else:
                if date:
                    for c in cars:
                        if (model.lower() == c.modelText.lower()) and (date == c.date):
                            carsModels.append(c)
                else:
                    for c in cars:
                        if model.lower() == c.modelText.lower():
                            carsModels.append(c)
            paginator = Paginator(carsModels, 150)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "listAdmin.html", {
                "cars": cars1,
                "models": allModels,
                "sorts": allSorts
            })
        elif sort:
            carsSorts = []
            if date:
                for c in cars:
                    if (sort.lower() == c.sortText.lower()) and (date == c.date):
                        carsSorts.append(c)
            else:
                for c in cars:
                    if sort.lower() == c.sortText.lower():
                        carsSorts.append(c)
            paginator = Paginator(carsSorts, 150)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "listAdmin.html", {
                "cars": cars1,
                "models": allModels,
                "sorts": allSorts
            })
        elif date:
            carsDate = Car.objects.filter(date=date).all()
            paginator = Paginator(carsDate, 150)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "listAdmin.html", {
                "cars": cars1,
                "models": allModels,
                "sorts": allSorts
            })
        else:
            empty = []
            return render(request, "listAdmin.html", {
                "cars": empty,
                "models": allModels,
                "sorts": allSorts
            })


def carPage(request, id):
    exists = False
    c = Car.objects.get(id=id)
    comments = c.commentList.all()
    if request.user.is_authenticated:
        fav = request.user.favList.all()
        for ca in fav:
            if ca.id == id:
                exists = True

    ads = c.ads.all()
    return render(request, "view.html", {
        "car":c,
        "ads":ads,
        "exists":exists,
        "comments":comments
    })


def list_cars(request):
    cars = Car.objects.all()
    allModels = CarModel.objects.order_by('modelText')
    allSorts = Sort.objects.order_by('sortText')
    v = View.objects.get(id=1)
    v.viewsCount += 1
    v.save()
    paginator = Paginator(cars, 150)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        cars1 = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cars1 = paginator.page(paginator.num_pages)
    if request.method == 'GET':
        return render(request, "list.html", {
            "cars": cars1,
            "models":allModels,
            "sorts":allSorts,
            "viewsCount":v.viewsCount
        })


    elif request.method == 'POST':

        motorSt = request.POST["motorSt"]

        search = request.POST["search"]

        model = request.POST["model"]

        sort = request.POST["sort"]

        date = request.POST["date"]

        if motorSt:

            carsMotors = []

            if search:

                if model:

                    if sort:

                        if date:

                            for c in cars:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()) and (
                                        sort.lower() == c.sortText.lower()) and (date == c.date):
                                    carsMotors.append(c)

                        else:

                            for c in cars:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)

                    else:

                        if date:

                            for c in cars:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()) and (date == c.date):
                                    carsMotors.append(c)

                        else:

                            for c in cars:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()):
                                    carsMotors.append(c)

                else:

                    if date:

                        if sort:

                            for c in cars:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        sort.lower() == c.sortText.lower()) and (date == c.date):
                                    carsMotors.append(c)

                        else:

                            for c in cars:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (date == c.date):
                                    carsMotors.append(c)

                    else:

                        if sort:

                            for c in cars:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)

                        else:

                            for c in cars:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()):
                                    carsMotors.append(c)

            else:

                if model:

                    if date:

                        if sort:

                            for c in cars:

                                if (motorSt == c.motorSt) and (sort.lower() == c.sortText.lower()) and (
                                        date == c.date) and (
                                        model.lower() == c.modelText.lower()):
                                    carsMotors.append(c)

                        else:

                            for c in cars:

                                if (motorSt == c.motorSt) and (model.lower() == c.modelText.lower()) and (
                                        date == c.date):
                                    carsMotors.append(c)

                    else:

                        if sort:

                            for c in cars:

                                if (motorSt == c.motorSt) and (model.lower() == c.modelText.lower()) and (
                                        sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)

                        else:

                            for c in cars:

                                if (motorSt == c.motorSt) and (model.lower() == c.modelText.lower()):
                                    carsMotors.append(c)

                else:

                    if date:

                        if sort:

                            for c in cars:

                                if (motorSt == c.motorSt) and (sort.lower() == c.sortText.lower()) and (date == c.date):
                                    carsMotors.append(c)

                        else:

                            for c in cars:

                                if (motorSt == c.motorSt) and (date == c.date):
                                    carsMotors.append(c)

                    else:

                        if sort:

                            for c in cars:

                                if (motorSt == c.motorSt) and (sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)

                        else:

                            for c in cars:

                                if motorSt == c.motorSt:
                                    carsMotors.append(c)

            paginator = Paginator(carsMotors, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        elif search:

            carSearch = []

            if model:

                if sort:

                    if date:

                        for c in cars:

                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()) and (
                                    sort.lower() == c.sortText.lower()) and (date == c.date):
                                carSearch.append(c)

                    else:

                        for c in cars:

                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()) and (
                                    sort.lower() == c.sortText.lower()):
                                carSearch.append(c)

                else:

                    if date:

                        for c in cars:

                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()) and (
                                    date == c.date):
                                carSearch.append(c)

                    else:

                        for c in cars:

                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()):
                                carSearch.append(c)

            else:

                if date:

                    if sort:

                        for c in cars:

                            if (search.lower() in c.name.lower()) and (sort.lower() == c.sortText.lower()) and (
                                    date == c.date):
                                carSearch.append(c)

                    else:

                        for c in cars:

                            if (search.lower() in c.name.lower()) and (date == c.date):
                                carSearch.append(c)

                else:

                    if sort:

                        for c in cars:

                            if (search.lower() in c.name.lower()) and (sort.lower() == c.sortText.lower()):
                                carSearch.append(c)

                    else:

                        for c in cars:

                            if search.lower() in c.name.lower():
                                carSearch.append(c)

            paginator = Paginator(carSearch, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        elif model:

            carsModels = []

            if sort:

                if date:

                    for c in cars:

                        if (model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()) and (
                                date == c.date):
                            carsModels.append(c)

                else:

                    for c in cars:

                        if (model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()):
                            carsModels.append(c)

            else:

                if date:

                    for c in cars:

                        if (model.lower() == c.modelText.lower()) and (date == c.date):
                            carsModels.append(c)

                else:

                    for c in cars:

                        if model.lower() == c.modelText.lower():
                            carsModels.append(c)

            paginator = Paginator(carsModels, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        elif sort:

            carsSorts = []

            if date:

                for c in cars:

                    if (sort.lower() == c.sortText.lower()) and (date == c.date):
                        carsSorts.append(c)

            else:

                for c in cars:

                    if sort.lower() == c.sortText.lower():
                        carsSorts.append(c)

            paginator = Paginator(carsSorts, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        elif date:

            carsDate = Car.objects.filter(date=date).all()

            paginator = Paginator(carsDate, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        else:

            empty = []

            return render(request, "list.html", {

                "cars": empty,

                "models": allModels,

                "sorts": allSorts

            })

def authorize(request):
    if request.method == "GET":
        return render(request, "authorize.html")

    elif request.method == "POST":
        admin = request.POST["password"]
        if admin == "belal1234":
            return HttpResponseRedirect("list-admin")
        else:
            return render(request, "authorize.html", {"message": "كلمة سر خاطئة"})


def authorizeAdd(request):
    if request.method == "GET":
        return render(request, "authorizeAdd.html")

    elif request.method == "POST":
        admin = request.POST["password"]
        if admin == "belal1234":
            return HttpResponseRedirect("add")
        else:
            return render(request, "authorizeAdd.html", {"message": "كلمة سر خاطئة"})

def AdName(request):
    allCars = Car.objects.all()
    if request.method == "POST":
        name = request.POST["name"]
        cars = Car.objects.filter(name=name)
        return render(request, "date of Ad.html", {"cars":cars, "name":name})
    elif request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "AdName.html", {"cars":allCars})
        else:
            return HttpResponseRedirect(reverse("login"))

def AdDate(request, name):
    if request.method == "POST":
        date = request.POST["date"]
        c = Car.objects.get(name=name, date=date)
        return render(request, "rest of Ad.html", {"car":c})

def AdRest(request, id):
    c = Car.objects.get(id=id)
    ads = c.ads.all()

    if request.method == "POST":
        videoID = ""
        video = request.POST["video_url"]
        image = request.POST["image"]
        image1 = request.POST["image1"]
        image2 = request.POST["image2"]
        image3 = request.POST["image3"]
        image4 = request.POST["image4"]
        country = request.POST["country"]
        mobile = request.POST["mobile"]
        advertiser = request.POST["advertiser"]
        paymentWay = request.POST["paymentWay"]
        carColor = request.POST["carColor"]
        status = request.POST["status"]
        fuel = request.POST["fuel"]
        driver = request.POST["driver"]
        price = request.POST["price"]
        if price == "":
            price = 0
        username = ""
        if request.user.is_authenticated:
            username = request.user.username
        if video:
            r = re.compile('(?:(?:https?\:\/\/)?(?:www\.)?(?:youtube|youtu)(?:(?:\.com|\.be)\/)(?:embed\/)?(?:watch\?)?(?:feature=player_embedded)?&?(?:v=)?([0-z]{11}|[0-z]{4}(?:\-|\_)[0-z]{4}|.(?:\-|\_)[0-z]{9}))')
            videoID = r.match(video).groups()[0]
        ad = Ad(name=c.name, carID=c.id, image=image, image1=image1, image2=image2, image3=image3, image4=image4, video=video, videoID=videoID, date=c.date, country=country, mobile=mobile, advertiser=advertiser, paymentWay=paymentWay, carColor=carColor, status=status, fuel=fuel, driver=driver, price=price, username=username)
        ad.save()
        c.ads.add(ad)
        return HttpResponseRedirect(f"../../{id}")
    elif request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "rest of Ad.html", {"car":c})
        else:
            return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user.banned:
            return render(request, "login.html", {
                "message": "هذا الحساب محظور قم بالابلاغ عن خطأ اذا كنت تعتقد غير ذلك."
            })
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("../list")
        else:
            return render(request, "login.html", {
                "message": "هذا الاسم أو كلمة السر غير صالحين."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("../list")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        phoneNumber = request.POST["phoneNumber"]
        email = "moaz25jan2015@gmail.com"
        pic = request.POST["pic"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "يجب أن تتوافق كلمة السر مع تأكيد كلمة السر."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, phoneNumber=phoneNumber, pic=pic)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "هذا الاسم موجود من قبل."
            })
        login(request, user)
        return HttpResponseRedirect("../list")
    else:
        return render(request, "register.html")


def addToFavList(request, CID):
    if request.method == "GET":
        if request.user.is_authenticated:
            car = Car.objects.get(id=CID)
            request.user.favList.add(car)
            return HttpResponseRedirect(f"../{CID}")
        else:
            return render(request, "loginFav.html", {
                "CID":CID
            })

    elif request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user.banned:
            return render(request, "login.html", {
                "message": "هذا الحساب محظور قم بالابلاغ عن خطأ اذا كنت تعتقد غير ذلك."
            })
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(f"../{CID}")
        else:
            return render(request, "login.html", {
                "message": "هذا الاسم أو كلمة السر غير صالحين."
            })


def removeFavList(request, CID):
    car = Car.objects.get(id=CID)
    request.user.favList.remove(car)
    return HttpResponseRedirect(f"../{CID}")


def favList(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            fav = request.user.favList.all()
            return render(request, "favList.html", {
                "favList":fav
            })
        else:
            return render(request, "loginFavList.html")

    elif request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user.banned:
            return render(request, "login.html", {
                "message": "هذا الحساب محظور قم بالابلاغ عن خطأ اذا كنت تعتقد غير ذلك."
            })
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("../list")
        else:
            return render(request, "login.html", {
                "message": "هذا الاسم أو كلمة السر غير صالحين."
            })


def frstCar(request, frstID):
    cars = Car.objects.all()
    if request.method == "GET":
        return render(request, "secCarChoice.html", {"frstID":frstID, "cars":cars})
    elif request.method == 'POST':
        motorSt = request.POST["motorSt"]
        search = request.POST["search"]
        if motorSt:
            carsMotors = Car.objects.filter(motorSt=motorSt).all()
            return render(request, "secCarChoice.html", {"frstID":frstID, "cars": carsMotors})
        elif search:
            carSearch = []
            for c in cars:
                if search.lower() in c.name.lower():
                    carSearch.append(c)
            return render(request, "secCarChoice.html", {"frstID":frstID, "cars": carSearch})
        else:
            empty = []
            return render(request, "secCarChoice.html", {"frstID":frstID, "cars": empty})

def compare(request, frstID, secID):
    frstDetails = ""
    secDetails = ""
    frstFlaws = ""
    secFlaws = ""
    frstCar = Car.objects.get(id=frstID)
    secCar = Car.objects.get(id=secID)
    fd = frstCar.details
    sd = secCar.details
    ff = frstCar.flaws
    sf = secCar.flaws
    f1 = fd.splitlines()
    s1 = sd.splitlines()
    f2 = ff.splitlines()
    s2 = sf.splitlines()
    for line1 in f1:
        notFound1 = True
        for l1 in s1:
            if line1 == l1:
                notFound1 = False
        if notFound1:
            frstDetails += line1
            frstDetails += '\n'

    for line2 in s1:
        notFound2 = True
        for l2 in f1:
            if line2 == l2:
                notFound2 = False
        if notFound2:
            secDetails += line2
            secDetails += '\n'

    for line3 in f2:
        notFound3 = True
        for l3 in s2:
            if line3 == l3:
                notFound3 = False
        if notFound3:
            frstFlaws += line3
            frstFlaws += '\n'

    for line4 in s2:
        notFound4 = True
        for l4 in f2:
            if line4 == l4:
                notFound4 = False
        if notFound4:
            secFlaws += line4
            secFlaws += '\n'

    return render(request, "compare.html", {
        "frstCar":frstCar,
        "secCar":secCar,
        "frstDetails":frstDetails,
        "secDetails":secDetails,
        "frstFlaws":frstFlaws,
        "secFlaws":secFlaws
    })


def addComent(request, CID):
    if request.method == "POST":
        c = Car.objects.get(id=CID)
        CommentText = request.POST["comment"]
        username = request.user.username
        commentObject = Comment(CommentText=CommentText, username=username)
        commentObject.save()
        c.commentList.add(commentObject)
        return HttpResponseRedirect(f"../{CID}")


def evaluate(request, CID):
    if request.method == "POST":
        c = Car.objects.get(id=CID)
        sending = request.POST["sending"]
        body = request.POST["body"]
        inside = request.POST["inside"]
        wheels = request.POST["wheels"]
        driving = request.POST["driving"]
        glass = request.POST["glass"]
        motor = request.POST["motor"]
        cond = request.POST["cond"]
        comment = request.POST["comment"]
        outside = request.POST["outside"]
        electric = request.POST["electric"]
        seat = request.POST["seat"]
        breaks = request.POST["breaks"]
        fuel = request.POST["fuel"]
        light = request.POST["light"]
        tawgeeh = request.POST["tawgeeh"]
        tabreed = request.POST["tabreed"]
        aadem = request.POST["aadem"]
        qabed = request.POST["qabed"]
        if sending == '1':
            c.sendingVery += 1
        if sending == '2':
            c.sendingGood += 1
        if sending == '3':
            c.sendingMed += 1
        if sending == '4':
            c.sendingBad += 1

        if body == '1':
            c.bodyVery += 1
        if body == '2':
            c.bodyGood += 1
        if body == '3':
            c.bodyMed += 1
        if body == '4':
            c.bodyBad += 1

        if inside == '1':
            c.insideVery += 1
        if inside == '2':
            c.insideGood += 1
        if inside == '3':
            c.insideMed += 1
        if inside == '4':
            c.insideBad += 1

        if wheels == '1':
            c.wheelsVery += 1
        if wheels == '2':
            c.wheelsGood += 1
        if wheels == '3':
            c.wheelsMed += 1
        if wheels == '4':
            c.wheelsBad += 1

        if driving == '1':
            c.drivingVery += 1
        if driving == '2':
            c.drivingGood += 1
        if driving == '3':
            c.drivingMed += 1
        if driving == '4':
            c.drivingBad += 1

        if glass == '1':
            c.glassVery += 1
        if glass == '2':
            c.glassGood += 1
        if glass == '3':
            c.glassMed += 1
        if glass == '4':
            c.glassBad += 1

        if motor == '1':
            c.motorVery += 1
        if motor == '2':
            c.motorGood += 1
        if motor == '3':
            c.motorMed += 1
        if motor == '4':
            c.motorBad += 1

        if cond == '1':
            c.condVery += 1
        if cond == '2':
            c.condGood += 1
        if cond == '3':
            c.condMed += 1
        if cond == '4':
            c.condBad += 1

        if comment == '1':
            c.commentVery += 1
        if comment == '2':
            c.commentGood += 1
        if comment == '3':
            c.commentMed += 1
        if comment == '4':
            c.commentBad += 1

        if outside == '1':
            c.outsideVery += 1
        if outside == '2':
            c.outsideGood += 1
        if outside == '3':
            c.outsideMed += 1
        if outside == '4':
            c.outsideBad += 1

        if electric == '1':
            c.electricVery += 1
        if electric == '2':
            c.electricGood += 1
        if electric == '3':
            c.electricMed += 1
        if electric == '4':
            c.electricBad += 1

        if seat == '1':
            c.seatVery += 1
        if seat == '2':
            c.seatGood += 1
        if seat == '3':
            c.seatMed += 1
        if seat == '4':
            c.seatBad += 1

        if breaks == '1':
            c.breakVery += 1
        if breaks == '2':
            c.breakGood += 1
        if breaks == '3':
            c.breakMed += 1
        if breaks == '4':
            c.breakBad += 1

        if fuel == '1':
            c.fuelVery += 1
        if fuel == '2':
            c.fuelGood += 1
        if fuel == '3':
            c.fuelMed += 1
        if fuel == '4':
            c.fuelBad += 1

        if light == '1':
            c.lightVery += 1
        if light == '2':
            c.lightGood += 1
        if light == '3':
            c.lightMed += 1
        if light == '4':
            c.lightBad += 1

        if tawgeeh == '1':
            c.tawgeehVery += 1
        if tawgeeh == '2':
            c.tawgeehGood += 1
        if tawgeeh == '3':
            c.tawgeehMed += 1
        if tawgeeh == '4':
            c.tawgeehBad += 1

        if tabreed == '1':
            c.tabreedVery += 1
        if tabreed == '2':
            c.tabreedGood += 1
        if tabreed == '3':
            c.tabreedMed += 1
        if tabreed == '4':
            c.tabreedBad += 1

        if aadem == '1':
            c.aademVery += 1
        if aadem == '2':
            c.aademGood += 1
        if aadem == '3':
            c.aademMed += 1
        if aadem == '4':
            c.aademBad += 1

        if qabed == '1':
            c.qabedVery += 1
        if qabed == '2':
            c.qabedGood += 1
        if qabed == '3':
            c.qabedMed += 1
        if qabed == '4':
            c.qabedBad += 1

        c.totalEv = (c.sendingVery * 4) + (c.sendingGood *3) + (c.sendingMed *2) + (c.sendingBad * -2) + (c.bodyVery *4) + (c.bodyGood *3) + (c.bodyMed *2) + (c.bodyBad * -2) + (c.insideVery *4) + (c.insideGood *3) + (c.insideMed *2) + (c.insideBad * -2) + (c.wheelsVery *4) + (c.wheelsGood *3) + (c.wheelsMed *2) + (c.wheelsBad * -2) + (c.drivingVery *4) + (c.drivingGood *3) + (c.drivingMed *2) + (c.drivingBad * -2) + (c.glassVery *4) + (c.glassGood *3) + (c.glassMed *2) + (c.glassBad * -2) + (c.motorVery *4) + (c.motorGood *3) + (c.motorMed *2) + (c.motorBad * -2) + (c.condVery *4) + (c.condGood *3) + (c.condMed *2) + (c.condBad * -2) + (c.commentVery *4) + (c.commentGood *3) + (c.commentMed *2) + (c.commentBad * -2) + (c.outsideVery *4) + (c.outsideGood *3) + (c.outsideMed *2) + (c.outsideBad * -2) + (c.electricVery *4) + (c.electricGood *3) + (c.electricMed *2) + (c.electricBad * -2) + (c.seatVery *4) + (c.seatGood *3) + (c.seatMed *2) + (c.seatBad * -2) + (c.breakVery *4) + (c.breakGood *3) + (c.breakMed *2) + (c.breakBad * -2) + (c.fuelVery *4) + (c.fuelGood * 3) + (c.fuelMed *2) + (c.fuelBad * -2) + (c.lightVery *4) + (c.lightGood *3) + (c.lightMed *2) + (c.lightBad * -2) + (c.tawgeehVery *4) + (c.tawgeehGood *3) + (c.tawgeehMed *2) + (c.tawgeehBad * -2) + (c.tabreedVery *4) + (c.tabreedGood *3) + (c.tabreedMed *2) + (c.tabreedBad * -2) + (c.aademVery *4) + (c.aademGood *3) + (c.aademMed *2) + (c.aademBad * -2) + (c.qabedVery *4) + (c.qabedGood *3) + (c.qabedMed *2) + (c.qabedBad * -2)

        c.save()
        request.user.evaluatedCars.add(c)
        return HttpResponseRedirect(f"../{CID}")
    elif request.method == "GET":
        if request.user.is_authenticated:
            notFound = True
            evaluatedCars = request.user.evaluatedCars.all()
            for ca in evaluatedCars:
                if ca.id == CID:
                    notFound = False
            if notFound:
                return render(request, "evaluation.html")
            else:
                return HttpResponseRedirect("../list")
        else:
            return render(request, "loginFav.html", {
                "CID": CID
            })

def totalEvaluation(request):
    cars = Car.objects.all()
    frstID = 0
    secID = 0
    thirdID = 0
    fourthID = 0
    fifthID = 0
    sixthID = 0
    maxValue = 0
    secMaxValue = 0
    thirdMaxValue = 0
    minValue = 0
    secMinValue = 0
    thirdMinValue = 0
    for ca in cars:
        maxValue = ca.totalEv
        secMaxValue = ca.totalEv
        thirdMaxValue = ca.totalEv
        minValue = ca.totalEv
        secMinValue = ca.totalEv
        thirdMinValue = ca.totalEv
        break
    for c in cars:
        if c.totalEv >= maxValue:
            maxValue = c.totalEv
            frstID = c.id
    for c in cars:
        if c.totalEv >= secMaxValue and c.id != frstID:
            secMaxValue = c.totalEv
            secID = c.id
    for c in cars:
        if c.totalEv >= thirdMaxValue and c.id != frstID and c.id != secID:
            thirdMaxValue = c.totalEv
            thirdID = c.id

    for c in cars:
        if c.totalEv <= minValue:
            minValue = c.totalEv
            fourthID = c.id
    for c in cars:
        if c.totalEv <= secMinValue and c.id != fourthID:
            secMinValue = c.totalEv
            fifthID = c.id
    for c in cars:
        if c.totalEv <= thirdMinValue and c.id != fourthID and c.id != fifthID:
            thirdMinValue = c.totalEv
            sixthID = c.id

    frst = Car.objects.get(id=frstID)
    sec = Car.objects.get(id=secID)
    third = Car.objects.get(id=thirdID)
    fourth = Car.objects.get(id=fourthID)
    fifth = Car.objects.get(id=fifthID)
    sixth = Car.objects.get(id=sixthID)

    return render(request, "totalEvaluation.html", {
        "frst":frst,
        "sec":sec,
        "third":third,
        "fourth":fourth,
        "fifth":fifth,
        "sixth":sixth
    })

def changeSold(request, AdId, CID):
    ad = Ad.objects.get(id=AdId)
    if ad.sold:
        ad.sold = False
    else:
        ad.sold = True
    ad.save()
    exists = False
    c = Car.objects.get(id=CID)
    comments = c.commentList.all()
    if request.user.is_authenticated:
        fav = request.user.favList.all()
        for ca in fav:
            if ca.id == CID:
                exists = True

    ads = c.ads.all()
    return render(request, "view.html", {
        "car": c,
        "ads": ads,
        "exists": exists,
        "comments": comments
    })


def addFavGen(request, id):
    if request.user.is_authenticated:
        notFound = True
        favcars = FavCar.objects.all()
        for cc in favcars:
            if cc.carID == id:
                notFound = False
        if notFound:
            c = Car.objects.get(id=id)
            fc = FavCar(name=c.name, image=c.image, logo=c.logo, carID=c.id, userID=request.user.id, username=request.user.username, userPic=request.user.pic)
            fc.save()
        return HttpResponseRedirect("../list")
    else:
        return HttpResponseRedirect("../login")


def genFavList(request):
    favCars = FavCar.objects.all().order_by("-id")
    if request.method == "GET":
        return render(request, "general favourite list.html", {
            "cars":favCars
        })
    elif request.method == "POST":
        if request.user.is_authenticated:
            id = request.POST["id"]
            fc = FavCar.objects.get(id=id)
            likes = fc.likes.all()
            notLiked = True
            for l in likes:
                if l.id == request.user.id:
                    notLiked = False
            if notLiked:
                fc.likes.add(request.user)
                fc.likesCount += 1
                fc.save()
            return render(request, "general favourite list.html", {
                "cars": favCars
            })
        else:
            return HttpResponseRedirect("../login")


def addCommentFav(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            id = request.POST["id"]
            commentText = request.POST["commentText"]
            comment = Comment(CommentText=commentText, username=request.user.username)
            comment.save()
            fc = FavCar.objects.get(id=id)
            fc.commentList.add(comment)
            fc.save()
            return HttpResponseRedirect("../genFavList")
        else:
            return HttpResponseRedirect("../login")


def deleteAd(request, id, CID):
    a = Ad.objects.get(id=id)
    a.delete()

    return HttpResponseRedirect(f"../../../{CID}")


def users(request):
    us = User.objects.order_by('username')
    return render(request, "users.html", {
        "users":us,
    })


def ban(request, id):
    u = User.objects.get(id=id)
    u.banned = True
    u.save()
    return HttpResponseRedirect("../../users")


def unban(request, id):
    u = User.objects.get(id=id)
    u.banned = False
    u.save()
    return HttpResponseRedirect("../../users")

def ads(request):
    ads = Ad.objects.all()
    if request.method == 'GET':
        return render(request, "ads.html", {
            "ads": ads,
        })


    elif request.method == 'POST':
        search = request.POST["search"]

        if search:

            adsSearch = []
            for ad in ads:
                if search.lower() in ad.name.lower():
                    adsSearch.append(ad)
            return render(request, "ads.html", {

                "ads": adsSearch,

            })

        else:

            empty = []

            return render(request, "ads.html", {

                "ads": empty,

            })

def alpha(request, C):
    ads = Ad.objects.all()
    adsAlpha = []
    for a in ads:
        if a.name[0].lower() == C.lower():
            adsAlpha.append(a)

    if request.method == 'GET':
        return render(request, "ads.html", {
            "ads": adsAlpha,
        })


def carAlpha(request, C):
    cars = Car.objects.all()
    allModels = CarModel.objects.order_by('modelText')
    allSorts = Sort.objects.order_by('sortText')
    v = View.objects.get(id=1)
    carsAlpha = []
    for c in cars:
        if c.name[0].lower() == C.lower():
            carsAlpha.append(c)

    paginator = Paginator(carsAlpha, 150)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        cars1 = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cars1 = paginator.page(paginator.num_pages)
    if request.method == 'GET':
        return render(request, "list.html", {
            "cars": cars1,
            "models": allModels,
            "sorts": allSorts,
            "viewsCount": v.viewsCount
        })
    elif request.method == 'POST':

        motorSt = request.POST["motorSt"]

        search = request.POST["search"]

        model = request.POST["model"]

        sort = request.POST["sort"]

        date = request.POST["date"]

        if motorSt:

            carsMotors = []

            if search:

                if model:

                    if sort:

                        if date:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()) and (
                                        sort.lower() == c.sortText.lower()) and (date == c.date):
                                    carsMotors.append(c)

                        else:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)

                    else:

                        if date:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()) and (date == c.date):
                                    carsMotors.append(c)

                        else:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        model.lower() == c.modelText.lower()):
                                    carsMotors.append(c)

                else:

                    if date:

                        if sort:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        sort.lower() == c.sortText.lower()) and (date == c.date):
                                    carsMotors.append(c)

                        else:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (date == c.date):
                                    carsMotors.append(c)

                    else:

                        if sort:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()) and (
                                        sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)

                        else:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (search.lower() in c.name.lower()):
                                    carsMotors.append(c)

            else:

                if model:

                    if date:

                        if sort:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (sort.lower() == c.sortText.lower()) and (
                                        date == c.date) and (
                                        model.lower() == c.modelText.lower()):
                                    carsMotors.append(c)

                        else:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (model.lower() == c.modelText.lower()) and (
                                        date == c.date):
                                    carsMotors.append(c)

                    else:

                        if sort:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (model.lower() == c.modelText.lower()) and (
                                        sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)

                        else:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (model.lower() == c.modelText.lower()):
                                    carsMotors.append(c)

                else:

                    if date:

                        if sort:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (sort.lower() == c.sortText.lower()) and (date == c.date):
                                    carsMotors.append(c)

                        else:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (date == c.date):
                                    carsMotors.append(c)

                    else:

                        if sort:

                            for c in carsAlpha:

                                if (motorSt == c.motorSt) and (sort.lower() == c.sortText.lower()):
                                    carsMotors.append(c)

                        else:

                            for c in carsAlpha:

                                if motorSt == c.motorSt:
                                    carsMotors.append(c)

            paginator = Paginator(carsMotors, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        elif search:

            carSearch = []

            if model:

                if sort:

                    if date:

                        for c in carsAlpha:

                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()) and (
                                    sort.lower() == c.sortText.lower()) and (date == c.date):
                                carSearch.append(c)

                    else:

                        for c in carsAlpha:

                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()) and (
                                    sort.lower() == c.sortText.lower()):
                                carSearch.append(c)

                else:

                    if date:

                        for c in carsAlpha:

                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()) and (
                                    date == c.date):
                                carSearch.append(c)

                    else:

                        for c in carsAlpha:

                            if (search.lower() in c.name.lower()) and (model.lower() == c.modelText.lower()):
                                carSearch.append(c)

            else:

                if date:

                    if sort:

                        for c in carsAlpha:

                            if (search.lower() in c.name.lower()) and (sort.lower() == c.sortText.lower()) and (
                                    date == c.date):
                                carSearch.append(c)

                    else:

                        for c in carsAlpha:

                            if (search.lower() in c.name.lower()) and (date == c.date):
                                carSearch.append(c)

                else:

                    if sort:

                        for c in carsAlpha:

                            if (search.lower() in c.name.lower()) and (sort.lower() == c.sortText.lower()):
                                carSearch.append(c)

                    else:

                        for c in carsAlpha:

                            if search.lower() in c.name.lower():
                                carSearch.append(c)

            paginator = Paginator(carSearch, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        elif model:

            carsModels = []

            if sort:

                if date:

                    for c in carsAlpha:

                        if (model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()) and (
                                date == c.date):
                            carsModels.append(c)

                else:

                    for c in carsAlpha:

                        if (model.lower() == c.modelText.lower()) and (sort.lower() == c.sortText.lower()):
                            carsModels.append(c)

            else:

                if date:

                    for c in carsAlpha:

                        if (model.lower() == c.modelText.lower()) and (date == c.date):
                            carsModels.append(c)

                else:

                    for c in carsAlpha:

                        if model.lower() == c.modelText.lower():
                            carsModels.append(c)

            paginator = Paginator(carsModels, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        elif sort:

            carsSorts = []

            if date:

                for c in carsAlpha:

                    if (sort.lower() == c.sortText.lower()) and (date == c.date):
                        carsSorts.append(c)

            else:

                for c in carsAlpha:

                    if sort.lower() == c.sortText.lower():
                        carsSorts.append(c)

            paginator = Paginator(carsSorts, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        elif date:

            carsDate = []
            for c in carsAlpha:
                if date == c.date:
                    carsDate.append(c)

            paginator = Paginator(carsDate, 50000)
            try:
                page = int(request.GET.get('page', '1'))
            except:
                page = 1

            try:
                cars1 = paginator.page(page)
            except(EmptyPage, InvalidPage):
                cars1 = paginator.page(paginator.num_pages)
            return render(request, "list.html", {

                "cars": cars1,

                "models": allModels,

                "sorts": allSorts

            })

        else:

            empty = []

            return render(request, "list.html", {

                "cars": empty,

                "models": allModels,

                "sorts": allSorts

            })

def gooogle(request):
    return render(request, "google9d3ea0c0cb0559ab.html")
