
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.deletion import CASCADE
from django.utils import timezone

from django.urls import reverse

User = get_user_model()

def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]



##############################################
def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname,kwargs={'ct_model':ct_model,'slug':obj.slug})









class LatestProductsManager:

      @staticmethod
      def get_products_for_main_page(*args, **kwargs):
          with_respect_to = kwargs.get('with_repect_to')
          products = []
          ct_models = ContentType.objects.filter(model__in=args)
          for ct_model in ct_models:
              model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
              products.extend(model_products)
          if  with_respect_to:
              ct_model = ContentType.objects.filter(model=with_respect_to)
              if ct_model.exists():
                 if  with_respect_to in args:
                     return sorted(
                         
                         products,key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),reverse=True,
                         
                         ) 

          return products


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):
    CATEGORY_NAME1 = 'Notebook'
    CATEGORY_NAME2 = 'Smarfon'
    
    CATEGORY_NAME_COUNT_NAME = {
            # (CATEGORY_NAME1,'notebook__count'),
            # (CATEGORY_NAME2,'smartfon__count')
            'Notebook': 'notebook__count',
            'Smartfon': 'smartfon__count' ,

    }
    

    def get_queryset(self):
        return super().get_queryset()
    
    def get_categories_for_left_sidebar(self):  
        models = get_models_for_count('notebook','smartfon') 
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(),count=getattr(c,self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data
 
class Category(models.Model):
    
     
    name = models.CharField(max_length=255 ,verbose_name="Name Category")
    slug = models.SlugField(unique=True)
    objects = CategoryManager()
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})



class Product(models.Model):
 

    class Meta:
        abstract = True
    
    category = models.ForeignKey(Category,verbose_name='Category',on_delete=models.CASCADE)
    title = models.CharField(max_length=255,verbose_name='Names')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Description',null=True)
    price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='price')

    def __str__(self):
        return self.title

    
    def get_model_name(self):
        return self.__class__.__name__.lower()

 


class Notebook(Product):
     diagonal = models.CharField(max_length=255,verbose_name='Diagonal')
     display = models.CharField(max_length=255,verbose_name='Type display')
     processor_freq = models.CharField(max_length=255,verbose_name='Freq processor')
     ram = models.CharField(max_length=255,verbose_name='RAM')
     video = models.CharField(max_length=255,verbose_name='Video card')
     time_wihout_charger = models.CharField(max_length=255,verbose_name = 'Battery life')

     def __str__(self):
        return "{}:{}".format(self.category.name,self.title)
    
     def get_absolute_url(self):
        return get_product_url(self,'product_detail')




class Smartfon(Product):
    diagonal = models.CharField(max_length=255,verbose_name='Diagonal')
    display_type =  models.CharField(max_length=255,verbose_name='Display type')
    resolution = models.CharField(max_length=255,verbose_name='Screen size')
    accum_volume = models.CharField(max_length=255,verbose_name='Battery capacity')
    ram = models.CharField(max_length=255,verbose_name='RAM')
    sd = models.BooleanField(default=True,verbose_name='Availability sd card')
    sd_volume_max = models.CharField(max_length=255,null=True,blank=True, verbose_name='The maximum memory')
    main_cam_mp = models.CharField(max_length=255,verbose_name='Main camera')
    frontal_cam_mp = models.CharField(max_length=255,verbose_name='Frontal camera')
   
    def __str__(self):
        return "{}: {}".format(self.category.name,self.title)

    def get_absolute_url(self):
      return get_product_url(self,'product_detail')


class CartProduct(models.Model):


    user = models.ForeignKey('Customer',verbose_name='Customer',on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart',verbose_name='Cart',on_delete=models.CASCADE,related_name='related_products')
    content_type  = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Summa')

    def __str__(self):
        return "Product:{} (for cart)".format(self.content_object.title)

    def save(self,*args,**kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args,**kwargs)

class Cart(models.Model):
    

    owner = models.ForeignKey('Customer',null=True,verbose_name='Owner',on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct,blank=True,related_name='related_cart')
    total_products =  models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9,default=0,decimal_places=2,verbose_name="Summa")
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
        
   


class Customer(models.Model):

    user = models.ForeignKey(User,verbose_name='Users',on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,verbose_name='Number phone',null=True,blank=True)
    address =   models.CharField(max_length=255,verbose_name='Address')
    orders = models.ManyToManyField('Order', verbose_name='Order cutomer', related_name='related_order')

    def __str__(self):
        return "User:{} {}".format(self.user.first_name,self.user.last_name)
        

class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'ready'
    STATUS_COMPLETED = 'completed'
 
    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'New order'),
        (STATUS_IN_PROGRESS,'Processing order'),
        (STATUS_READY,'Ready order'),
        (STATUS_COMPLETED,'Completed order')

    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF,'Pickup'),
        (BUYING_TYPE_DELIVERY,'Delivery')
    )
 
    customer = models.ForeignKey(Customer, verbose_name='Client', on_delete=models.CASCADE, related_name='related_orders')
    first_name = models.CharField(max_length=200, verbose_name='Name',)
    last_name = models.CharField(max_length=200, verbose_name="Firstname")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    cart = models.ForeignKey(Cart, verbose_name='Cart', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name="Address", null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Status order', 
        choices=STATUS_CHOICES, 
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Type order',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Comments...', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Created order')
    order_date = models.DateField(verbose_name='Date of receipt of order', default=timezone.now)

    def __str__(self):
        return str(self.id)
