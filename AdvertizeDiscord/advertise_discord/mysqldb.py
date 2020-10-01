import pymysql.cursors

class DB:
    def __init__(self, host='localhost',                                                                                                                            
                                 user='root',                                                                                                                                 
                                 password='',
                                 db='database',
                                 charset='utf8mb4',                                    
                                 cursorclass=pymysql.cursors.DictCursor):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.cursorclass = cursorclass
        self.cursor = None

    def getConnection(self):                                                                                                                                            
        return pymysql.connect(host=self.host,                                                                                                                            
                                    user=self.user,                                                                                                                   
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset,
                                    cursorclass=self.cursorclass)

    def getCursor(self, connection=None):
        return connection.cursor() if connection else self.getConnection().cursor()
    
    def execute(self, cmd, args:tuple=None, cursor=None):
        if not cursor:
            cursor = self.getCursor()
        return cursor.execute(cmd, args)

