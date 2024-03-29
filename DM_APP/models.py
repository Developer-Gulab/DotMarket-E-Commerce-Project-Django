from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Slider(models.Model):
    Discount_Deal = (
        ('HOT DEALS','HOT DEALS'),
        ('New Arraivels','New Arraivels'),
        ('New DEALS','New DEALS')
    )
    
    image = models.ImageField(upload_to = 'media/slider_imgs')
    discount_deal = models.CharField(choices = Discount_Deal, max_length = 200)
    sale = models.IntegerField()
    brand_name = models.CharField(max_length = 200)
    discount = models.IntegerField()
    link = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.brand_name
    
    
class Banner_Area(models.Model):
    image = models.ImageField(upload_to = 'media/banner_imgs')
    discount_deal = models.CharField(max_length = 200)
    quote = models.CharField(max_length = 200)
    discount = models.IntegerField()
    link = models.CharField(max_length = 200, null = True)
    
    def __str__(self):
        return self.quote
    
    
class Main_Category(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name + "--" + self.main_category.name
    
class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.category.main_category.name + "--" + self.category.name + "--" + self.name
    


class Section(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
    
    
class Color(models.Model):
    code = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.code
    
    
class Brand(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    total_quantity = models.IntegerField()
    availability = models.IntegerField()
    featured_image = models.CharField(max_length = 200)
    product_name = models.CharField(max_length = 100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null = True)
    price = models.IntegerField()
    discount = models.IntegerField()
    tax = models.IntegerField(null = True) 
    packing_cost = models.IntegerField(null = True)
    product_information = RichTextField()
    model_name = models.CharField(max_length = 100)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null = True)
    tags = models.CharField(max_length = 100)
    description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "DM_APP_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)


class CouponCode(models.Model):
    code = models.CharField(max_length = 100)
    discount = models.IntegerField()
    
    def __str__(self):
        return self.code

    
class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.CharField(max_length = 200)
    
class Additional_Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length = 200)
    detail = models.CharField(max_length = 200)
    

    