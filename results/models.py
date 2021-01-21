from django.db import models

# Create your models here.
class Lists(models.Model):
    name = models.CharField('节目名称', default='',max_length=50)

    class Meta:
        verbose_name = '待查询'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return str(self.name)




class Final_Lists(models.Model):
    id = models.IntegerField('ID',primary_key=True)
    name = models.CharField('节目名称', default='',max_length=50)
    year = models.CharField('年份', default='',max_length=4)
    score = models.FloatField('评分',default='',max_length=4)
    ratenum = models.IntegerField('评分人数', default='')

    class Meta:
        verbose_name = '查询结果'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return str(self.name)