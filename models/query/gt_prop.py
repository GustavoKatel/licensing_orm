from .query_prop import QueryProp

class GTProp(QueryProp):
    '''
    GTProp defines the comparator matching values greater the initial value
    '''
    def compare(self, other_data):
        return self.data < other_data