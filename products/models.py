from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from simple_history.models import HistoricalRecords
from cloudinary.models import CloudinaryField


class Product(models.Model):
    codigo = models.CharField(
        primary_key=True, editable=True, max_length=40, verbose_name=(u'Código'))
    barra = models.CharField(
        max_length=200, unique=True, verbose_name=(u'Barra'))
    name = models.CharField(max_length=200,
                            verbose_name=(u'Nombre'))
    name_extend = models.CharField(max_length=200, unique=True,
                                   verbose_name=(u'Nombre Extendido'))
    images = models.ImageField(upload_to='photos/products')
    slug = models.SlugField(max_length=200, unique=True, verbose_name=(u'Url'))
    description = models.TextField(
        max_length=4000, blank=True, verbose_name=(u'Detalle'))
    price1 = models.PositiveSmallIntegerField(
        verbose_name=(u'Precio1'))
    price2 = models.PositiveSmallIntegerField(blank=True, null=True,
                                              verbose_name=(u'Precio2'))
    price3 = models.PositiveSmallIntegerField(blank=True, null=True,
                                              verbose_name=(u'Precio3'))
    price4 = models.PositiveSmallIntegerField(blank=True, null=True,
                                              verbose_name=(u'Precio4'))
    price5 = models.PositiveSmallIntegerField(blank=True, null=True,
                                              verbose_name=(u'Precio5'))
    price_old = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name=(u'Precio Anterior'))
    active = models.BooleanField(default=True, verbose_name=(u'Activo'))
    offer = models.BooleanField(default=False, verbose_name=(u'Oferta'))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=(u'Creado'))
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name=(u'Modificado'))
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

   
    def __str__(self):
        return f'{self.name} : cod:{self.codigo}'

   

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name=(u'Nombre'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=(u'Url'))

    image = CloudinaryField('categories', blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=(u'Creado'))
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name=(u'Modificado'))
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class CategoryProduct(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=(u'Producto'))
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=(u'Creado'))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=(u'Categoría'))

    class Meta:
        verbose_name = 'Categoria de Producto'
        verbose_name_plural = 'Categoria de Productos'

    def __str__(self):
        return str(self.category)


class Gallery(models.Model):
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE, verbose_name=(u'Producto'))
    image = models.ImageField(
        upload_to='store/products', max_length=255, verbose_name=(u'Imagenes'))

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Galeria de Imagenes'


class Attribut(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name=(u'Nombre'))
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'

    def __str__(self):
        return self.name

