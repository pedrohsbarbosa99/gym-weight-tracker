from django.db.models import Lookup


class Similarity(Lookup):
    lookup_name = "similarity"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "similarity(%s, %s) >= %s" % (lhs, rhs, 0.4), params
