import random

from django.shortcuts import render, redirect
from rest_framework import generics, mixins, permissions
from django.contrib.auth import authenticate, login
from .serializers import NothebooksSerializer, CommentUserSerializer, CartApiSerializer, DocumentOfSoldSerializer
from .models import *
from .forms import RegistrationUser
from django.db.models import Sum, Max
from django.contrib import messages


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
            else:
                messages.error(request, 'Неправельний логін або пароль!!!')
                return redirect('main')
        username = request.user
        model_cart = ProductCart.objects.all()

        '''cart_total_price'''
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        """Like like all"""
        model_like = LikeListModel.objects.all()

        """conditional of like_modal"""
        like_modal_status = 0

        """conditional of modal_cart"""
        cart_modal_status = 0

        data = {'username': username,
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like,
                'like_modal_status': like_modal_status,
                'cart_modal_status': cart_modal_status
                }
        return render(request, 'main/main_page.html', data)

    @staticmethod
    def post(request):
        delete_btn = request.POST.get('delete_btn')
        del_like = request.POST.get('del_like')
        username = request.user

        if del_like:
            try:
                '''cart_all_items'''
                model_cart = ProductCart.objects.all()

                """Like like all"""
                model_like = LikeListModel.objects.all()

                LikeListModel.objects.filter(id=del_like).delete()
                like_modal_status = 1
                cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

                data = {
                    'username': username,
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'like_modal_status': like_modal_status
                }

                return render(request, 'main/main_page.html', data)

            except Exception:
                return redirect(request.path)

        if delete_btn:
            try:
                '''cart_all_items'''
                model_cart = ProductCart.objects.all()

                """Like like all"""
                model_like = LikeListModel.objects.all()

                ProductCart.objects.filter(id=delete_btn).delete()
                cart_modal_status = 1
                cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

                data = {
                    'username': username,
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'cart_modal_status': cart_modal_status
                }

                return render(request, 'main/main_page.html', data)

            except Exception:
                return redirect('main')


class Registration(generics.GenericAPIView,
                   mixins.CreateModelMixin):

    @staticmethod
    def get(request):
        form = RegistrationUser
        data = {"form": form}
        return render(request, "main/registration.html", data)

    @staticmethod
    def post(request):
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

        filter_stuff = request.GET.get('filter_stuff')

        if filter_stuff:
            model = NotebooksList.objects.filter(brand=filter_stuff)

        if filter:
            ready_deliver = request.GET.get('ready_deliver')
            search = request.GET.get('exampleRadios')
            price_to = request.GET.get('price_to')
            price_from = request.GET.get('price_from')
            processor = request.GET.get('processor')

            if search is not None:
                # filter with start and end price
                if all([(price_from is not None), (price_to is not None), processor]):
                    # have stuff
                    if ready_deliver:
                        try:
                            model = NotebooksList.objects.filter(brand=search, price__gte=int(price_from),
                                                                 price__lte=int(price_to), in_out='Є в наявності',
                                                                 processor=processor)
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        if processor is not None:
                            try:
                                model = NotebooksList.objects.filter(brand=search, price__gte=int(price_from),
                                                                     price__lte=int(price_to), processor=processor)
                            except Exception:
                                return redirect(request.path)
                        else:
                            try:
                                model = NotebooksList.objects.filter(brand=search, price__gte=int(price_from),
                                                                     price__lte=int(price_to))
                            except Exception:
                                return redirect(request.path)

                # filter without  start price
                elif all([(price_from is None), (processor is not None)]):
                    #  have stuff
                    if ready_deliver:
                        try:
                            model = NotebooksList.objects.filter(brand=search, price__lte=int(price_to),
                                                                 in_out='Є в наявності', processor=processor)
                        except Exception:
                            return redirect(request.path)

                    # don't have  stuff
                    else:
                        if processor is not None:
                            try:
                                model = NotebooksList.objects.filter(brand=search, price__lte=int(price_to),
                                                                     processor=processor)
                            except Exception:
                                return redirect(request.path)
                        else:
                            try:
                                model = NotebooksList.objects.filter(brand=search, price__lte=int(price_to),
                                                                     )
                            except Exception:
                                return redirect(request.path)

                # filter without end price
                else:
                    # have stuff
                    if ready_deliver and processor:
                        try:
                            price_from = request.GET.get('price_from')
                            model = NotebooksList.objects.filter(brand=search, price__gte=int(price_from),
                                                                 in_out='Є в наявності', processor=processor)
                        except Exception:
                            return redirect(request.path)

                    # don't have stuff
                    else:
                        if processor:
                            try:
                                price_from = request.GET.get('price_from')
                                model = NotebooksList.objects.filter(brand=search, price__gte=int(price_from),
                                                                     in_out='Є в наявності', processor=processor)
                            except Exception:
                                return redirect(request.path)
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
                if all([(price_from is not None), (price_to is not None), processor]):
                    # have stuff
                    if ready_deliver:
                        try:
                            model = NotebooksList.objects.filter(price__gte=int(price_from),
                                                                 price__lte=int(price_to), in_out='Є в наявності',
                                                                 processor=processor)
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        if processor:
                            try:
                                model = NotebooksList.objects.filter(price__gte=int(price_from),
                                                                     price__lte=int(price_to), processor=processor)
                            except Exception:
                                return redirect(request.path)
                        else:
                            if processor:
                                try:
                                    model = NotebooksList.objects.filter(price__gte=int(price_from),
                                                                         price__lte=int(price_to))
                                except Exception:
                                    return redirect(request.path)

                # filter by price without start price
                elif all([(price_from is None), (price_to is not None), processor]):
                    # have stuff
                    if all([ready_deliver, processor]):
                        try:
                            model = NotebooksList.objects.filter(price__lte=int(price_to), in_out='Є в наявності',
                                                                 processor=processor)
                        except Exception:
                            return redirect(request.path)
                    # don't have
                    else:
                        if all([(price_to is not None), processor]):
                            try:
                                model = NotebooksList.objects.filter(price__lte=int(price_to), processor=processor)
                            except Exception:
                                return redirect(request.path)
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
            curent_url = request.path

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
                    'current_url': curent_url
                    }
            return render(request, 'main/stuff_detail.html', data)

        price_max = model.aggregate(Max('price'))
        username = request.user
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        """conditional of modal_like"""
        like_modal_status = 0

        """conditional of cart_modal"""
        cart_modal_status = 0

        data = {'model': model,
                'username': username,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like,
                'like_modal_status': like_modal_status,
                'cart_modal_status': cart_modal_status
                }
        return render(request, 'main/nothebook.html', data)

    @staticmethod
    def post(request):
        add_comment = request.POST.get('add_comment')
        add_questions = request.POST.get('add_question')
        buy = request.POST.get('buy')
        add_like = request.POST.get('add_like')
        delete_btn = request.POST.get('delete_btn')
        del_like = request.POST.get('del_like')

        if del_like:
            model = NotebooksList.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            LikeListModel.objects.filter(id=del_like).delete()
            like_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'like_modal_status': like_modal_status
                    }

            return render(request, 'main/nothebook.html', data)

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
            model = NotebooksList.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            ProductCart.objects.filter(id=delete_btn).delete()
            cart_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'cart_modal_status': cart_modal_status
                    }

            return render(request, 'main/nothebook.html', data)

        if buy:
            model_add_cart = NotebooksList.objects.filter(id=buy, ).values()[0]
            username = request.user
            title = model_add_cart['title']
            product_pic = model_add_cart['pic_link']
            product_price = model_add_cart['price']
            product_status = model_add_cart['in_out']

            if product_status == 'Є в наявності':
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

        filter_stuff = request.GET.get('filter_stuff')

        if filter_stuff:
            model = Videocards.objects.filter(brand=filter_stuff)

        if filter:
            ready_deliver = request.GET.get('ready_deliver')
            search = request.GET.get('exampleRadios')
            price_to = request.GET.get('price_to')
            price_from = request.GET.get('price_from')

            if search is not None:
                # filter with start and end price
                if all([(price_from is not None), (price_to is not None)]):
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
                    if all([ready_deliver, (price_from is not None)]):
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
                    if all([ready_deliver, (price_from is not None)]):
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
                                                              )
                        except Exception:
                            return redirect(request.path)

            # search  by price without brand
            elif search is None:
                # filter with price with start and end
                if all([(price_from is not None), (price_to is not None), ready_deliver]):
                    # have stuff
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
            curent_url = request.path

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
                    'cart_sum': cart_sum['product_price__sum'],
                    'current_url': curent_url
                    }
            return render(request, 'main/stuff_detail.html', data)

        username = request.user
        price_max = model.aggregate(Max('price'))

        """aggregate sum of all cart items"""
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        """Like like all"""
        model_like = LikeListModel.objects.all()

        """condition of modal_like"""
        like_modal_status = 0

        """conditional of modal_like"""
        cart_modal_status = 0

        data = {"model": model,
                'username': username,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like,
                'like_modal_status': like_modal_status,
                'cart_modal_status': cart_modal_status
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
            model = Videocards.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            LikeListModel.objects.filter(id=del_like).delete()
            like_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'like_modal_status': like_modal_status
                    }

            return render(request, 'main/videocards.html', data)

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
            model = Videocards.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            ProductCart.objects.filter(id=delete_btn).delete()
            cart_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'cart_modal_status': cart_modal_status
                    }

            return render(request, 'main/videocards.html', data)

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

        filter_stuff = request.GET.get('filter_stuff')

        if filter_stuff:
            model = Monitors_list.objects.filter(brand=filter_stuff)

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
            curent_url = request.path

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
                    'cart_sum': cart_sum['product_price__sum'],
                    'current_url': curent_url
                    }
            return render(request, 'main/stuff_detail.html', data)

        price_max = model.aggregate(Max('price'))
        username = request.user

        """aggregate sum of all cart items"""
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        """Like like all"""
        model_like = LikeListModel.objects.all()

        """conditional of modal_like"""
        like_modal_status = 0

        """conditional of modal_cart"""
        cart_modal_status = 0

        data = {'username': username,
                'model': model,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like,
                'like_modal_status': like_modal_status,
                'cart_modal_status': cart_modal_status
                }
        return render(request, 'main/displays.html', data)

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
            model = Monitors_list.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            LikeListModel.objects.filter(id=del_like).delete()
            like_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'like_modal_status': like_modal_status
                    }

            return render(request, 'main/displays.html', data)

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
            model = Monitors_list.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            ProductCart.objects.filter(id=delete_btn).delete()
            cart_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'cart_modal_status': cart_modal_status
                    }

            return render(request, 'main/displays.html', data)

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

        filter_stuff = request.GET.get('filter_stuff')

        if filter_stuff:
            model = Memory_list.objects.filter(brand=filter_stuff)

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
            curent_url = request.path

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
                    'cart_sum': cart_sum['product_price__sum'],
                    'current_url': curent_url
                    }
            return render(request, 'main/stuff_detail.html', data)

        price_max = model.aggregate(Max('price'))
        username = request.user

        """aggregate sum of all cart items"""
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        """Like like all"""
        model_like = LikeListModel.objects.all()

        """condition of like_modal"""
        like_modal_status = 0

        """conditional of cart_modal"""
        cart_modal_status = 0

        data = {'username': username,
                'model': model,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like,
                'like_modal_status': like_modal_status,
                'cart_modal_status': cart_modal_status
                }

        return render(request, 'main/memory.html', data)

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
            model = Memory_list.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            LikeListModel.objects.filter(id=del_like).delete()
            like_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'like_modal_status': like_modal_status
                    }
            return render(request, 'main/memory.html', data)

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
            model = Memory_list.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            ProductCart.objects.filter(id=delete_btn).delete()
            cart_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'cart_modal_status': cart_modal_status
                    }

            return render(request, 'main/memory.html', data)

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


class HardDisk(generics.GenericAPIView):

    @staticmethod
    def get(request):
        model = HardDiskLists.objects.all()
        model_cart = ProductCart.objects.all()

        detail = request.GET.get('stuff_detail')
        filter = request.GET.get('search')
        reject_filters = request.GET.get('reject_filters')

        filter_stuff = request.GET.get('filter_stuff')

        if filter_stuff:
            model = HardDiskLists.objects.filter(brand=filter_stuff)

        if filter:
            search = request.GET.get('exampleRadios')
            ready_deliver = request.GET.get('ready_deliver')
            price_to = request.GET.get('price_to')
            price_from = request.GET.get('price_from')
            memory_size = request.GET.get('memory_size')

            if search is not None:
                # filter with start and end price
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        if memory_size:
                            try:
                                model = HardDiskLists.objects.filter(brand=search, price__gte=int(price_from),
                                                                     price__lte=int(price_to), in_out='Є в наявності',
                                                                     size=memory_size)
                            except Exception:
                                return redirect(request.path)
                        else:
                            model = HardDiskLists.objects.filter(brand=search, price__gte=int(price_from),
                                                                 price__lte=int(price_to), in_out='Є в наявності',
                                                                 )

                    # don't have stuff
                    else:
                        if memory_size:
                            try:
                                model = HardDiskLists.objects.filter(brand=search, price__gte=int(price_from),
                                                                     price__lte=int(price_to), size=memory_size)
                            except Exception:
                                return redirect(request.path)
                        else:
                            model = HardDiskLists.objects.filter(brand=search, price__gte=int(price_from),
                                                                 price__lte=int(price_to))

                # filter without  start price
                elif price_from is None:
                    #  have stuff
                    if ready_deliver:
                        if memory_size:
                            try:
                                model = HardDiskLists.objects.filter(brand=search, price__lte=int(price_to),
                                                                     in_out='Є в наявності', size=memory_size)
                            except Exception:
                                return redirect(request.path)

                    # don't have  stuff
                    else:
                        try:
                            model = HardDiskLists.objects.filter(brand=search, price__lte=int(price_to),
                                                                 )
                        except Exception:
                            return redirect(request.path)

                # filter without end price
                else:
                    # have stuff
                    if ready_deliver:
                        if memory_size:
                            try:
                                price_from = request.GET.get('price_from')
                                model = HardDiskLists.objects.filter(brand=search, price__gte=int(price_from),
                                                                     in_out='Є в наявності', size=memory_size)
                            except Exception:
                                return redirect(request.path)

                    # don't have stuff
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = HardDiskLists.objects.filter(brand=search, price__gte=int(price_from),
                                                                 in_out='Є в наявності')
                        except Exception:
                            return redirect(request.path)

            # search  by price without brand
            elif search is None:
                # filter with price with start and end
                if price_from is not None and price_to is not None:
                    # have stuff
                    if ready_deliver:
                        if memory_size:
                            try:
                                model = HardDiskLists.objects.filter(price__gte=int(price_from),
                                                                     price__lte=int(price_to), in_out='Є в наявності',
                                                                     size=memory_size
                                                                     )
                            except Exception:
                                return redirect(request.path)
                        else:
                            try:
                                model = HardDiskLists.objects.filter(price__gte=int(price_from),
                                                                     price__lte=int(price_to), in_out='Є в наявності',
                                                                     )
                            except Exception:
                                return redirect(request.path)
                    # don't have stuff
                    else:
                        if memory_size:
                            try:
                                model = HardDiskLists.objects.filter(price__gte=int(price_from),
                                                                     price__lte=int(price_to), size=memory_size)
                            except Exception:
                                return redirect(request.path)
                        else:
                            try:
                                model = HardDiskLists.objects.filter(price__gte=int(price_from),
                                                                     price__lte=int(price_to))
                            except Exception:
                                return redirect(request.path)

                # filter by price without start price
                elif price_from is None:
                    # have stuff
                    if ready_deliver:
                        if memory_size:
                            try:
                                model = HardDiskLists.objects.filter(price__lte=int(price_to), in_out='Є в наявності',
                                                                     size=memory_size)
                            except Exception:
                                return redirect(request.path)
                    # don't have
                    else:
                        try:
                            model = HardDiskLists.objects.filter(price__lte=int(price_to), size=memory_size)
                        except Exception:
                            return redirect(request.path)

                # filter by price without end price
                else:
                    # have stuff
                    if ready_deliver:
                        if memory_size:
                            try:
                                price_from = request.GET.get('price_from')
                                model = HardDiskLists.objects.filter(price__gte=int(price_from), in_out='Є в наявності',
                                                                     size=memory_size)
                            except Exception:
                                return redirect(request.path)
                    # don't have
                    else:
                        try:
                            price_from = request.GET.get('price_from')
                            model = HardDiskLists.objects.filter(price__gte=int(price_from), size=memory_size)
                        except Exception:
                            return redirect(request.path)

        # cancel all filter
        if reject_filters:
            model = HardDiskLists.objects.all()

        if detail:
            model_rating = CommentsUserMemory.objects.filter(name_of_stuff=detail).values('rating')
            curent_url = request.path

            avr_rating = 0
            for el in model_rating:
                res = el['rating']
                if res is not None:
                    avr_rating += int(res)
                else:
                    res = 0
                    avr_rating += res

            model = HardDiskLists.objects.filter(id=detail)
            model_1 = CommentsUserHardDisk.objects.filter(name_of_stuff=HardDiskLists(detail)).values('rating',
                                                                                                      'name_of_user',
                                                                                                      'comment',
                                                                                                      'link_video',
                                                                                                      'date')
            model_2 = QuestionUsersHardDisk.objects.filter(name_of_stuff=HardDiskLists(detail)).values('name_of_user',
                                                                                                       'comment',
                                                                                                       'date')

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
                    'cart_sum': cart_sum['product_price__sum'],
                    'current_url': curent_url
                    }
            return render(request, 'main/stuff_detail.html', data)

        price_max = model.aggregate(Max('price'))
        username = request.user

        """aggregate sum of all cart items"""
        cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

        """Like like all"""
        model_like = LikeListModel.objects.all()

        """condition of like_modal"""
        like_modal_status = 0

        """conditional of cart_modal"""
        cart_modal_status = 0

        data = {'username': username,
                'model': model,
                'price_max': price_max['price__max'],
                'model_cart': model_cart,
                'cart_sum': cart_sum['product_price__sum'],
                'model_like': model_like,
                'like_modal_status': like_modal_status,
                'cart_modal_status': cart_modal_status
                }
        return render(request, "main/hard_disk_list.html", data)

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
            model = HardDiskLists.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            LikeListModel.objects.filter(id=del_like).delete()
            like_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'like_modal_status': like_modal_status
                    }
            return render(request, 'main/hard_disk_list.html', data)

        if add_like:
            model_add_like = HardDiskLists.objects.filter(id=add_like).values()[0]
            username = request.user
            title = model_add_like['title']
            product_pic = model_add_like['pic_link']
            product_price = model_add_like['price']
            product_status = model_add_like['in_out']

            LikeListModel.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                         product_price=product_price, product_status=product_status)

            return redirect(request.path)

        if delete_btn:
            model = HardDiskLists.objects.all()
            '''cart_all_items'''
            model_cart = ProductCart.objects.all()

            """Like like all"""
            model_like = LikeListModel.objects.all()

            ProductCart.objects.filter(id=delete_btn).delete()
            cart_modal_status = 1
            price_max = model.aggregate(Max('price'))
            username = request.user
            cart_sum = ProductCart.objects.filter(user_name__username=username).aggregate(Sum('product_price'))

            data = {'model': model,
                    'username': username,
                    'price_max': price_max['price__max'],
                    'model_cart': model_cart,
                    'cart_sum': cart_sum['product_price__sum'],
                    'model_like': model_like,
                    'cart_modal_status': cart_modal_status
                    }

            return render(request, 'main/hard_disk_list.html', data)

        if buy:
            test = HardDiskLists.objects.filter(id=buy).values()[0]
            username = request.user
            title = test['title']
            product_pic = test['pic_link']
            product_price = test['price']
            product_status = test['in_out']

            ProductCart.objects.create(user_name=username, product_title=title, product_pic=product_pic,
                                       product_price=product_price, product_status=product_status)

            return redirect('hard_disk')

        if add_comment:
            username = request.user
            rating = request.POST.get('simple-rating')
            stuff_name = request.POST.get('add_comment')
            comment = request.POST.get('comment')
            link_video = request.POST.get('link_video')
            CommentsUserHardDisk.objects.create(rating=rating, name_of_user=username,
                                                name_of_stuff=HardDiskLists(stuff_name),
                                                comment=comment, link_video=link_video)
            model = HardDiskLists.objects.filter(id=stuff_name)
            model_1 = CommentsUserHardDisk.objects.filter(name_of_stuff=HardDiskLists(stuff_name)).values('rating',
                                                                                                          'name_of_user',
                                                                                                          'comment',
                                                                                                          'date')
            model_2 = QuestionUsersHardDisk.objects.filter(name_of_stuff=HardDiskLists(stuff_name)).values(
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
            QuestionUsersHardDisk.objects.create(name_of_user=username, name_of_stuff=HardDiskLists(stuff_name),
                                                 comment=comment)
            model = HardDiskLists.objects.filter(id=stuff_name)
            model_1 = CommentsUserHardDisk.objects.filter(name_of_stuff=HardDiskLists(stuff_name)).values(
                'name_of_user',
                'comment',
                'date')

            model_2 = QuestionUsersHardDisk.objects.filter(name_of_stuff=HardDiskLists(stuff_name)).values(
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


"""Buy_form"""


class Checkout(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        try:
            if user:
                model = ProductCart.objects.filter(user_name=user).values('product_pic', 'product_price',
                                                                          'product_title')
                curt_sum = ProductCart.objects.filter(user_name=user).aggregate(Sum('product_price'))

                data = {'model': model,
                        'curt_sum': curt_sum['product_price__sum']}

                return render(request, 'main/checkout.html', data)
        except Exception:
            return render(request, 'main/checkout.html')

    @staticmethod
    def post(request):
        order = request.POST.get('order')
        if order:
            user = request.user
            name = request.POST.get('client_name')
            sur_name = request.POST.get('client_surname')
            client_phone = request.POST.get('client_phone')
            client_email = request.POST.get('client_email')
            state = request.POST.get('state')
            city = request.POST.get('city')
            num_of_post = request.POST.get('post_num')
            model = ProductCart.objects.filter(user_name=user).values('product_pic', 'product_price', 'product_title')
            order_num = random.randint(1, 150000)
            for el in range(len(model)):
                product_pic = model[el]['product_pic']
                product_price = model[el]['product_price']
                product_title = model[el]['product_title']
                OrderList.objects.create(username=user, name=name, sur_name=sur_name, mobile_number=client_phone,
                                         email=client_email, state=state, city=city, num_of_post=num_of_post,
                                         product_pic=product_pic, product_price=product_price,
                                         product_title=product_title,
                                         order_num=order_num)
                ProductCart.objects.filter(product_title=product_title).delete()

        return redirect('main')


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


"""CRM main page"""


class AdminPanelStartPage(generics.GenericAPIView,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          ):
    serializer_class = DocumentOfSoldSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        order_username = request.GET.get('order_username')
        model = OrderList.objects.all()
        total_sum = OrderList.objects.aggregate(Sum('product_price'))['product_price__sum']

        options = request.GET.get('options')

        personal_data = None

        test = User.objects.filter(username=request.user).values('is_superuser', 'groups')
        if any([(test[0]['is_superuser'] == True), (test[0]['groups'] == 1)]):
            if order_username:
                model_user = User.objects.filter(username=options).values('id')[0]['id']
                model = OrderList.objects.filter(username=model_user)
                print(model)
                total_sum = OrderList.objects.filter(username=model_user).aggregate(Sum('product_price'))[
                        'product_price__sum']

                personal_data = OrderList.objects.filter(username=model_user).values()[0]

        data = {'model': model,
                'total_sum': total_sum,
                'username': options,
                'personal_data': personal_data,
                }

        if any([(test[0]['is_superuser'] == True), (test[0]['groups'] == 1)]):
            return render(request, "main/AdminPanelStartPage.html", data)
        else:
            return render(request, "main/errors_pages/500_code.html")


    @staticmethod
    def post(request):
        model = OrderList.objects.all()
        total_sum = OrderList.objects.aggregate(Sum('product_price'))['product_price__sum']

        sold_order = request.POST.get('sold')

        if sold_order:
            username = User.objects.filter(username=sold_order).values('id')[0]['id']
            model_order = OrderList.objects.filter(username=username).values()
            print(model_order)
            for el in model_order:
                name = el['name']
                sur_name = el['sur_name']
                mobile_number = el['mobile_number']
                email = el['email']
                product_title = el['product_title']
                product_pic = el['product_pic']
                product_price = el['product_price']
                order_num = el['order_num']

                DocumentOfSold.objects.create(username=username, name=name, sur_name=sur_name,
                                              product_title=product_title, mobile_number=mobile_number, email=email,
                                              product_pic=product_pic, product_price=product_price, order_num=order_num)

                OrderList.objects.filter(id=el['id']).delete()

        data = {'model': model,
                'total_sum': total_sum
                }

        return render(request, "main/AdminPanelStartPage.html", data)