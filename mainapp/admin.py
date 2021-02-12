from django.contrib import admin
from django.forms import ModelChoiceField,ModelForm
from django.forms.utils import ErrorList
# Register your models here.

from .models import *


# class SmartfonAdminForm(ModelForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         instance = kwargs.get('instance')
#         if not instance.sd:
#             self.fields['sd_volume_max'].widget.attrs.update({
#                  'readonly':True,'style':'background:gray'
#             })


        
#     def clean(self):
#         if not self.cleaned_data['sd']:
#             self.cleaned_data['sd_volume_max'] = None
#         return self.cleaned_data
 


class NotebookAdmin(admin.ModelAdmin):
    


    def formfield_for_foreignkey(self,db_field,request,**kwargs):

          if db_field.name == 'category':
              return ModelChoiceField(Category.objects.filter(slug='notebooks'))
          return super().formfield_for_foreignkey(db_field,request,**kwargs)


class SmartfonAdmin(admin.ModelAdmin):
   
    
    change_form_template = 'admin.html'
    def formfield_for_foreignkey(self,db_field,request,**kwargs):

        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartfons'))
        return super().formfield_for_foreignkey(db_field,request,**kwargs)












admin.site.register(Category)
admin.site.register(Notebook,NotebookAdmin)
admin.site.register(Smartfon,SmartfonAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.site_header = 'MARKET.UZ ADMIN'
