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
    pic = models.ImageField(upload_to='notebooks_pic', null=True, blank=True)
    pic_link = models.TextField(null=True, blank=True)
    pic_link_2 = models.TextField(null=True, blank=True)
    pic_link_3 = models.TextField(null=True, blank=True)
    pic_link_4 = models.TextField(null=True, blank=True)
    pic_link_5 = models.TextField(null=True, blank=True)
    pic_link_6 = models.TextField(null=True, blank=True)
    pic_link_7 = models.TextField(null=True, blank=True)
    pic_link_8 = models.TextField(null=True, blank=True)
    pic_link_9 = models.TextField(null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    in_out = models.CharField(max_length=255, choices=in_out_list)
    processor = models.CharField(max_length=50, null=True, blank=True)
    display_width = models.CharField(max_length=6, null=True, blank=True)
    ram = models.CharField(max_length=3, null=True, blank=True)
    video_card = models.CharField(max_length=65, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.title} {self.video_link} {self.pic} {self.pic_link} {self.description}" \
               f"{self.price} {self.in_out} {self.processor} {self.display_width} {self.ram} {self.video_card}"



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


"""working model for hard_disk page"""


class HardDiskLists(models.Model):
    in_out_list = (('Є в наявності', 'Є в наявності'),
                   ('Немає в наявності', 'Немає в наявності'))

    list_of_brand = (('Hitachi', 'Hitachi'),
                     ('Samsung', 'Samsung'),
                     ('Seagate', 'Seagate'),
                     ('Toshiba', 'Toshiba'),
                     ('WD', 'WD'),
                     )

    brand = models.CharField(max_length=60, choices=list_of_brand)
    title = models.CharField(max_length=255)
    video_link = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='hard_disc_pic', null=True, blank=True)
    pic_link = models.TextField(null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    in_out = models.CharField(max_length=255, choices=in_out_list)
    size = models.CharField(max_length=2,null=True, blank=True)
    count_of_twist = models.CharField(max_length=4,null=True, blank=True, default=0)
    socket = models.CharField(max_length=50)
    buffer_size = models.CharField(max_length=3,null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.title} {self.video_link} {self.pic}" \
               f" {self.pic_link} {self.description} {self.price} {self.in_out}" \
               f"{self.size} {self.count_of_twist} {self.socket} {self.buffer_size}"

    class Meta:
        verbose_name = 'HardDiskList'
        verbose_name_plural = "HardDiskList"


"""test"""


class HardDiskList(Memory_list):
    list_of_brand = (('samsung', 'samsung'),
                     ('wd', 'wd'),
                     ('kingston', 'kingston'))

    def __str__(self):
        return f"{self.brand} {self.title} {self.video_link} {self.pic}" \
               f" {self.pic_link} {self.description} {self.price} {self.in_out}"

    class Meta:
        verbose_name = 'HardDiskList'
        verbose_name_plural = 'HardDiskLists'


class CommentsUsers(models.Model):
    rating_choice = ((1, 1),
                     (2, 2),
                     (3, 3),
                     (4, 4),
                     (5, 5)
                     )
    rating = models.IntegerField(choices=rating_choice, null=True, blank=True)
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
    rating_choice = ((1, 1),
                     (2, 2),
                     (3, 3),
                     (4, 4),
                     (5, 5)
                     )
    rating = models.IntegerField(choices=rating_choice, null=True, blank=True)
    name_of_user = models.CharField(max_length=50)
    name_of_stuff = models.ForeignKey(Memory_list, on_delete=models.CASCADE)
    comment = models.TextField()
    link_video = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date}"

    class Meta:
        verbose_name = 'CommentsUserMemory'
        verbose_name_plural = "CommentsUserMemory"


"""comment for hard_disk page"""


class CommentsUserHardDisk(models.Model):
    rating_choice = ((1, 1),
                     (2, 2),
                     (3, 3),
                     (4, 4),
                     (5, 5)
                     )
    rating = models.IntegerField(choices=rating_choice, null=True, blank=True)
    name_of_user = models.CharField(max_length=50)
    name_of_stuff = models.ForeignKey(HardDiskLists, on_delete=models.CASCADE)
    comment = models.TextField()
    link_video = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f" {self.name_of_stuff} {self.comment} {self.date}"

    class Meta:
        verbose_name = 'CommentsUserHardDisk'
        verbose_name_plural = "CommentsUserHardDisk"


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
        return f"{self.name_of_stuff} {self.comment} {self.date}"

    class Meta:
        verbose_name = 'QuestionUsersMemory'
        verbose_name_plural = "QuestionUsersMemory"


"""Question for  hard_disk page"""


class QuestionUsersHardDisk(models.Model):
    name_of_user = models.CharField(max_length=50)
    name_of_stuff = models.ForeignKey(HardDiskLists, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name_of_stuff} {self.comment} {self.date}"

    class Meta:
        verbose_name = 'QuestionUsersHardDisk'
        verbose_name_plural = "QuestionUsersHardDisk"


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


class LikeListModel(models.Model):
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
        verbose_name = 'LikeListModel'
        verbose_name_plural = 'LikeListModel'
