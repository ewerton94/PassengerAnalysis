from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from escopos.models import LogAcesso
from django.conf import settings

DICT_METHODS = {
    'POST': 'add',
    'PUT': 'change',
    'DELETE': 'delete',
    'GET': 'view',
    'OPTIONS': 'view',
    'PATCH': 'view'

}
print(settings.DEBUG)
if False:
    CustomPermission = permissions.AllowAny

else:
    class CustomPermission(permissions.BasePermission):
        """
        Object-level permission to only allow owners of an object to edit it.
        Assumes the model instance has an `owner` attribute.
        """

        def has_object_permission(self, request, view, obj):
            # Read permissions are allowed to any request,
            # so we'll always allow GET, HEAD or OPTIONS requests.
            print('Entrou')
            if request.method in permissions.SAFE_METHODS:
                return True

            # obj here is a UserProfile instance
            print(obj.escopo_id == request.user.escopo.escopo_id)
            return obj.escopo_id == request.user.escopo.escopo_id

        def has_permission(self, request, view):
            user = request.user
            print('ewfewf')
            if not user.is_authenticated:
                return False

            obj_content_type = ContentType.objects.get_for_model(view.queryset.model)
            app = obj_content_type.app_label
            model = obj_content_type.model

            LogAcesso.objects.create(usuario=user, url=request.get_full_path(),
                                     permissao='%s.%s_%s' % (app, DICT_METHODS[request.method.upper()], model),
                                     metodo=request.method)

            return user.has_perm('%s.%s_%s' % (app, DICT_METHODS[request.method.upper()], model))
