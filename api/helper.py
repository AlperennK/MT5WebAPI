from api.connect import Connection
from api.connect import Credentials1


class MT5Helper(object):
    def __init__(self):
        self.conn=Connection()

    def add_user(self):
        self.conn.data={'login': '0', 'pass_main':Credentials1['DEFAULT_MAIN_PASS'], 'pass_investor':Credentials1['DEFAULT_PASS_INVESTOR'], 'group': 'market-en', 'name': 'testertest', 'leverage': '100',
                                                     'city':'Podgorica', 'Country':'Montenegro'}

        url_add=self.conn.url_generate(urlpath='user_add')
        return self.conn._request(method='get', url=url_add)

    def del_user(self, user):
        self.conn.data={'login': user}
        url_del=self.conn.url_generate(urlpath='user_delete')
        return self.conn._request(method='get', url=url_del)

    def change_group(self, user, group):
        self.conn.data={'login': user, 'group':group}
        return self.conn._request(method='get', url=self.conn.url_generate('user_update'))


