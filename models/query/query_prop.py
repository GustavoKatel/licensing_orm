
class QueryProp(object):
    '''
    QueryProp defines the comparator interface to enhance query in models
    '''
    def __init__(self, data):
        self.data = data

    def __eq__(self, other_data):
        return self.compare(other_data)

    def compare(self, other_data):
        return self.data == other_data