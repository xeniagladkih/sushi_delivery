from django.contrib import admin
from .models import *
from import_export import resources, widgets
from import_export.admin import ImportExportActionModelAdmin
from import_export.fields import Field

class MenuItemResource(resources.ModelResource):
    category = Field(
    column_name='category',
    attribute='category',
    widget= widgets.ForeignKeyWidget(Category, field='name')
    )

    class Meta:
        model = MenuItem

class MenuItemAdmin(ImportExportActionModelAdmin):
    resource_class = MenuItemResource
    list_display = [field.name for field in MenuItem._meta.fields if field.name != "id"]
    ordering = ['id']


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class CategoryAdmin(ImportExportActionModelAdmin):
    resource_class = CategoryResource
    list_display = [field.name for field in Category._meta.fields if field.name != "id"]


admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderModel)
admin.site.register(ShippingAddress)


