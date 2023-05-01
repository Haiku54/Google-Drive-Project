import pyodbc
from IDataBase import *

connection_string = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=(local)\SQLEXPRESS;DATABASE=google_drive_projrct_dataBase;Trusted_Connection=yes;'

class SQLDataBase(IDataBase):
    def __init__(self):
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
        OUTPUT INSERTED.RequestID
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (email, name, requested_file_id, returned_file_id, request_date, is_copied))
        
        # Get the generated RequestID using OUTPUT INSERTED
        request_id = self.cursor.fetchone()[0]

        self.conn.commit()

        return request_id





    def insert_activeFiles(self, returned_file_id, requested_file_id):
        query = '''
        INSERT INTO ActiveFiles (ReturnedFileID, RequestedFileID)
        VALUES (?, ?)
        '''
        self.cursor.execute(query, (returned_file_id, requested_file_id))
        self.conn.commit()

    
    def is_RequestedFiles_in_table(self, file_id):
        query = '''
        SELECT COUNT(*) FROM RequestedFiles WHERE FileID = ?
        '''
        self.cursor.execute(query, (file_id,))
        count = self.cursor.fetchone()[0]

        return count > 0



    def close_connection(self):
        self.cursor.close()
        self.conn.close()
