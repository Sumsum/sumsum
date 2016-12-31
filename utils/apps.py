from django.apps import AppConfig
from django.conf import settings
from django.db.models import Lookup
from utils.fields import TransField


class TransIContains(Lookup):
    lookup_name = 'icontains'
    prepare_rhs = False

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        if params and not self.bilateral_transforms:
            params[0] = '%{}%'.format(connection.ops.prep_for_like_query(params[0]))
        sql = []
        for code, name in settings.LANGUAGES:
            sql.append('{}::json->>\'{}\''.format(lhs, code))
        return '({}) ILIKE {}'.format(' OR '.join(sql), rhs), params


class UtilsConfig(AppConfig):
    name = 'utils'

    def ready(self):
        TransField.register_lookup(TransIContains)
