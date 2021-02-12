from django import template
from django.db import models
from django.utils.safestring import mark_safe
from mainapp.models import Smartfon

register = template.Library()

TABLE_HAED = """
         <table class="table">

        <tbody>

            """
TABLE_TAIL = """
              </tbody>
              </table>
            """
TABLE_CONTENT = """
            <tr>
            <td>{name}</td>
            <td>{value}</td>

            </tr>

                """


PRODUCT_SPEC = {
         'notebook':{
              'Diagonal':'diagonal',
              'Display type':'display',
              'Freq processor':'processor_freq',
              'RAM':'ram',
              'Video card':'video',
              'Battery life':'time_wihout_charger' ,
         },

         'smartfon':{
              'Diagonal':'diagonal',
              'Display type':'display_type',
              'Screen sizer':'resolution',
              'Battery capacity':'accum_volume',
              'RAM':'ram',
              'Sd':'sd',
              'The maximum memory':'sd_volume_max',
              'Main camera':'main_cam_mp',
              'Frontal camera':'frontal_cam_mp'

             }

     
}



def get_product_spec(product,model_name):
    table_content = ''
    for name,  value in PRODUCT_SPEC[model_name].items():
       table_content += TABLE_CONTENT.format(name=name,value=getattr(product,value))
    return table_content      



# @register.filter
# def product_spec(product):
#     model_name = product.__class__._meta.model_name
#     if isinstance(product,Smartfon):
#           if not product.sd:
#               PRODUCT_SPEC['smartfon'].pop('The maximum memory')
#           else:
#               PRODUCT_SPEC['smartfon']['The maximum memory']='sd_volume_max'
#     return  mark_safe(TABLE_HAED + get_product_spec(product,model_name) + TABLE_TAIL)
    