"""
This class defines the order of objects
"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderPallyneFields(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderPallyneFields, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # There is no current value
            try:
                obj = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in for_fields
                    query = {'field': getattr(model_instance, field) for field in self.for_fields}
                    obj = obj.filter(**query)
                # get the order of the last item
                last_item = obj.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderPallyneFields, self).pre_save(model_instance, add)
