import django_filters
from django.contrib.auth.models import Group, User
from django.db.models import Q

from statuspage.filtersets import BaseFilterSet
from users.models import ObjectPermission, Token

__all__ = (
    'GroupFilterSet',
    'ObjectPermissionFilterSet',
    'UserFilterSet',
)


class GroupFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    class Meta:
        model = Group
        fields = ['id', 'name']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(name__icontains=value)


class UserFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    group_id = django_filters.ModelMultipleChoiceFilter(
        field_name='groups',
        queryset=Group.objects.all(),
        label='Group',
    )
    group = django_filters.ModelMultipleChoiceFilter(
        field_name='groups__name',
        queryset=Group.objects.all(),
        to_field_name='name',
        label='Group (name)',
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(username__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )


class TokenFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    user_id = django_filters.ModelMultipleChoiceFilter(
        field_name='user',
        queryset=User.objects.all(),
        label='User',
    )
    user = django_filters.ModelMultipleChoiceFilter(
        field_name='user__username',
        queryset=User.objects.all(),
        to_field_name='username',
        label='User (name)',
    )
    created = django_filters.DateTimeFilter()
    created__gte = django_filters.DateTimeFilter(
        field_name='created',
        lookup_expr='gte'
    )
    created__lte = django_filters.DateTimeFilter(
        field_name='created',
        lookup_expr='lte'
    )
    expires = django_filters.DateTimeFilter()
    expires__gte = django_filters.DateTimeFilter(
        field_name='expires',
        lookup_expr='gte'
    )
    expires__lte = django_filters.DateTimeFilter(
        field_name='expires',
        lookup_expr='lte'
    )

    class Meta:
        model = Token
        fields = ['id', 'key', 'write_enabled', 'description']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(user__username__icontains=value) |
            Q(description__icontains=value)
        )


class ObjectPermissionFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    user_id = django_filters.ModelMultipleChoiceFilter(
        field_name='users',
        queryset=User.objects.all(),
        label='User',
    )
    user = django_filters.ModelMultipleChoiceFilter(
        field_name='users__username',
        queryset=User.objects.all(),
        to_field_name='username',
        label='User (name)',
    )
    group_id = django_filters.ModelMultipleChoiceFilter(
        field_name='groups',
        queryset=Group.objects.all(),
        label='Group',
    )
    group = django_filters.ModelMultipleChoiceFilter(
        field_name='groups__name',
        queryset=Group.objects.all(),
        to_field_name='name',
        label='Group (name)',
    )

    class Meta:
        model = ObjectPermission
        fields = ['id', 'name', 'enabled', 'object_types', 'description']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )
