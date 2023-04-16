import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'order.settings'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import django
django.setup() # To be able to work with models

from .models import MenuItem
import xlrd


class UploadingMenuItems(object):
    foreign_key_fields = ["category"]
    model = MenuItem

    # Read the dictionary from import_files()
    def __init__(self, data):
        data = data
        self.uploaded_file = data.get("file")
        self.parsing()


    def getting_related_model(self, field_name):
        model = self.model
        related_model = model._meta.get_field(field_name).remote_field.model
        return related_model
    

    def getting_headers(self):
        s = self.s
        headers = dict()

        fields = [field.name for field in MenuItem._meta.get_fields() if not field.auto_created]
        columns = []

        for column in range(s.ncols): # ncols - how many cols with data
            value = s.cell(0, column).value # Get cell's value 
            headers[column] = value
            columns.append(value)

        # Check if file has all required columns
        for field in fields:
            if field not in columns:
                raise ValueError(f'Column [{field}] is required!')

        return headers
    

    def check_conditions(self, field_name, value, row):
        folder_path = 'media/import'
        folder_contents = [os.path.join('import/', value) for value in os.listdir(folder_path)]

        # Check if fields 'name', 'price', 'image' have values
        if field_name == "name" or field_name == "price" or field_name == "image":
            if not value:
                raise ValueError(f"Field [{field_name}] in row [{row + 1}] is empty!")
        
        # Check if 'image' has correct value
        if field_name == "image" and value not in folder_contents:
            raise ValueError(f"Can not find [{field_name}] in row [{row + 1}]")

        # Check if 'price' has correct value
        if field_name == "price":
            if value <= 0:
                raise ValueError(f"Field [{field_name}] in row [{row + 1}] has to be more than zero!")
            elif type(value) != float or value % 1 != 0:
                raise ValueError(f"Field [{field_name}] in row [{row + 1}] has to be integer!")
            

    
    def parsing(self):
        uploaded_file = self.uploaded_file
        wb = xlrd.open_workbook(file_contents=uploaded_file.read())
        s = wb.sheet_by_index(0) # Open first list from exel file
        self.s = s

        headers = self.getting_headers()
        print(headers)

        menu_item_bulk_list = list()
        
        for row in range(1, s.nrows):
            row_dict = {}
            for column in range(s.ncols):
                value = s.cell(row, column).value
                field_name = headers[column]

                # Check if field 'id' has value
                if field_name == "id"  and not value:
                    continue

                self.check_conditions(field_name, value, row)

                if field_name in self.foreign_key_fields:
                    related_model = self.getting_related_model(field_name)
                    print(related_model)

                    if not value:
                        raise ValueError(f"Field [{field_name}] in row [{row + 1}] is empty!")
 
                    instance, created = related_model.objects.get_or_create(name=value)
                    value = instance

                row_dict[field_name] = value 
            
            if row_dict["name"] in list(MenuItem.objects.values_list('name', flat=True).distinct()):
                continue
            
            name_list = []
            for item in menu_item_bulk_list:
                name_list.append(item.name)

            if row_dict["name"] in name_list:
                continue

            print(row_dict)  
            menu_item_bulk_list.append(MenuItem(**row_dict))
            # MenuItem.objects.create(**row_dict)

        MenuItem.objects.bulk_create(menu_item_bulk_list)
        return True