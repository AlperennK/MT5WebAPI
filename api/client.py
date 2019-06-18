import pymysql
import pymysql.cursors
from api.credentials import Credentials1



class Client(object):
    PORT=Credentials1['PORT']
    BUFFER_SIZE=Credentials1['BUFFER_SIZE']
    CHARSET_DB=Credentials1['CHARSET_DB']

    def __init__(self):
        self.cursor=self._init_cursor()
        self.NAME_DB = Credentials1['NAME_DB']

    def _init_cursor(self):
        try:
            connection = pymysql.connect(host=Credentials1['DB_IP'], connect_timeout= Credentials1['DB_TIMEOUT'],
                                 user=Credentials1['USER_DB'],
                                 password=Credentials1['PASS_DB'],
                                 db=Credentials1['NAME_DB'],
                                 charset=Credentials1['CHARSET_DB'],
                                 cursorclass=pymysql.cursors.DictCursor)


        except pymysql.OperationalError as e:
            raise SystemExit('Database connection can not be established ', str(e))

        return connection.cursor()


    def check_login(self, lognum):
        cur=self.cursor
        cur.execute("SELECT * FROM " + str(self.NAME_DB) + ".mt5_users WHERE LOGIN = %s", (lognum,))
        db_res=cur.fetchone()
        if db_res !=None:
            return db_res
        print(db_res)
        if db_res != None:
            return db_res

#Equity and Margin Should be refactored to more genreic function.

#Checks margin value by ticket number
    def check_margin(self, ticket, activity):
        cur=self.cursor
        cur.execute("SELECT * FROM mt_real.sf_accountdetails WHERE mt_real.sf_accountdetails.ActivityLog =(select Activitylog from mt_real.sf_activitytradedetails where mt_real.sf_activitytradedetails.Ticket=%s and mt_real.sf_activitytradedetails.TradeActivity=%s)", (ticket, activity,))
        db_res=cur.fetchone()
        if db_res !=None:
            return db_res
        print(db_res)
        if db_res != None:
            return db_res


#'1', 'Login'
#'2', 'Logout'
#'3', 'Operation with order/position'
#'4', 'Stop out'
#'5', 'Account group changed

    def check_lastip(self, lognum, typeact):
        cur=self.cursor
        cur.execute("SELECT a.IP FROM sf_activitylog as a \
        WHERE a.id = (SELECT max(id) FROM sf_activitylog as b WHERE b.Login = %s and b.TypeAct = %s)", (lognum, typeact,))
        db_res=cur.fetchone()
        if db_res !=None:
            return db_res['IP']
        print(db_res)
        if db_res != None:
            return db_res

    def check_last_trade(self):
        cur=self.cursor
        cur.execute("SELECT MAX(TICKET) FROM mt4_trades")
        db_res=cur.fetchone()
        if db_res != None:
            return db_res

    def check_trade(self, order):
        cur=self.cursor
        cur.execute("SELECT * FROM mt4_trades WHERE TICKET = %s", (order,))
        db_res=cur.fetchone()
        if db_res !=None:
            return db_res

    def generate_operation_id(self):
        return self.check_last_trade()['MAX(TICKET)'] + 1

    def get_last_ip_mt5(self,lognum):
        cur=self.cursor
        cur.execute("SELECT * FROM mt5_real.clientconnection WHERE login= %s AND connectioneventtypeID=0 ORDER BY(ID) DESC", (lognum,))
        db_res=cur.fetchone()
        if db_res !=None:
            return db_res


#SELECT * FROM sf_activitylog as a
#WHERE a.id = (SELECT max(id) FROM sf_activitylog as b WHERE b.Login = 995117396 and b.TypeAct = 3)
