from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分類名稱')
    description = models.TextField(blank=True, verbose_name='分類描述')
    order = models.IntegerField(default=0, verbose_name='排序順序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    class Meta:
        verbose_name = '商品分類'
        verbose_name_plural = '商品分類'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='商品名稱')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='價格')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products', verbose_name='商品分類')
    image = models.ImageField(upload_to='products/',
                              verbose_name='商品圖片', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name='商品描述')
    ingredients = models.TextField(blank=True, verbose_name='商品成分')
    is_featured = models.BooleanField(default=False, verbose_name='精選商品')
    is_new = models.BooleanField(default=False, verbose_name='新上市商品')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-is_new', 'category__order', 'name']

    def __str__(self):
        return self.name
