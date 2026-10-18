from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions

from escopos.models import LogAcesso

DICT_METHODS = {
    'POST': 'add',
    'PUT': 'change',
    'DELETE': 'delete',
    'GET': 'view',
    'OPTIONS': 'view',
    'PATCH': 'view',
    'HEAD': 'view',
}


class CustomPermission(permissions.BasePermission):
    """
    Permission based on Django model perms, with DEBUG-friendly fallbacks.
    """

    def _user_escopo_id(self, user):
        usuario = getattr(user, 'usuario', None)
        if usuario is None:
            return None
        return usuario.escopo_id

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        obj_escopo_id = getattr(obj, 'escopo_id', None)
        if obj_escopo_id is None:
            return True

        return obj_escopo_id == self._user_escopo_id(request.user)

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser or user.is_staff:
            return True

        queryset = getattr(view, 'queryset', None)
        if queryset is None and hasattr(view, 'get_queryset'):
            try:
                queryset = view.get_queryset()
            except Exception:
                queryset = None

        if queryset is None:
            return True

        model = queryset.model
        obj_content_type = ContentType.objects.get_for_model(model)
        app = obj_content_type.app_label
        model_name = obj_content_type.model
        method = request.method.upper()
        perm_codename = DICT_METHODS.get(method, 'view')
        perm = f'{app}.{perm_codename}_{model_name}'

        try:
            LogAcesso.objects.create(
                usuario=user,
                url=request.get_full_path(),
                permissao=perm,
                metodo=method,
            )
        except Exception:
            pass

        if user.has_perm(perm):
            return True

        # Local/dev usability: authenticated users with an escopo can read.
        if method in ('GET', 'HEAD', 'OPTIONS') and self._user_escopo_id(user) is not None:
            return True

        return False
