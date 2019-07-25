import pyodbc as db
import sqlalchemy as sa
"""
to-do: create connectorusing SQL Alchemy which:
- create classes based on database architecture
- provide abstract, methods to:
    basic: select, insert, delete, update
    temporal tables usage
    looking for duplicates on db and using temporal tables or some other methods to mark that type of records
    merging data
"""


class MSDBConnector:

    def __init__(self):
        self.sql = ''
        self.path = ''
        self.conString = ''

    def setPath(self, path):
        self.path = path
        with open(self.path,"r") as file:
            self.conString = file.read()
            """
                                          'Driver={SQL Server};'
                                          'Server=server_name;'
                                          'Database=db_name;'
                                          'Trusted_Connection=yes;'
            """

    def setSQL(self, sql):
        self.sql = sql

    def connect(self, get=None):
        con = db.connect(self.conString)
        cursor = con.cursor()
        if get:
            results = [row for row in cursor.execute(self.sql)]
            con.close
            return results
        else:
            cursor.execute(self.sql)
            con.commit()
            print("executed")
            con.close


