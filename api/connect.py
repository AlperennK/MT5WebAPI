import requests
from requests.exceptions import ConnectionError
import urllib
import json
from hashlib import md5
import secrets
import sys
from api.credentials import Credentials1

"""
Possible api calls to be used in query function can be checked
https://support.metaquotes.net/en/docs/mt5/api/webapi_https
https://conf.fxclub.org/display/MET/MT5WebAPIExtention
"""
class Connection(object):

    def __init__(self):
        self.mt5server=Credentials1['MT5_IP']
        self.mt5port=Credentials1['MT5_PORT']
        self.login=Credentials1['login_mt5']
        self.password=Credentials1['MT5_PASSWORD']
        self.version=Credentials1['version']
        self.agent=Credentials1['agent']
        self.logintest=Credentials1['login_mt5']
        self.baseurl='https://mt5-fcil-real.test.fxclub.org/'

        self.authenticate()


    def authenticate(self):
        self.payload={'version':self.version, 'agent':self.agent, 'login': self.login, 'type': self.agent}
        self.session=requests.Session()
        self.session.headers.update({'MT5WEBAPI': 'true'})
        self.session.headers.update({"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded"})
        self.response=None
        self.data=self.payload
        self.url=self.url_generate('auth_start')

        try:
            response=self.session.get(self.url)
        except ConnectionError:
            print(f"The connection to {self.url} is failed")
            sys.exit(1)

        str_response=response.content.decode('utf8')

        json_response=json.loads(str_response)
        #Converting srv_rand response from json to bytearray
        srv_rand=bytearray.fromhex(json_response['srv_rand'])

        t1 = md5(self.password.encode('utf-16le')).digest()
        t2 = 'WebAPI'.encode('ascii')
        pwd_hash_api = md5(t1 + t2).digest()

        srv_rand_answer= md5(pwd_hash_api + srv_rand).hexdigest()
        cli_rand=secrets.token_hex(16)
        param_answer={'srv_rand_answer':srv_rand_answer, 'cli_rand':cli_rand}
        url_answer='https://mt5-fcil-real.test.fxclub.org/auth_answer?'
        url_answer=url_answer+urllib.parse.urlencode(param_answer)

        try:
            response2=self.session.get(url_answer)
        except ConnectionError:
            print(f"The connection to {self.url} is failed")
            sys.exit(1)

        json_response2=json.loads(response2.content.decode('utf8'))
        cli_rand_answer=json_response2['cli_rand_answer']
        return


    def url_generate(self, urlpath):
        return self.baseurl + str(urlpath) + '?' + urllib.parse.urlencode(self.data)


    def _request(self, method, url, **kwargs):
        data=kwargs.get('data', None)
        if data and isinstance(data, dict):
            kwargs['data'] = data

        if data and (method == 'get'):
            del(kwargs['data'])

        self.response=getattr(self.session, method)(url, **kwargs)
        return self.query_response()

    """
    Drivers for requests
    """
    def _get(self, path, **kwargs):
        return self._request('get', url= self.url_generate(urlpath=path), **kwargs)

    def _post(self, path, **kwargs):
        return self._request('post', url=self.url_generate(urlpath=path), **kwargs)

    def _put(self, path, **kwargs):
        return self._request('put', url=self.url_generate(urlpath=path), **kwargs)

    def _del(self, path, **kwargs):
        return self._request('delete', url=self.url_generate(urlpath=path), **kwargs)

    def post_query(self, params):
        self.data=params
        self.url=self.url_generate()
        self.response=self.session.post(self.url, data=self.data)
        return self.query_response()

    def query_response(self):
        if self.response.status_code not in (200,201,202):
            self.response.raise_for_status()
            print(f"The connection to {self.url} is failed")

        return json.loads(self.response.content.decode('utf8'))



#answer=conn.query(method='FXC_GETDEPOSIT', params={'login':'555019075', 'group':'market-en'})
#FXC_CHANGEDEPOSIT|OPERATION_ID=%d|LOGIN=%d|DEPOSIT=%.2f|COMMENT=%s|CHECKOPEN=%d|MIN_BALANCE=%d
#answer=conn.query(method='FXC_CHANGEDEPOSIT', params={'OPERATION_ID':'91021113', 'LOGIN': '555019077', 'DEPOSIT':'1000', 'COMMENT': 'deposited'})
#answer=conn.query(method='user_add', params={'login': '0', 'pass_main':Credentials1['DEFAULT_MAIN_PASS'], 'pass_investor':Credentials1['DEFAULT_PASS_INVESTOR'], 'group': 'market-en', 'name': 'testertest', 'leverage': '100'})

#answer=conn.change_group(login=Credentials1['login_test'] ,group="market-en")
#print(conn.url_generate(method='group_get', payload={'group':'market-en'}))
#print(conn.url_generate(method='group_get', payload={'':''}))

#print(answer.content)
#print(type(answer))
