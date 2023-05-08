import pyodbc
from data_base.IDataBase import *

connection_string = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=(local)\SQLEXPRESS;DATABASE=google_drive_projrct_dataBase;Trusted_Connection=yes;'

class SQLDataBase(IDataBase):
    _instance = None

    #singlton
    def __new__(cls): 
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    

    def __init__(self):
        if not hasattr(self, 'conn'):
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
        self.conn.commit()


    def insert_requests(self, email, name, requested_file_id, returned_file_id, request_date, is_copied,folderID):
        query = '''
        INSERT INTO Requests (Email, Name, RequestedFileID, ReturnedFileID, RequestDate, IsCopied,FolderID)
        OUTPUT INSERTED.RequestID
        VALUES (?, ?, ?, ?, ?, ?,?)
        '''
        self.cursor.execute(query, (email, name, requested_file_id, returned_file_id, request_date, is_copied,folderID))
        
        # Get the generated RequestID using OUTPUT INSERTED
        request_id = self.cursor.fetchone()[0]

        self.conn.commit()

        return request_id


    def get_email_by_request_id(self, request_id):
        query = '''
        SELECT Email
        FROM Requests
        WHERE RequestID = ?
        '''
        self.cursor.execute(query, (request_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None


    def get_requestFile_id_by_request_id(self, request_id):
        query = '''
        SELECT RequestedFileID
        FROM Requests
        WHERE RequestID = ?
        '''
        self.cursor.execute(query, (request_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None


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
    

    def update_is_copied_to_true(self, request_id):
        query = '''
        UPDATE Requests
        SET IsCopied = 1
        WHERE RequestID = ?
        '''
        self.cursor.execute(query, (request_id))
        self.conn.commit()

    
    def update_file_size_in_requested_files(self, file_id, file_size):
        query = '''
        UPDATE RequestedFiles
        SET FileSize = ?
        WHERE FileID = ? AND FileSize IS NULL
        '''
        self.cursor.execute(query, (file_size, file_id))
        self.conn.commit()


    def update_request_with_returned_file(self, request_id, returned_file_id):
        query = '''
        UPDATE Requests
        SET ReturnedFileID = ?
        WHERE RequestID = ?
        '''
        self.cursor.execute(query, (returned_file_id, request_id))
        self.conn.commit()

    
    def insert_into_active_files(self, requested_file_id, returned_file_id):
        query = '''
        INSERT INTO ActiveFiles (ReturnedFileID, RequestedFileID, CreationDate)
        VALUES (?, ?, GETDATE())
        '''
        self.cursor.execute(query, (returned_file_id, requested_file_id))
        self.conn.commit()


    def get_returned_file_id_active(self, requested_file_id):
        query = '''
        SELECT ReturnedFileID
        FROM ActiveFiles
        WHERE RequestedFileID = ?
        '''
        self.cursor.execute(query, (requested_file_id,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            return None
        

    def is_email_authorized(self,email):
        query = f"SELECT COUNT(*) FROM AuthorizedEmails WHERE Email = ?"
        self.cursor.execute(query, email)
        count = self.cursor.fetchone()[0]
        return count > 0
    

    def delete_files_from_active_files(self, list_of_files):
        query = '''
        DELETE FROM ActiveFiles
        WHERE ReturnedFileID = ?
        '''
        for file in list_of_files:
            self.cursor.execute(query, (file,))
            self.conn.commit()

    
    def get_requsted_folderID(self,request_id):
        query = '''
        SELECT FolderID FROM Requests WHERE RequestID = ?
        '''
        self.cursor.execute(query, (request_id,))
        result = self.cursor.fetchone()[0]
        return result




    def close_connection(self):
        self.cursor.close()
        self.conn.close()
