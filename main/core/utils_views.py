# -*- coding: utf-8 -*-
from django.http import Http404


def get_object_or_404(object_model, object_id, caller=None):
    try:
        return object_model.objects.get(id=object_id)
    except object_model.DoesNotExist:
        if hasattr(caller, 'request'):
            caller.log.debugIndirect('Object <%s#%s> not found' % (object_model.__name__, object_id))
        raise Http404
