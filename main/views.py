from django.shortcuts import render, redirect
from rest_framework import generics, mixins, permissions
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
from .forms import *

from django.middleware.csrf import get_token


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
        data = {'username': username}
        return render(request, 'main/main_page.html', data)


class Registration(generics.GenericAPIView,
                   mixins.CreateModelMixin):

    @staticmethod
    def get(request):
        form = RegistrationUser
        data = {"form": form}
        return render(request, "main/registration.html", data)

    def post(self, request):
        form = RegistrationUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')


class DetailInfo(generics.GenericAPIView):
    @staticmethod
    def get(request):
        return render(request, 'main/stuff_detail.html')


class Nothebooks(generics.GenericAPIView):
    @staticmethod
    def get(request):
        model = NotebooksList.objects.all()

        search = request.GET.get('exampleRadios')
        detail = request.GET.get('stuff_detail')

        if detail:
            model = NotebooksList.objects.filter(id=detail)
            model_1 = CommentsUsers.objects.filter(name_of_stuff=NotebooksList(detail)).values('name_of_user',
                                                                                               'comment', 'date')
            model_2 = QuestionUsers.objects.filter(name_of_stuff=NotebooksList(detail)).values('name_of_user',
                                                                                               'comment', 'date')
            quentety = len(model_1)
            quentety_1 = len(model_2)
            username = request.user
            data = {'model': model,
                    'model_1': model_1,
                    'model_2': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1
                    }
            return render(request, 'main/stuff_detail.html', data)

        if search:
            if search == "Apple":
                model = NotebooksList.objects.filter(brand='Apple')
                data = {'model': model}
                return render(request, 'main/nothebook.html', data)

            elif search == "Acer":
                model = NotebooksList.objects.filter(brand='Acer')
                data = {'model': model}
                return render(request, 'main/nothebook.html', data)

            elif search == "Asus":
                model = NotebooksList.objects.filter(brand='Asus')
                data = {'model': model}
                return render(request, 'main/nothebook.html', data)

        username = request.user
        videocard = 'videocard'
        data = {'model': model,
                'username': username,
                }
        return render(request, 'main/nothebook.html', data)

    def post(self, request):
        add_comment = request.POST.get('add_comment')
        add_questions = request.POST.get('add_question')
        if add_comment:
            username = request.user
            stuff_name = request.POST.get('add_comment')
            comment = request.POST.get('comment')
            CommentsUsers.objects.create(name_of_user=username, name_of_stuff=NotebooksList(stuff_name),
                                         comment=comment)
            model = NotebooksList.objects.filter(id=stuff_name)
            model_1 = CommentsUsers.objects.filter(name_of_stuff=NotebooksList(stuff_name)).values('name_of_user',
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
            model_1 = CommentsUsers.objects.filter(name_of_stuff=NotebooksList(stuff_name)).values('name_of_user',
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
        search = request.GET.get('exampleRadios')
        detail = request.GET.get('stuff_detail')

        if detail:
            model = Videocards.objects.filter(id=detail)
            model_1 = CommentsUsersVideocard.objects.filter(name_of_stuff=Videocards(detail)).values('name_of_user',
                                                                                                     'comment',
                                                                                                     'date')
            model_2 = QuestionUsersVideocard.objects.filter(name_of_stuff=Videocards(detail)).values('name_of_user',
                                                                                                     'comment',
                                                                                                     'date')
            quentety = len(model_1)
            quentety_1 = len(model_2)
            username = request.user
            data = {'model': model,
                    'model_1': model_1,
                    'model_2': model_2,
                    'username': username,
                    'quentety': quentety,
                    'quentety_1': quentety_1
                    }
            return render(request, 'main/stuff_detail.html', data)

        if search == "AMD":
            model = Videocards.objects.filter(brand='AMD')
            data = {'model': model}
            return render(request, "main/videocards.html", data)

        elif search == "Gigabyte":
            model = Videocards.objects.filter(brand='Gigabyte')
            data = {'model': model}
            return render(request, "main/videocards.html", data)

        elif search == "Asus":
            model = Videocards.objects.filter(brand='Asus')
            data = {'model': model}
            return render(request, "main/videocards.html", data)

        elif search == "INNO3D":
            model = Videocards.objects.filter(brand='INNO3D')
            data = {'model': model}
            return render(request, "main/videocards.html", data)

        elif search == "MSI":
            model = Videocards.objects.filter(brand='MSI')
            data = {'model': model}
            return render(request, "main/videocards.html", data)

        model = Videocards.objects.all()
        username = request.user
        data = {"model": model,
                'username': username}

        return render(request, "main/videocards.html", data)

    def post(self, request):
        add_comment = request.POST.get('add_comment')
        add_question = request.POST.get('add_question')

        if add_comment:
            username = request.user
            stuff_name = request.POST.get('add_comment')
            comment = request.POST.get('comment')
            CommentsUsersVideocard.objects.create(name_of_user=username, name_of_stuff=Videocards(stuff_name),
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
