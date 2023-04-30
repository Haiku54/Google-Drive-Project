import pyodbc
from IDataBase import *

class SQLDataBase(IDataBase):
    def __init__(self, connection_string):
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()


    def insert_requested_files(self, file_id, file_size):
        query = '''
        INSERT INTO RequestedFiles (FileID, FileSize)
        VALUES (?, ?)
        '''
        self.cursor.execute(query, (file_id, file_size))
        self.conn.commit()

    def insert_returned_files(self, file_id, requested_file_id):
        query = '''
        INSERT INTO ReturnedFiles (FileID, RequestedFileID, CreationDate)
        VALUES (?, ?, GETDATE())
        '''
        self.cursor.execute(query, (file_id, requested_file_id))
        self.connection.commit()


    def insert_requests(self, email, name, requested_file_id, returned_file_id, request_date, is_copied):
        query = '''
        INSERT INTO Requests (Email, Name, RequestedFileID, ReturnedFileID, RequestDate, IsCopied)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (email, name, requested_file_id, returned_file_id, request_date, is_copied))
        
        # Get the generated RequestID
        self.cursor.execute("SELECT SCOPE_IDENTITY();")
        request_id = self.cursor.fetchone()[0]

        self.conn.commit()
        
        return request_id


    def insert_active_files(self, returned_file_id, requested_file_id):
        query = '''
        INSERT INTO ActiveFiles (ReturnedFileID, RequestedFileID)
        VALUES (?, ?)
        '''
        self.cursor.execute(query, (returned_file_id, requested_file_id))
        self.conn.commit()


    def close_connection(self):
        self.cursor.close()
        self.conn.close()
