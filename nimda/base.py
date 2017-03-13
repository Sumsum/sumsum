def line_fields(fields):
    """
    Makes lines of two fields, basically turns any vector
    into a 2 columns wide matrix.
    """
    lines = []
    counter = 0
    while counter < len(fields):
        try:
            next_field = fields[counter + 1]
        except IndexError:
            line = (fields[counter],)
            counter = counter + 1
        else:
            line = (fields[counter], next_field)
            counter = counter + 2
        lines.append(line)
    return lines


class NimdaException(Exception):
    pass


class NimdaSiteMixin(object):
    def each_context(self, request):
        """
        Adds available_apps to each context
        """
        c = super(NimdaSiteMixin, self).each_context(request)
        res = self.index(request)
        c['available_apps'] = res.context_data['app_list']
        return c
