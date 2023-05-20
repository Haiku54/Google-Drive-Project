import mysql.connector
import datetime
import json
import atexit

# Load the database configuration from json file
with open('data_base/database_config.json') as f:
    config = json.load(f)

class MySQLDataBase:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()


    def insert_requested_files(self, file_id, file_size):
        query = '''
        INSERT INTO RequestedFiles (FileID, FileSize)
        VALUES (%s, %s)
        '''
        self.cursor.execute(query, (file_id, file_size))
        self.conn.commit()


    def insert_returned_files(self, file_id, requested_file_id):
        query = '''
        INSERT INTO ReturnedFiles (FileID, RequestedFileID, CreationDate)
        VALUES (%s, %s, %s)
        '''
        #creation current date
        now = datetime.datetime.now()
        self.cursor.execute(query, (file_id, requested_file_id, now))
        self.conn.commit()


    def insert_requests(self, email, name, requested_file_id, returned_file_id, request_date, is_copied, folderID):
        query = '''
        INSERT INTO Requests (Email, Name, RequestedFileID, ReturnedFileID, RequestDate, IsCopied, FolderID)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(query, (email, name, requested_file_id, returned_file_id, request_date, is_copied, folderID))
        
        # Get the generated RequestID using lastrowid
        request_id = self.cursor.lastrowid

        self.conn.commit()

        return request_id


    def get_email_by_request_id(self, request_id):
        query = '''
        SELECT Email
        FROM Requests
        WHERE RequestID = %s
        '''
        self.cursor.execute(query, (request_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None


    def get_requestFile_id_by_request_id(self, request_id):
        query = '''
        SELECT RequestedFileID
        FROM Requests
        WHERE RequestID = %s
        '''
        self.cursor.execute(query, (request_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None


    def insert_activeFiles(self, returned_file_id, requested_file_id):
        query = '''
        INSERT INTO ActiveFiles (ReturnedFileID, RequestedFileID)
        VALUES (%s, %s)
        '''
        self.cursor.execute(query, (returned_file_id, requested_file_id))
        self.conn.commit()


    def is_RequestedFiles_in_table(self, file_id):
        query = '''
        SELECT COUNT(*) FROM RequestedFiles WHERE FileID = %s
        '''
        self.cursor.execute(query, (file_id,))
        count = self.cursor.fetchone()[0]

        return count > 0


    def update_is_copied_to_true(self, request_id):
        query = '''
        UPDATE Requests
        SET IsCopied = 1
        WHERE RequestID = %s
        '''
        self.cursor.execute(query, (request_id,))  # Note the comma after request_id
        self.conn.commit()

    
    def update_file_size_in_requested_files(self, file_id, file_size):
        query = '''
        UPDATE RequestedFiles
        SET FileSize = %s
        WHERE FileID = %s AND FileSize IS NULL
        '''
        self.cursor.execute(query, (file_size, file_id))
        self.conn.commit()


    def update_request_with_returned_file(self, request_id, returned_file_id):
        query = '''
        UPDATE Requests
        SET ReturnedFileID = %s
        WHERE RequestID = %s
        '''
        self.cursor.execute(query, (returned_file_id, request_id))
        self.conn.commit()


    def insert_into_active_files(self, requested_file_id, returned_file_id):
        query = '''
        INSERT INTO ActiveFiles (ReturnedFileID, RequestedFileID)
        VALUES (%s, %s)
        '''
        self.cursor.execute(query, (returned_file_id, requested_file_id))
        self.conn.commit()


    def get_returned_file_id_active(self, requested_file_id):
        query = '''
        SELECT ReturnedFileID
        FROM ActiveFiles
        WHERE RequestedFileID = %s
        '''
        self.cursor.execute(query, (requested_file_id,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            return None


    def is_email_authorized(self,email):
        query = "SELECT COUNT(*) FROM AuthorizedEmails WHERE Email = %s"
        self.cursor.execute(query, (email,))
        count = self.cursor.fetchone()[0]
        return count > 0


    def delete_files_from_active_files(self, list_of_files):
        query = '''
        DELETE FROM ActiveFiles
        WHERE ReturnedFileID = %s
        '''
        for file in list_of_files:
            self.cursor.execute(query, (file,))
            self.conn.commit()


    def get_requsted_folderID(self,request_id):
        query = '''
        SELECT FolderID FROM Requests WHERE RequestID = %s
        '''
        self.cursor.execute(query, (request_id,))
        result = self.cursor.fetchone()[0]
        return result


    def is_user_uploaded_half_GB_last_2_hours(self, email):
        """
        Returns True if the user has uploaded more than half a gigabyte in the last two hours, False otherwise.
        
        :param email: The email of the user.
        :return: True if the user has uploaded more than half a gigabyte in the last two hours, False otherwise.
        """
        two_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=2)

        query = '''
        SELECT rf.FileID, rf.FileSize
        FROM Requests AS r
        JOIN RequestedFiles AS rf ON r.RequestedFileID = rf.FileID
        WHERE r.Email = %s
        AND r.RequestDate >= %s
        AND r.ReturnedFileID IS NOT NULL
        AND r.IsCopied IS NOT NULL
        '''

        # Execute the query with the email and time as parameters
        self.cursor.execute(query, (email, two_hours_ago))

        # Fetch the results.
        results = self.cursor.fetchall()

        # Calculate the total size of the returned files
        total_size = sum([result[1] for result in results])

        # Return True if the total size is greater than half a gigabyte, False otherwise
        return total_size > (0.5 * 1024 * 1024 * 1024)


    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        print("Connection to data base closed")