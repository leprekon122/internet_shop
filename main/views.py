from django.shortcuts import render, redirect
from rest_framework import generics, mixins, permissions
from django.contrib.auth import authenticate, login
from .serializers import *
from .models import *
from .forms import *
from django.db.models import Sum

from django.db.models import Max


# Create your views here.
class MainPage(generics.GenericAPIView):
    @staticmethod
    def get(request):
        if request.GET.get('login'):
            username = request.GET.get('username')
            password = request.GET.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main')
        username = request.user
        model_cart = ProductCart.objects.all()

        '''cart_total_price'''
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        data = {'username': username,
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum']}
        return render(request, 'main/main_page.html', data)

    def post(self, request):
        delete_btn = request.POST.get('delete_btn')

        if delete_btn:
            ProductCart.objects.filter(id=delete_btn).delete()
            return redirect('main')


class Registration(generics.GenericAPIView,
                   mixins.CreateModelMixin):

    @staticmethod
    def get(request):
        form = RegistrationUser
        data = {"form": form}
        return render(request, "main/registration.html", data)

    def post(self, request):
        try:
            form = RegistrationUser(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main')
        except Exception:
            return redirect('registration')


class DetailInfo(generics.GenericAPIView):
    @staticmethod
    def get(request):
        return render(request, 'main/stuff_detail.html')


class Nothebooks(generics.GenericAPIView):
    @staticmethod
    def get(request):

        model = NotebooksList.objects.all()
        '''cart_all_items'''
        model_cart = ProductCart.objects.all()

        search = request.GET.get('exampleRadios')
        detail = request.GET.get('stuff_detail')
        prices = request.GET.get('price')

        if prices:
            try:
                price_from = request.GET.get('price_from')
                price_to = request.GET.get('price_to')
                if price_from != '' and price_to != '':
                    model = NotebooksList.objects.filter(price__gte=int(price_from), price__lte=int(price_to))
                elif price_from == '':
                    model = NotebooksList.objects.filter(price__lte=int(price_to))
                else:
                    model = NotebooksList.objects.filter(price__gte=int(price_from))

            except Exception:
                return redirect('note_main')

        if detail:
            model_rating = CommentsUsers.objects.filter(name_of_stuff=detail).values('rating')
            model_cart = ProductCart.objects.all()

            avr_rating = 0
            for el in model_rating:
                res = el['rating']
                if res is not None:
                    avr_rating += int(res)
                else:
                    res = 0
                    avr_rating += res

            model = NotebooksList.objects.filter(id=detail)
            model_1 = CommentsUsers.objects.filter(name_of_stuff=NotebooksList(detail)).values('rating', 'name_of_user',
                                                                                               'comment', 'link_video',
                                                                                               'date')
            model_2 = QuestionUsers.objects.filter(name_of_stuff=NotebooksList(detail)).values('name_of_user',
                                                                                               'comment', 'date')
            try:
                avr_rating_plural = avr_rating // len(model_rating)
            except Exception:
                avr_rating_plural = 0

            quantity_of_comment = len(model_rating)

            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))
            quentety = len(model_1)
            quentety_1 = len(model_2)

            data = {'model': model,
                    'model_1': model_1,
                    'model_2': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1,
                    'avg_rating': avr_rating_plural,
                    'quantity_of_comment': quantity_of_comment,
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum']
                    }
            return render(request, 'main/stuff_detail.html', data)

        if search:
            if search == "Apple":
                model = NotebooksList.objects.filter(brand='Apple')


            elif search == "Acer":
                model = NotebooksList.objects.filter(brand='Acer')


            elif search == "Asus":
                model = NotebooksList.objects.filter(brand='Asus')

        price_max = model.aggregate(Max('price'))
        username = request.user
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        data = {'model': model,
                'username': username,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                }
        return render(request, 'main/nothebook.html', data)

    def post(self, request):
        add_comment = request.POST.get('add_comment')
        add_questions = request.POST.get('add_question')
        buy = request.POST.get('buy')
        delete_btn = request.POST.get('delete_btn')

        if delete_btn:
            ProductCart.objects.filter(id=delete_btn).delete()
            return redirect(request.path_info)

        if buy:
            test = NotebooksList.objects.filter(id=buy).values()[0]
            username = request.user
            title = test['title']
            product_pic = test['pic_link']
            product_price = test['price']
            product_status = test['in_out']

            ProductCart.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                       product_price=product_price, product_status=product_status)

            return redirect(request.path_info)

        if add_comment:
            username = request.user
            rating = request.POST.get('simple-rating')
            stuff_name = request.POST.get('add_comment')
            comment = request.POST.get('comment')
            link_video = request.POST.get('link_video')
            CommentsUsers.objects.create(rating=rating, name_of_user=username, name_of_stuff=NotebooksList(stuff_name),
                                         comment=comment, link_video=link_video)
            model = NotebooksList.objects.filter(id=stuff_name)
            model_1 = CommentsUsers.objects.filter(name_of_stuff=NotebooksList(stuff_name)).values('rating',
                                                                                                   'name_of_user',
                                                                                                   'comment', 'date')

            model_2 = QuestionUsers.objects.filter(name_of_stuff=NotebooksList(stuff_name)).values('name_of_user',
                                                                                                   'comment', 'date')
            quentety = len(model_1)
            quentety_1 = len(model_2)

            data = {'model': model,
                    'model_1': model_1,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1
                    }
            return render(request, 'main/stuff_detail.html', data)

        if add_questions:
            username = request.user
            stuff_name = request.POST.get('add_question')
            comment = request.POST.get('question')
            QuestionUsers.objects.create(name_of_user=username, name_of_stuff=NotebooksList(stuff_name),
                                         comment=comment)
            model = NotebooksList.objects.filter(id=stuff_name)
            model_1 = CommentsUsers.objects.filter(name_of_stuff=NotebooksList(stuff_name)).values('rating',
                                                                                                   'name_of_user',
                                                                                                   'comment', 'date')
            model_2 = QuestionUsers.objects.filter(name_of_stuff=NotebooksList(stuff_name)).values('name_of_user',
                                                                                                   'comment', 'date')
            quentety = len(model_1)
            quentety_1 = len(model_2)
            data = {'model': model,
                    'model_1': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1}
            return render(request, 'main/stuff_detail.html', data)


class Videocard(generics.GenericAPIView):
    @staticmethod
    def get(request):
        model = Videocards.objects.all()
        model_cart = ProductCart.objects.all()

        search = request.GET.get('exampleRadios')
        detail = request.GET.get('stuff_detail')
        prices = request.GET.get('price')

        if prices:
            try:
                price_from = request.GET.get('price_from')
                price_to = request.GET.get('price_to')
                if price_from != '' and price_to != '':
                    model = Videocards.objects.filter(price__gte=int(price_from), price__lte=int(price_to))
                elif price_from == '':
                    model = Videocards.objects.filter(price__lte=int(price_to))
                else:
                    model = Videocards.objects.filter(price__gte=int(price_from))

            except Exception:
                return redirect('videocards')

        if detail:
            model_rating = CommentsUsersVideocard.objects.filter(name_of_stuff=detail).values('rating')

            avr_rating = 0
            for el in model_rating:
                res = el['rating']
                if res is not None:
                    avr_rating += int(res)
                else:
                    res = 0
                    avr_rating += res

            model = Videocards.objects.filter(id=detail)
            model_1 = CommentsUsersVideocard.objects.filter(name_of_stuff=Videocards(detail)).values('rating',
                                                                                                     'name_of_user',
                                                                                                     'comment',
                                                                                                     'link_video',
                                                                                                     'date')

            model_2 = QuestionUsersVideocard.objects.filter(name_of_stuff=Videocards(detail)).values('name_of_user',
                                                                                                     'comment', 'date')
            try:
                avr_rating_plural = avr_rating // len(model_rating)
            except Exception:
                avr_rating_plural = 0
            quantity_of_comment = len(model_rating)

            quentety = len(model_1)
            quentety_1 = len(model_2)
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'model_1': model_1,
                    'model_2': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1,
                    'avg_rating': avr_rating_plural,
                    'quantity_of_comment': quantity_of_comment,
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum']
                    }
            return render(request, 'main/stuff_detail.html', data)

        if search == "AMD":
            model = Videocards.objects.filter(brand='AMD')

        elif search == "Gigabyte":
            model = Videocards.objects.filter(brand='Gigabyte')

        elif search == "Asus":
            model = Videocards.objects.filter(brand='Asus')

        elif search == "INNO3D":
            model = Videocards.objects.filter(brand='INNO3D')

        elif search == "MSI":
            model = Videocards.objects.filter(brand='MSI')

        username = request.user
        price_max = model.aggregate(Max('price'))

        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        data = {"model": model,
                'username': username,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum']
                }

        return render(request, "main/videocards.html", data)

    @staticmethod
    def post(request):
        add_comment = request.POST.get('add_comment')
        add_question = request.POST.get('add_question')
        buy = request.POST.get('buy')
        delete_btn = request.POST.get('delete_btn')

        if delete_btn:
            ProductCart.objects.filter(id=delete_btn).delete()
            return redirect('videocards')

        if buy:
            test = Videocards.objects.filter(id=buy).values()[0]
            username = request.user
            title = test['title']
            product_pic = test['pic_link']
            product_price = test['price']
            product_status = test['in_out']

            ProductCart.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                       product_price=product_price, product_status=product_status)

            return redirect('videocards')

        if add_comment:
            username = request.user
            rating = request.POST.get('simple-rating')
            stuff_name = request.POST.get('add_comment')
            comment = request.POST.get('comment')
            link_video = request.POST.get('link_video')
            CommentsUsersVideocard.objects.create(rating=rating, name_of_user=username,
                                                  name_of_stuff=Videocards(stuff_name),
                                                  comment=comment, link_video=link_video)
            model = Videocards.objects.filter(id=stuff_name)
            model_1 = CommentsUsersVideocard.objects.filter(name_of_stuff=Videocards(stuff_name)).values('name_of_user',
                                                                                                         'comment',
                                                                                                         'date')
            model_2 = QuestionUsersVideocard.objects.filter(name_of_stuff=Videocards(stuff_name)).values(
                'name_of_user',
                'comment', 'date')

            quentety = len(model_1)
            quentety_1 = len(model_2)
            data = {'model': model,
                    'model_1': model_1,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1
                    }
            return render(request, 'main/stuff_detail.html', data)

        if add_question:
            username = request.user
            stuff_name = request.POST.get('add_question')
            comment = request.POST.get('question')
            QuestionUsersVideocard.objects.create(name_of_user=username, name_of_stuff=Videocards(stuff_name),
                                                  comment=comment)
            model = Videocards.objects.filter(id=stuff_name)
            model_1 = CommentsUsersVideocard.objects.filter(name_of_stuff=Videocards(stuff_name)).values('name_of_user',
                                                                                                         'comment',
                                                                                                         'date')

            model_2 = QuestionUsersVideocard.objects.filter(name_of_stuff=Videocards(stuff_name)).values(
                'name_of_user',
                'comment', 'date')

            quentety = len(model_1)
            quentety_1 = len(model_2)
            data = {'model': model,
                    'model_1': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1}
            return render(request, 'main/stuff_detail.html', data)


class Monitors(generics.GenericAPIView):

    @staticmethod
    def get(request):
        search = request.GET.get('exampleRadios')
        detail = request.GET.get('stuff_detail')
        prices = request.GET.get('price')

        model = Monitors_list.objects.all()
        model_cart = ProductCart.objects.all()

        if prices:
            try:
                price_from = request.GET.get('price_from')
                price_to = request.GET.get('price_to')
                if price_from != '' and price_to != '':
                    model = Monitors_list.objects.filter(price__gte=int(price_from), price__lte=int(price_to))
                elif price_from == '':
                    model = Monitors_list.objects.filter(price__lte=int(price_to))
                else:
                    model = Monitors_list.objects.filter(price__gte=int(price_from))

            except Exception:
                return redirect('displays')

        if detail:
            model_rating = CommentsUserMonitor.objects.filter(name_of_stuff=detail).values('rating')

            avr_rating = 0
            for el in model_rating:
                res = el['rating']
                if res is not None:
                    avr_rating += int(res)
                else:
                    res = 0
                    avr_rating += res

            model = Monitors_list.objects.filter(id=detail)
            model_1 = CommentsUserMonitor.objects.filter(name_of_stuff=Monitors_list(detail)).values('rating',
                                                                                                     'name_of_user',
                                                                                                     'comment',
                                                                                                     'link_video',
                                                                                                     'date')
            model_2 = QuestionUsersMonitor.objects.filter(name_of_stuff=Monitors_list(detail)).values('name_of_user',
                                                                                                      'comment', 'date')

            try:
                avr_rating_plural = avr_rating // len(model_rating)
            except Exception:
                avr_rating_plural = 0
            quantity_of_comment = len(model_rating)

            quentety = len(model_1)
            quentety_1 = len(model_2)
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'model_1': model_1,
                    'model_2': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1,
                    'avg_rating': avr_rating_plural,
                    'quantity_of_comment': quantity_of_comment,
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum']
                    }
            return render(request, 'main/stuff_detail.html', data)

        if search == "Asus":
            model = Monitors_list.objects.filter(brand='Asus')

        elif search == "Acer":
            model = Monitors_list.objects.filter(brand='Acer')

        elif search == "BenQ":
            model = Monitors_list.objects.filter(brand='BenQ')

        elif search == "Dell":
            model = Monitors_list.objects.filter(brand='Dell')

        elif search == "LG":
            model = Monitors_list.objects.filter(brand='LG')

        price_max = model.aggregate(Max('price'))
        username = request.user
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        data = {'username': username,
                'model': model,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum']
                }
        return render(request, 'main/displays.html', data)

    def post(self, request):
        add_comment = request.POST.get('add_comment')
        add_question = request.POST.get('add_question')
        buy = request.POST.get('buy')
        delete_btn = request.POST.get('delete_btn')

        if delete_btn:
            ProductCart.objects.filter(id=delete_btn).delete()
            return redirect('displays')

        if buy:
            test = Monitors_list.objects.filter(id=buy).values()[0]
            username = request.user
            title = test['title']
            product_pic = test['pic_link']
            product_price = test['price']
            product_status = test['in_out']

            ProductCart.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                       product_price=product_price, product_status=product_status)

            return redirect('displays')

        if add_comment:
            username = request.user
            rating = request.POST.get('simple-rating')
            stuff_name = request.POST.get('add_comment')
            comment = request.POST.get('comment')
            link_video = request.POST.get('link_video')
            CommentsUserMonitor.objects.create(rating=rating, name_of_user=username,
                                               name_of_stuff=Monitors_list(stuff_name),
                                               comment=comment, link_video=link_video)
            model = Monitors_list.objects.filter(id=stuff_name)
            model_1 = CommentsUserMonitor.objects.filter(name_of_stuff=Monitors_list(stuff_name)).values('rating',
                                                                                                         'name_of_user',
                                                                                                         'comment',
                                                                                                         'date')
            model_2 = QuestionUsersMonitor.objects.filter(name_of_stuff=Monitors_list(stuff_name)).values(
                'name_of_user',
                'comment', 'date')

            quentety = len(model_1)
            quentety_1 = len(model_2)
            data = {'model': model,
                    'model_1': model_1,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1,

                    }
            return render(request, 'main/stuff_detail.html', data)

        if add_question:
            username = request.user
            stuff_name = request.POST.get('add_question')
            comment = request.POST.get('question')
            QuestionUsersMonitor.objects.create(name_of_user=username, name_of_stuff=Monitors_list(stuff_name),
                                                comment=comment)
            model = Monitors_list.objects.filter(id=stuff_name)
            model_1 = CommentsUserMonitor.objects.filter(name_of_stuff=Monitors_list(stuff_name)).values('name_of_user',
                                                                                                         'comment',
                                                                                                         'date')

            model_2 = QuestionUsersMonitor.objects.filter(name_of_stuff=Monitors_list(stuff_name)).values(
                'name_of_user',
                'comment', 'date')

            quentety = len(model_1)
            quentety_1 = len(model_2)
            data = {'model': model,
                    'model_1': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1}
            return render(request, 'main/stuff_detail.html', data)


class Memory(generics.GenericAPIView):

    @staticmethod
    def get(request):
        search = request.GET.get('exampleRadios')
        detail = request.GET.get('stuff_detail')
        prices = request.GET.get('price')

        model = Memory_list.objects.all()
        model_cart = ProductCart.objects.all()

        if prices:
            try:
                price_from = request.GET.get('price_from')
                price_to = request.GET.get('price_to')
                if price_from != '' and price_to != '':
                    model = Memory_list.objects.filter(price__gte=int(price_from), price__lte=int(price_to))
                elif price_from == '':
                    model = Memory_list.objects.filter(price__lte=int(price_to))
                else:
                    model = Memory_list.objects.filter(price__gte=int(price_from))

            except Exception:
                return redirect('memory')

        if detail:
            model_rating = CommentsUserMemory.objects.filter(name_of_stuff=detail).values('rating')

            avr_rating = 0
            for el in model_rating:
                res = el['rating']
                if res is not None:
                    avr_rating += int(res)
                else:
                    res = 0
                    avr_rating += res

            model = Memory_list.objects.filter(id=detail)
            model_1 = CommentsUserMemory.objects.filter(name_of_stuff=Memory_list(detail)).values('rating',
                                                                                                  'name_of_user',
                                                                                                  'comment',
                                                                                                  'link_video',
                                                                                                  'date')
            model_2 = QuestionUsersMemory.objects.filter(name_of_stuff=Memory_list(detail)).values('name_of_user',
                                                                                                   'comment', 'date')

            try:
                avr_rating_plural = avr_rating // len(model_rating)
            except Exception:
                avr_rating_plural = 0
            quantity_of_comment = len(model_rating)

            quentety = len(model_1)
            quentety_1 = len(model_2)
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'model_1': model_1,
                    'model_2': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1,
                    'avg_rating': avr_rating_plural,
                    'quantity_of_comment': quantity_of_comment,
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum']
                    }
            return render(request, 'main/stuff_detail.html', data)

        if search == "AMD":
            model = Memory_list.objects.filter(brand='AMD')

        elif search == "Crucial":
            model = Memory_list.objects.filter(brand='Crucial')

        elif search == "HyperX":
            model = Memory_list.objects.filter(brand='HyperX')

        elif search == "Kingston":
            model = Memory_list.objects.filter(brand='Kingston')

        elif search == "Samsung":
            model = Memory_list.objects.filter(brand='Samsung')

        price_max = model.aggregate(Max('price'))
        username = request.user
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        data = {'username': username,
                'model': model,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum']
                }

        return render(request, 'main/memory.html', data)

    def post(self, request):
        add_comment = request.POST.get('add_comment')
        add_question = request.POST.get('add_question')
        buy = request.POST.get('buy')
        delete_btn = request.POST.get('delete_btn')

        if delete_btn:
            ProductCart.objects.filter(id=delete_btn).delete()
            return redirect('memory')

        if buy:
            test = Memory_list.objects.filter(id=buy).values()[0]
            username = request.user
            title = test['title']
            product_pic = test['pic_link']
            product_price = test['price']
            product_status = test['in_out']

            ProductCart.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                       product_price=product_price, product_status=product_status)

            return redirect('memory')

        if add_comment:
            username = request.user
            rating = request.POST.get('simple-rating')
            stuff_name = request.POST.get('add_comment')
            comment = request.POST.get('comment')
            link_video = request.POST.get('link_video')
            CommentsUserMemory.objects.create(rating=rating, name_of_user=username,
                                              name_of_stuff=Memory_list(stuff_name),
                                              comment=comment, link_video=link_video)
            model = Memory_list.objects.filter(id=stuff_name)
            model_1 = CommentsUserMemory.objects.filter(name_of_stuff=Memory_list(stuff_name)).values('rating',
                                                                                                      'name_of_user',
                                                                                                      'comment',
                                                                                                      'date')
            model_2 = QuestionUsersMemory.objects.filter(name_of_stuff=Memory_list(stuff_name)).values(
                'name_of_user',
                'comment', 'date')

            quentety = len(model_1)
            quentety_1 = len(model_2)
            data = {'model': model,
                    'model_1': model_1,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1,

                    }
            return render(request, 'main/stuff_detail.html', data)

        if add_question:
            username = request.user
            stuff_name = request.POST.get('add_question')
            comment = request.POST.get('question')
            QuestionUsersMemory.objects.create(name_of_user=username, name_of_stuff=Memory_list(stuff_name),
                                               comment=comment)
            model = Memory_list.objects.filter(id=stuff_name)
            model_1 = CommentsUserMemory.objects.filter(name_of_stuff=Memory_list(stuff_name)).values('name_of_user',
                                                                                                      'comment',
                                                                                                      'date')

            model_2 = QuestionUsersMonitor.objects.filter(name_of_stuff=Memory_list(stuff_name)).values(
                'name_of_user',
                'comment', 'date')

            quentety = len(model_1)
            quentety_1 = len(model_2)
            data = {'model': model,
                    'model_1': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1}
            return render(request, 'main/stuff_detail.html', data)


class NothebookApi(generics.GenericAPIView,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   ):
    queryset = NotebooksList.objects.all()
    serializer_class = NothebooksSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NothebookApiDeleteOrupdate(generics.GenericAPIView,
                                 mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin):
    queryset = NotebooksList.objects.all()
    serializer_class = NothebooksSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, *kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class DetailCommentsApi(generics.GenericAPIView,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    queryset = CommentsUsers.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, *kwargs)
