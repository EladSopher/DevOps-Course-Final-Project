import django_tables2 as tables
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import RelatedField
from django_tables2.data import TableQuerysetData

from statuspage.tables import columns
from utilities.paginator import EnhancedPaginator, get_paginate_count

__all__ = (
    'BaseTable',
    'StatusPageTable',
)


class BaseTable(tables.Table):
    """
    Base table class for StatusPage objects. Adds support for:

        * Automatic prefetching of related objects
        * styling

    :param user: Personalize table display for the given user (optional). Has no effect if AnonymousUser is passed.
    """
    exempt_columns = ()

    class Meta:
        attrs = {
            'class': 'min-w-full divide-y divide-gray-300 dark:divide-gray-700',
            'th': {
                'class': 'px-3 py-3.5 text-left font-semibold text-gray-900 dark:text-gray-100',
            }
        }

    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.rounded = ''

        # Set default empty_text if none was provided
        if self.empty_text is None:
            self.empty_text = f"No {self._meta.model._meta.verbose_name_plural} found"

        # Determine the table columns to display by checking the following:
        #   1. User's configuration for the table
        #   2. Meta.default_columns
        #   3. Meta.fields
        selected_columns = None
        if user is not None and not isinstance(user, AnonymousUser):
            selected_columns = user.config.get(f"tables.{self.__class__.__name__}.columns")
        if not selected_columns:
            selected_columns = getattr(self.Meta, 'default_columns', self.Meta.fields)

        # Hide non-selected columns which are not exempt
        for column in self.columns:
            if column.name not in [*selected_columns, *self.exempt_columns]:
                self.columns.hide(column.name)

        # Rearrange the sequence to list selected columns first, followed by all remaining columns
        # TODO: There's probably a more clever way to accomplish this
        self.sequence = [
            *[c for c in selected_columns if c in self.columns.names()],
            *[c for c in self.columns.names() if c not in selected_columns]
        ]

        # PK column should always come first
        if 'pk' in self.sequence:
            self.sequence.remove('pk')
            self.sequence.insert(0, 'pk')

        # Actions column should always come last
        if 'actions' in self.sequence:
            self.sequence.remove('actions')
            self.sequence.append('actions')

        # Dynamically update the table's QuerySet to ensure related fields are pre-fetched
        if isinstance(self.data, TableQuerysetData):

            prefetch_fields = []
            for column in self.columns:
                if column.visible:
                    model = getattr(self.Meta, 'model')
                    accessor = column.accessor
                    prefetch_path = []
                    for field_name in accessor.split(accessor.SEPARATOR):
                        try:
                            field = model._meta.get_field(field_name)
                        except FieldDoesNotExist:
                            break
                        if isinstance(field, RelatedField):
                            # Follow ForeignKeys to the related model
                            prefetch_path.append(field_name)
                            model = field.remote_field.model
                        elif isinstance(field, GenericForeignKey):
                            # Can't prefetch beyond a GenericForeignKey
                            prefetch_path.append(field_name)
                            break
                    if prefetch_path:
                        prefetch_fields.append('__'.join(prefetch_path))
            self.data.data = self.data.data.prefetch_related(*prefetch_fields)

    def _get_columns(self, visible=True):
        columns = []
        for name, column in self.columns.items():
            if column.visible == visible and name not in self.exempt_columns:
                columns.append((name, column.verbose_name))
        return columns

    @property
    def available_columns(self):
        return self._get_columns(visible=False)

    @property
    def selected_columns(self):
        return self._get_columns(visible=True)

    @property
    def objects_count(self):
        """
        Return the total number of real objects represented by the Table. This is useful when dealing with
        prefixes/IP addresses/etc., where some table rows may represent available address space.
        """
        if not hasattr(self, '_objects_count'):
            self._objects_count = sum(1 for obj in self.data if hasattr(obj, 'pk'))
        return self._objects_count

    def configure(self, request):
        """
        Configure the table for a specific request context. This performs pagination and records
        the user's preferred ordering logic.
        """
        # Save ordering preference
        if request.user.is_authenticated:
            table_name = self.__class__.__name__
            if self.prefixed_order_by_field in request.GET:
                # If an ordering has been specified as a query parameter, save it as the
                # user's preferred ordering for this table.
                ordering = request.GET.getlist(self.prefixed_order_by_field)
                request.user.config.set(f'tables.{table_name}.ordering', ordering, commit=True)
            elif ordering := request.user.config.get(f'tables.{table_name}.ordering'):
                # If no ordering has been specified, set the preferred ordering (if any).
                self.order_by = ordering
            rounded_config = request.user.config.get('pagination.placement')
            if rounded_config == 'top':
                self.rounded = 'md:rounded-b-lg'
            if rounded_config == 'bottom' or rounded_config is None:
                self.rounded = 'md:rounded-t-lg'

        # Paginate the table results
        paginate = {
            'paginator_class': EnhancedPaginator,
            'per_page': get_paginate_count(request)
        }
        tables.RequestConfig(request, paginate).configure(self)


class StatusPageTable(BaseTable):
    """
    Table class for most StatusPage objects. Includes default columns for:

        * PK (row selection)
        * ID
        * Actions
    """
    pk = columns.ToggleColumn(
        visible=False
    )
    id = tables.Column(
        linkify=True,
        verbose_name='Id'
    )
    actions = columns.ActionsColumn()

    exempt_columns = ('pk', 'actions')

    class Meta(BaseTable.Meta):
        pass
