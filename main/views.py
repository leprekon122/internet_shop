from django.shortcuts import render, redirect
from rest_framework import generics, mixins, permissions
from django.contrib.auth import authenticate, login
from .serializers import *
from .models import *
from .forms import *
from django.db.models import Sum, Avg, Max


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

        """Like like all"""
        model_like = LikeListModel.objects.all()

        data = {'username': username,
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like
                }
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

        """Like like all"""
        model_like = LikeListModel.objects.all()

        detail = request.GET.get('stuff_detail')
        filter = request.GET.get('search')
        reject_filters = request.GET.get('reject_filters')

        if filter:
            ready_deliver = request.GET.get('ready_deliver')
            search = request.GET.get('exampleRadios')
            price_to = request.GET.get('price_to')
            price_from = request.GET.get('price_from')
            print(search)

            if search is not None:
                # filter with start and end price
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = NotebooksList.objects.filter(brand=search, price__gte=int(price_from),
                                                                 price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        try:
                            model = NotebooksList.objects.filter(brand=search, price__gte=int(price_from),
                                                                 price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter without  start price
                elif price_from is None:
                    #  have stuff
                    if ready_deliver:
                        try:
                            model = NotebooksList.objects.filter(brand=search, price__lte=int(price_to),
                                                                 in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have  stuff
                    else:
                        try:
                            model = NotebooksList.objects.filter(brand=search, price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter without end price
                else:
                    # have stuff
                    if ready_deliver:
                        try:
                            price_from = request.GET.get('price_from')
                            model = NotebooksList.objects.filter(brand=search, price__gte=int(price_from),
                                                                 in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = NotebooksList.objects.filter(brand=search, price__gte=int(price_from),
                                                                 in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

            # search  by price without brand
            elif search is None:
                # filter with price with start and end
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = NotebooksList.objects.filter(price__gte=int(price_from),
                                                                 price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            model = NotebooksList.objects.filter(price__gte=int(price_from),
                                                                 price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)
                # filter by price without start price
                elif price_from is None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = NotebooksList.objects.filter(price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            model = NotebooksList.objects.filter(price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter by price without end price
                else:
                    # have stuff
                    if ready_deliver:
                        try:
                            price_from = request.GET.get('price_from')
                            model = NotebooksList.objects.filter(price__gte=int(price_from), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = NotebooksList.objects.filter(price__gte=int(price_from))
                        except Exception:
                            return redirect(request.path)

        # cancel all filter
        if reject_filters:
            model = NotebooksList.objects.all()

        # go to  the detail page
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
                    'cart_sum': cart_sum['product_price__sum'],
                    }
            return render(request, 'main/stuff_detail.html', data)

        price_max = model.aggregate(Max('price'))
        username = request.user
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        data = {'model': model,
                'username': username,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like,
                }
        return render(request, 'main/nothebook.html', data)

    def post(self, request):

        add_comment = request.POST.get('add_comment')
        add_questions = request.POST.get('add_question')
        buy = request.POST.get('buy')
        add_like = request.POST.get('add_like')
        delete_btn = request.POST.get('delete_btn')
        del_like = request.POST.get('del_like')

        if del_like:
            LikeListModel.objects.filter(id=del_like).delete()
            return redirect(request.path)

        if add_like:
            model_add_like = NotebooksList.objects.filter(id=add_like).values()[0]
            username = request.user
            title = model_add_like['title']
            product_pic = model_add_like['pic_link']
            product_price = model_add_like['price']
            product_status = model_add_like['in_out']

            LikeListModel.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                         product_price=product_price, product_status=product_status)

            return redirect(request.path)

        if delete_btn:
            ProductCart.objects.filter(id=delete_btn).delete()
            return redirect(request.path_info)

        if buy:
            model_add_cart = NotebooksList.objects.filter(id=buy).values()[0]
            username = request.user
            title = model_add_cart['title']
            product_pic = model_add_cart['pic_link']
            product_price = model_add_cart['price']
            product_status = model_add_cart['in_out']

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

        detail = request.GET.get('stuff_detail')
        filter = request.GET.get('search')
        reject_filters = request.GET.get('reject_filters')

        if filter:
            ready_deliver = request.GET.get('ready_deliver')
            search = request.GET.get('exampleRadios')
            price_to = request.GET.get('price_to')
            price_from = request.GET.get('price_from')

            if search is not None:
                # filter with start and end price
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = Videocards.objects.filter(brand=search, price__gte=int(price_from),
                                                              price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        try:
                            model = Videocards.objects.filter(brand=search, price__gte=int(price_from),
                                                              price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter without  start price
                elif price_from is None:
                    #  have stuff
                    if ready_deliver:
                        try:
                            model = Videocards.objects.filter(brand=search, price__lte=int(price_to),
                                                              in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have  stuff
                    else:
                        try:
                            model = Videocards.objects.filter(brand=search, price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter without end price
                else:
                    # have stuff
                    if ready_deliver:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Videocards.objects.filter(brand=search, price__gte=int(price_from),
                                                              in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Videocards.objects.filter(brand=search, price__gte=int(price_from),
                                                              in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

            # search  by price without brand
            elif search is None:
                # filter with price with start and end
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = Videocards.objects.filter(price__gte=int(price_from),
                                                              price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            model = Videocards.objects.filter(price__gte=int(price_from),
                                                              price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)
                # filter by price without start price
                elif price_from is None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = Videocards.objects.filter(price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            model = Videocards.objects.filter(price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter by price without end price
                else:
                    # have stuff
                    if ready_deliver:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Videocards.objects.filter(price__gte=int(price_from), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Videocards.objects.filter(price__gte=int(price_from))
                        except Exception:
                            return redirect(request.path)

        # cancel all filter
        if reject_filters:
            model = Videocards.objects.all()

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

        username = request.user
        price_max = model.aggregate(Max('price'))

        """aggregate sum of all cart items"""
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        """Like like all"""
        model_like = LikeListModel.objects.all()

        data = {"model": model,
                'username': username,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like
                }

        return render(request, "main/videocards.html", data)

    @staticmethod
    def post(request):
        add_comment = request.POST.get('add_comment')
        add_question = request.POST.get('add_question')
        buy = request.POST.get('buy')
        add_like = request.POST.get('add_like')
        delete_btn = request.POST.get('delete_btn')
        del_like = request.POST.get('del_like')

        # delete stuff from like list
        if del_like:
            LikeListModel.objects.filter(id=del_like).delete()
            return redirect(request.path)
        # add stuff to list like
        if add_like:
            model_add_like = Videocards.objects.filter(id=add_like).values()[0]
            username = request.user
            title = model_add_like['title']
            product_pic = model_add_like['pic_link']
            product_price = model_add_like['price']
            product_status = model_add_like['in_out']

            LikeListModel.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                         product_price=product_price, product_status=product_status)

            return redirect(request.path)

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

        model = Monitors_list.objects.all()
        model_cart = ProductCart.objects.all()

        detail = request.GET.get('stuff_detail')
        filter = request.GET.get('search')
        reject_filters = request.GET.get('reject_filters')

        if filter:
            search = request.GET.get('exampleRadios')
            ready_deliver = request.GET.get('ready_deliver')
            price_to = request.GET.get('price_to')
            price_from = request.GET.get('price_from')

            if search is not None:
                # filter with start and end price
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = Monitors_list.objects.filter(brand=search, price__gte=int(price_from),
                                                                 price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        try:
                            model = Monitors_list.objects.filter(brand=search, price__gte=int(price_from),
                                                                 price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter without  start price
                elif price_from is None:
                    #  have stuff
                    if ready_deliver:
                        try:
                            model = Monitors_list.objects.filter(brand=search, price__lte=int(price_to),
                                                                 in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have  stuff
                    else:
                        try:
                            model = Monitors_list.objects.filter(brand=search, price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter without end price
                else:
                    # have stuff
                    if ready_deliver:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Monitors_list.objects.filter(brand=search, price__gte=int(price_from),
                                                                 in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Monitors_list.objects.filter(brand=search, price__gte=int(price_from),
                                                                 in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

            # search  by price without brand
            elif search is None:
                # filter with price with start and end
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = Monitors_list.objects.filter(price__gte=int(price_from),
                                                                 price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            model = Monitors_list.objects.filter(price__gte=int(price_from),
                                                                 price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)
                # filter by price without start price
                elif price_from is None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = Monitors_list.objects.filter(price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            model = Monitors_list.objects.filter(price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter by price without end price
                else:
                    # have stuff
                    if ready_deliver:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Monitors_list.objects.filter(price__gte=int(price_from), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Monitors_list.objects.filter(price__gte=int(price_from))
                        except Exception:
                            return redirect(request.path)

        # cancel all filter
        if reject_filters:
            model = Monitors_list.objects.all()

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

        price_max = model.aggregate(Max('price'))
        username = request.user

        """aggregate sum of all cart items"""
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        """Like like all"""
        model_like = LikeListModel.objects.all()

        data = {'username': username,
                'model': model,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like
                }
        return render(request, 'main/displays.html', data)

    def post(self, request):
        add_comment = request.POST.get('add_comment')
        add_question = request.POST.get('add_question')
        buy = request.POST.get('buy')
        add_like = request.POST.get('add_like')
        delete_btn = request.POST.get('delete_btn')
        del_like = request.POST.get('del_like')

        # delete stuff from like list
        if del_like:
            LikeListModel.objects.filter(id=del_like).delete()
            return redirect(request.path)

        if add_like:
            model_add_like = Monitors_list.objects.filter(id=add_like).values()[0]
            username = request.user
            title = model_add_like['title']
            product_pic = model_add_like['pic_link']
            product_price = model_add_like['price']
            product_status = model_add_like['in_out']

            LikeListModel.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                         product_price=product_price, product_status=product_status)

            return redirect(request.path)

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

        model = Memory_list.objects.all()
        model_cart = ProductCart.objects.all()

        detail = request.GET.get('stuff_detail')
        filter = request.GET.get('search')
        reject_filters = request.GET.get('reject_filters')

        if filter:
            search = request.GET.get('exampleRadios')
            ready_deliver = request.GET.get('ready_deliver')
            price_to = request.GET.get('price_to')
            price_from = request.GET.get('price_from')

            if search is not None:
                # filter with start and end price
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = Memory_list.objects.filter(brand=search, price__gte=int(price_from),
                                                               price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        try:
                            model = Memory_list.objects.filter(brand=search, price__gte=int(price_from),
                                                               price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter without  start price
                elif price_from is None:
                    #  have stuff
                    if ready_deliver:
                        try:
                            model = Memory_list.objects.filter(brand=search, price__lte=int(price_to),
                                                               in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have  stuff
                    else:
                        try:
                            model = Memory_list.objects.filter(brand=search, price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter without end price
                else:
                    # have stuff
                    if ready_deliver:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Memory_list.objects.filter(brand=search, price__gte=int(price_from),
                                                               in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Memory_list.objects.filter(brand=search, price__gte=int(price_from),
                                                               in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

            # search  by price without brand
            elif search is None:
                # filter with price with start and end
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = Memory_list.objects.filter(price__gte=int(price_from),
                                                               price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            model = Memory_list.objects.filter(price__gte=int(price_from),
                                                               price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)
                # filter by price without start price
                elif price_from is None:
                    # have stuff
                    if ready_deliver:
                        try:
                            model = Memory_list.objects.filter(price__lte=int(price_to), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            model = Memory_list.objects.filter(price__lte=int(price_to))
                        except Exception:
                            return redirect(request.path)

                # filter by price without end price
                else:
                    # have stuff
                    if ready_deliver:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Memory_list.objects.filter(price__gte=int(price_from), in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = Memory_list.objects.filter(price__gte=int(price_from))
                        except Exception:
                            return redirect(request.path)

        # cancel all filter
        if reject_filters:
            model = Memory_list.objects.all()

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

        price_max = model.aggregate(Max('price'))
        username = request.user

        """aggregate sum of all cart items"""
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        """Like like all"""
        model_like = LikeListModel.objects.all()

        data = {'username': username,
                'model': model,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like
                }

        return render(request, 'main/memory.html', data)

    def post(self, request):
        add_comment = request.POST.get('add_comment')
        add_question = request.POST.get('add_question')
        buy = request.POST.get('buy')
        add_like = request.POST.get('add_like')
        delete_btn = request.POST.get('delete_btn')
        del_like = request.POST.get('del_like')

        # delete stuff from like list
        if del_like:
            LikeListModel.objects.filter(id=del_like).delete()
            return redirect(request.path)

        if add_like:
            model_add_like = Memory_list.objects.filter(id=add_like).values()[0]
            username = request.user
            title = model_add_like['title']
            product_pic = model_add_like['pic_link']
            product_price = model_add_like['price']
            product_status = model_add_like['in_out']

            LikeListModel.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                         product_price=product_price, product_status=product_status)

            return redirect(request.path)

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


class CartApi(generics.GenericAPIView,
              mixins.CreateModelMixin,
              mixins.ListModelMixin):
    queryset = ProductCart.objects.all()
    serializer_class = CartApiSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
