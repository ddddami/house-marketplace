from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class PromotedItemManager(models.Manager):
    def get_promotions_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return PromotedItem.objects \
            .select_related('promotion') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class PromotedItem(models.Model):
    objects = PromotedItemManager()
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
