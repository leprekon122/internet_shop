from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class NotebooksList(models.Model):
    in_out_list = (('Є в наявності', 'Є в наявності'),
                   ('Немає в наявності', 'Немає в наявності'))

    list_of_brand = (('Apple', 'Apple'),
                     ('Acer', 'Acer'),
                     ('Asus', 'Asus'),
                     ('Dell', 'Dell'),
                     ('HP', 'HP'),
                     ('Lenovo', 'Lenovo'),
                     ('MSI', 'MSI'),
                     ('Razer', 'Razer'),
                     ('Samsung', 'Samsung')
                     )

    brand = models.CharField(max_length=60, choices=list_of_brand, default='brand')
    title = models.CharField(max_length=255)
    video_link = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='notebooks_pic')
    pic_link = models.TextField(null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    in_out = models.CharField(max_length=255, choices=in_out_list)


class Videocards(models.Model):
    in_out_list = (('Є в наявності', 'Є в наявності'),
                   ('Немає в наявності', 'Немає в наявності'))

    list_of_brand = (('AMD', 'AMD'),
                     ('Gigabyte', 'Gigabyte'),
                     ('Asus', 'Asus'),
                     ('INNO3D', 'INNO3D'),
                     ('MSI', 'MSI'),
                     )

    brand = models.CharField(max_length=60, choices=list_of_brand, default='brand')
    title = models.CharField(max_length=255)
    video_link = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='videocards_pic')
    pic_link = models.TextField(null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    in_out = models.CharField(max_length=255, choices=in_out_list)

    def __str__(self):
        return f"{self.brand} {self.title} {self.video_link} {self.pic} {self.description} {self.price} {self.in_out}"


class Monitors_list(models.Model):
    in_out_list = (('Є в наявності', 'Є в наявності'),
                   ('Немає в наявності', 'Немає в наявності'))

    list_of_brand = (('Asus', 'Asus'),
                     ('Acer', 'Acer'),
                     ('BenQ', 'BenQ'),
                     ('Dell', 'Dell'),
                     ('LG', 'LG'),
                     )

    brand = models.CharField(max_length=60, choices=list_of_brand)
    title = models.CharField(max_length=255)
    video_link = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='monitors_pic')
    pic_link = models.TextField(null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    in_out = models.CharField(max_length=255, choices=in_out_list)

    def __str__(self):
        return f"{self.brand} {self.title} {self.video_link} {self.pic}" \
               f" {self.pic_link} {self.description} {self.price} {self.in_out}"

    class Meta:
        verbose_name = 'display'
        verbose_name_plural = "display's"


class Memory_list(models.Model):
    in_out_list = (('Є в наявності', 'Є в наявності'),
                   ('Немає в наявності', 'Немає в наявності'))

    list_of_brand = (('AMD', 'AMD'),
                     ('Crucial', 'Crucial'),
                     ('HyperX', 'HyperX'),
                     ('Kingston', 'Kingston'),
                     ('Samsung', 'Samsung'),
                     )

    brand = models.CharField(max_length=60, choices=list_of_brand)
    title = models.CharField(max_length=255)
    video_link = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='monitors_pic')
    pic_link = models.TextField(null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    in_out = models.CharField(max_length=255, choices=in_out_list)

    def __str__(self):
        return f"{self.brand} {self.title} {self.video_link} {self.pic}" \
               f" {self.pic_link} {self.description} {self.price} {self.in_out}"

    class Meta:
        verbose_name = 'Memory_list'
        verbose_name_plural = "Memory_list"


class CommentsUsers(models.Model):
    rating_choice = (('1', '1'),
                     ('2', '2'),
                     ('3', '3'),
                     ('4', '4'),
                     ('5', '5')
                     )
    rating = models.CharField(max_length=15, choices=rating_choice, null=True, blank=True)
    name_of_user = models.CharField(max_length=50, null=True)
    name_of_stuff = models.ForeignKey(NotebooksList, on_delete=models.CASCADE)
    comment = models.TextField()
    link_video = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date} {self.rating}"

    class Meta:
        verbose_name = 'CommentsUsers'
        verbose_name_plural = 'CommentsUsers'


class QuestionUsers(models.Model):
    name_of_user = models.CharField(max_length=50)
    name_of_stuff = models.ForeignKey(NotebooksList, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date}"

    class Meta:
        verbose_name = 'QuestionUsers'
        verbose_name_plural = 'QuestionUsers'


class CommentsUsersVideocard(models.Model):
    rating_choice = (('1', '1'),
                     ('2', '2'),
                     ('3', '3'),
                     ('4', '4'),
                     ('5', '5')
                     )

    rating = models.CharField(max_length=15, choices=rating_choice, null=True, blank=True)
    name_of_user = models.CharField(max_length=50, null=True)
    name_of_stuff = models.ForeignKey(Videocards, on_delete=models.CASCADE)
    comment = models.TextField()
    link_video = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date} {self.rating}"

    class Meta:
        verbose_name = 'CommentsUsersVideocard'
        verbose_name_plural = "CommentsUsersVideocard's"


class CommentsUserMonitor(models.Model):
    rating_choice = (('1', '1'),
                     ('2', '2'),
                     ('3', '3'),
                     ('4', '4'),
                     ('5', '5')
                     )
    rating = models.CharField(max_length=15, choices=rating_choice, null=True, blank=True)
    name_of_user = models.CharField(max_length=50)
    name_of_stuff = models.ForeignKey(Monitors_list, on_delete=models.CASCADE)
    comment = models.TextField()
    link_video = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date} {self.rating}"

    class Meta:
        verbose_name = 'CommentsUserMonitor'
        verbose_name_plural = "CommentsUserMonitors"


class CommentsUserMemory(models.Model):
    rating_choice = (('1', '1'),
                     ('2', '2'),
                     ('3', '3'),
                     ('4', '4'),
                     ('5', '5')
                     )
    rating = models.CharField(max_length=15, choices=rating_choice, null=True, blank=True)
    name_of_user = models.CharField(max_length=50)
    name_of_stuff = models.ForeignKey(Memory_list, on_delete=models.CASCADE)
    comment = models.TextField()
    link_video = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date} {self.rating}"

    class Meta:
        verbose_name = 'CommentsUserMemory'
        verbose_name_plural = "CommentsUserMemory"


class QuestionUsersVideocard(models.Model):
    name_of_user = models.CharField(max_length=50)
    name_of_stuff = models.ForeignKey(Videocards, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date}"

    class Meta:
        verbose_name = 'QuestionUsersVideocard'
        verbose_name_plural = "QuestionUsersVideocard's"


class QuestionUsersMonitor(models.Model):
    name_of_user = models.CharField(max_length=50)
    name_of_stuff = models.ForeignKey(Monitors_list, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date}"

    class Meta:
        verbose_name = 'QuestionUsersMonitor'
        verbose_name_plural = "QuestionUsersMonitor's"


class QuestionUsersMemory(models.Model):
    name_of_user = models.CharField(max_length=50)
    name_of_stuff = models.ForeignKey(Memory_list, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date}"

    class Meta:
        verbose_name = 'QuestionUsersMemory'
        verbose_name_plural = "QuestionUsersMemory"


class ProductCart(models.Model):
    in_out_list = (('Є в наявності', 'Є в наявності'),
                   ('Немає в наявності', 'Немає в наявності'))

    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255)
    product_pic = models.TextField()
    product_price = models.IntegerField()
    product_status = models.CharField(max_length=255, choices=in_out_list)

    def __str__(self):
        return f"{self.user_name} {self.product_title} {self.product_pic} {self.product_price} {self.product_status}"

    class Meta:
        verbose_name = 'ProductCart'
        verbose_name_plural = 'ProductsCart'
