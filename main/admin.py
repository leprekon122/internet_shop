from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(NotebooksList)
admin.site.register(Videocards)
admin.site.register(Monitors_list)
admin.site.register(Memory_list)
admin.site.register(HardDiskLists)
admin.site.register(CommentsUsers)
admin.site.register(QuestionUsers)
admin.site.register(CommentsUsersVideocard)
admin.site.register(CommentsUserHardDisk)
admin.site.register(QuestionUsersVideocard)
admin.site.register(QuestionUsersMonitor)
admin.site.register(QuestionUsersMemory)
admin.site.register(QuestionUsersHardDisk)
admin.site.register(ProductCart)
admin.site.register(LikeListModel)
admin.site.register(OrderList)
admin.site.register(DocumentOfSold)

