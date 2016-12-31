import sqlite3



class SQLDB:
    def __init__(self):
        try:
            self.getCon()
        except:
            pass

        try:
            self.CreateTable()
        except:
            pass

        try:
            self.insertInitData()
        except Exception as e:
            print e
            pass

    def getCon(self):
        self.dbconnection = sqlite3.connect('/tmp/globalpnp.db')

    def CreateTable(self):
        cursor = self.dbconnection.cursor()
        cursor.execute('''CREATE TABLE metmetadata(name text primary key,ip text, port int,type text)''')
        cursor.execute('''CREATE TABLE snapdata(keyname text primary key,data text)''')
        self.dbconnection.commit()
        self.dbconnection.close()

    def insertInitData(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("Insert INTO metmetadata(name,port) values('inp',8200)")
        cursor.execute("Insert INTO metmetadata(name,port,ip) values('out',8500,'192.168.100.1')")
        cursor.execute("Insert INTO metmetadata(name,port,ip) values('outTee',8500,'192.168.100.1')")
        cursor.execute("Insert INTO metmetadata(name,port) values('cont',8100)")
        cursor.execute("Insert INTO snapdata(keyname,data) values('status','av')")
        cursor.execute("Insert INTO snapdata(keyname,data) values('prgid','01')")
        cursor.execute("Insert INTO snapdata(keyname,data) values('programs','a|b|c|d')")
        cursor.execute("Insert INTO snapdata(keyname) values('parent')")
        cursor.execute("Insert INTO snapdata(keyname) values('myname')")  #whether a b c d
        cursor.execute("Insert INTO snapdata(keyname) values('controljson')")
        cursor.execute("Insert INTO snapdata(keyname) values('seqjson')")
        cursor.execute("Insert INTO snapdata(keyname) values('myprj')")
        self.dbconnection.commit()
        self.dbconnection.close()

    def getInputDaemonPort(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT port FROM metmetadata WHERE name = 'inp'")
        return cursor.fetchone()[0]

    def getOutputDaemonPort(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT port FROM metmetadata WHERE name = 'out'")
        return cursor.fetchone()[0]

    def getOutputDaemonIP(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT ip FROM metmetadata WHERE name = 'out'")
        return cursor.fetchone()[0]

    def getControlDaemonPort(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT port FROM metmetadata WHERE name = 'cont'")
        return cursor.fetchone()[0]

    def getStatus(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT data FROM snapdata WHERE keyname = 'status'")
        return cursor.fetchone()[0]

    def getprgid(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT data FROM snapdata WHERE keyname = 'prgid'")
        return cursor.fetchone()[0]

    def getprograms(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT data FROM snapdata WHERE keyname = 'programs'")
        return cursor.fetchone()[0]

    def isPrgInMe(self,prg):
        prs=self.getprograms()
        prs=prs.split("|")
        if (prg in prs):
            return True
        return False

    def setPrgID(self,prgid):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE snapdata SET data = ? WHERE keyname = 'prgid' ''',(prgid,))
        self.dbconnection.commit()
        self.dbconnection.close()

    def setStatus(self,status):
        self.getCon()
        cursor = self.dbconnection.cursor()
        if(status):
            cursor.execute('''UPDATE snapdata SET data = 'av' WHERE keyname = 'status' ''')
        else:
            cursor.execute('''UPDATE snapdata SET data = 'nav' WHERE keyname = 'status' ''')
        self.dbconnection.commit()
        self.dbconnection.close()

    def setParent(self, parentIP):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE snapdata SET data = ? WHERE keyname = 'parent' ''', (parentIP,))
        self.dbconnection.commit()
        self.dbconnection.close()
        print "PARENIP:- ",parentIP

    def setMyName(self, name):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE snapdata SET data = ? WHERE keyname = 'myname' ''', (name,))
        self.dbconnection.commit()
        self.dbconnection.close()

    def getMyName(self):
        try:
            self.getCon()
            cursor = self.dbconnection.cursor()
            cursor.execute("SELECT data FROM snapdata WHERE keyname = 'myname'")
            return cursor.fetchone()[0]
        except:
            return None

    def getParent(self):
        try:
            self.getCon()
            cursor = self.dbconnection.cursor()
            cursor.execute("SELECT data FROM snapdata WHERE keyname = 'parent'")
            return cursor.fetchone()[0]
        except:
            return None

    def setControlJson(self,json):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE snapdata SET data = ? WHERE keyname = 'controljson' ''', (json,))
        self.dbconnection.commit()
        self.dbconnection.close()

    def setSeqJson(self,json):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE snapdata SET data = ? WHERE keyname = 'seqjson' ''', (json,))
        self.dbconnection.commit()
        self.dbconnection.close()

    def getControlJson(self):
        try:
            self.getCon()
            cursor = self.dbconnection.cursor()
            cursor.execute("SELECT data FROM snapdata WHERE keyname = 'controljson'")
            return cursor.fetchone()[0]
        except:
            return None

    def getSeqJson(self):
        try:
            self.getCon()
            cursor = self.dbconnection.cursor()
            cursor.execute("SELECT data FROM snapdata WHERE keyname = 'seqjson'")
            return cursor.fetchone()[0]
        except:
            return None


    def setOutputIp(self, ip):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE metmetadata SET ip = ? WHERE name = 'out' ''', (ip,))
        self.dbconnection.commit()
        self.dbconnection.close()

    def setOutputPort(self, port):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE metmetadata SET port = ? WHERE name = 'out' ''', (port,))
        self.dbconnection.commit()
        self.dbconnection.close()

    def setMyProgram(self,myprj):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE snapdata SET data = ? WHERE keyname = 'myprj' ''', (myprj,))
        self.dbconnection.commit()
        self.dbconnection.close()


    def setOutputIpTee(self, ip):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE metmetadata SET ip = ? WHERE name = 'outTee' ''', (ip,))
        self.dbconnection.commit()
        self.dbconnection.close()

    def setOutputPortTee(self, port):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute('''UPDATE metmetadata SET port = ? WHERE name = 'outTee' ''', (port,))
        self.dbconnection.commit()
        self.dbconnection.close()

    def getOutputDaemonIpTee(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT ip FROM metmetadata WHERE name = 'outTee'")
        return cursor.fetchone()[0]

    def getOutputDaemonPortTee(self):
        self.getCon()
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT port FROM metmetadata WHERE name = 'outTee'")
        return cursor.fetchone()[0]
# a=SQLDB()
# print a.getOutputDaemonPort()
# print a.getInputDaemonPort()
# print a.getprograms()
# print a.getControlDaemonPort()
# print a.getOutputDaemonIP()
# print a.isPrgInMe("a")
# print a.isPrgInMe("z")
# print a.getprgid()
# print a.getStatus()
# print a.getMyName()
# print a.getParent()
