from inspect import currentframe, getframeinfo
import pathlib
import sqlite3
from sqlite3 import Error
from datetime import date
from datetime import date

class Db:
    initialisiert = False
    fileDb = ""
    conn = None

    @staticmethod
    def aktuellesVerzeichnis():
        filename = getframeinfo(currentframe()).filename
        parent = pathlib.Path(filename).resolve().parent
        return parent

    @staticmethod
    def init():
        Db.initialisiert = True
        Db.Db = Db.aktuellesVerzeichnis() / "saved.dat"


        Db.conn = Db.erstelleVerbindung(Db.Db)

        sql_create_events_table = """ CREATE TABLE IF NOT EXISTS events (
                                                id integer PRIMARY KEY,
                                                inhalt text,
                                                zeitStartMin integer,
                                                zeitEndeMin integer,
                                                dateOrdinal integer,
                                                state integer
                                            ); """

        sql_create_zeiten_table = """CREATE TABLE IF NOT EXISTS zeiten (
                                        id integer PRIMARY KEY,
                                        zeitMin integer
                                    );"""

        Db.erstelleTabelle(Db.conn, sql_create_events_table)
        Db.erstelleTabelle(Db.conn, sql_create_zeiten_table)

    @staticmethod
    def erstelleVerbindung(db_file):
        """ create a database connection to the SQLite database
                specified by db_file
            :param db_file: database file
            :return: Connection object or None
            """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    @staticmethod
    def erstelleTabelle(conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    @staticmethod
    def addEvent(conn, event):
        from EventManager import EventManager as EM
        sql = ''' INSERT INTO events(inhalt,zeitStartMin, zeitEndeMin, dateOrdinal,state)
                      VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        state = 0
        if event.istPause: state = 1
        if event == EM.mittagspause: state = 2
        cur.execute(sql, (event.text, event.startzeit.zeitInMinuten(), event.endzeit.zeitInMinuten(), event.startzeit.datum.toordinal(), state))
        return cur.lastrowid

    @staticmethod
    def addZeit(conn, zeit):
        sql = ''' INSERT INTO zeiten(zeitMin)
                              VALUES(?) '''
        cur = conn.cursor()
        cur.execute(sql, (zeit.zeitInMinuten(),))
        return cur.lastrowid

    @staticmethod
    def updateEvent(conn, event):
        from EventManager import EventManager as EM
        """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
        sql = ''' UPDATE events
                  SET inhalt = ? ,
                      zeitStartMin = ? ,
                      zeitEndeMin = ?,
                      dateOrdinal = ?,
                      state = ?
                  WHERE id = ?'''
        state = 0
        if event.istPause: state = 1
        if event == EM.mittagspause: state = 2
        cur = conn.cursor()
        cur.execute(sql, (event.text, event.startzeit.zeitInMinuten(), event.endzeit.zeitInMinuten(), event.startzeit.datum.toordinal(), state, event.id))
        conn.commit()

    @staticmethod
    def updateZeit(conn, zeit):
        from TimeManager import TimeManager as TM
        """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
        sql = ''' UPDATE zeiten
                  SET zeitMin = ?
                  WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, (zeit.zeitInMinuten(), zeit.id))
        conn.commit()

    @staticmethod
    def erhalteAlleEvents(conn):
        from Event import Event
        from Zeit import Zeit
        from EventManager import EventManager as EM
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM events")

        rows = cur.fetchall()
        events = []

        for row in rows:
            zeitStart = Zeit(0, 0)
            zeitEnde = Zeit(0, 0)
            zeitStart.vonMinuten(row[2])
            zeitEnde.vonMinuten(row[3])
            event = Event(zeitStart, zeitEnde)
            event.id = row[0]
            event.text = row[1]
            event.startzeit.datum = date.fromordinal(row[4])
            event.endzeit.datum = event.startzeit.datum
            if row[5] == 1: event.istPause = True
            if row[5] == 2:
                EM.mittagspause = event
            else:
                events.append(event)
        return events

    @staticmethod
    def erhalteAlleEventsAm(conn, datum=date.today()):
        from Event import Event
        from Zeit import Zeit
        from EventManager import EventManager as EM
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        datum = datum.toordinal()
        cur = conn.cursor()
        cur.execute('''SELECT * FROM events WHERE dateOrdinal=?''',(datum,))

        rows = cur.fetchall()
        events = []

        for row in rows:
            zeitStart = Zeit(0, 0)
            zeitEnde = Zeit(0, 0)
            zeitStart.vonMinuten(row[2])
            zeitEnde.vonMinuten(row[3])
            event = Event(zeitStart, zeitEnde)
            event.id = row[0]
            event.text = row[1]
            event.startzeit.datum = date.fromordinal(row[4])
            event.endzeit.datum = event.startzeit.datum
            if row[5] == 1: event.istPause = True
            if row[5] == 2:
                EM.mittagspause = event
            else:
                events.append(event)
        return events
    @staticmethod
    def erhalteAlleZeiten(conn):
        from Zeit import Zeit
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM zeiten")

        rows = cur.fetchall()
        zeiten = []
        for row in rows:
            zeit = Zeit(0, 0)
            zeit.id = row[0]
            zeit.vonMinuten(row[1])
            zeiten.append(zeit)
        return zeiten

    @staticmethod
    def entferneEvent(conn, event):
        """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:
        """
        sql = 'DELETE FROM events WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (event.id,))
        conn.commit()

    @staticmethod
    def entferneZeit(conn, zeit):
        """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:
        """
        sql = 'DELETE FROM zeiten WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (zeit.id,))
        conn.commit()