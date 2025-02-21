
import time
import base64
import os

from chat import Chat

class Project(Chat):

    def __init__(self):
        super().__init__()
        self.dashboard_payload = None
        self.uploaded_files = []
        pass

    def delete(self):
            super().reset()
            self.dashboard_payload = None
            self._delete_uploaded_files()
            print("TODO: Reset is only mocked currently.")
            pass

    def _delete_uploaded_files(self):
        for file in self.uploaded_files:
            try:
                os.remove(f"uploads/{file}")
            except Exception as e:
                print(f"Error deleting file: {str(e)}")
        self.uploaded_files = []
        pass

    def get_dashboard_payload(self):
        return self.dashboard_payload
        pass

    def set_dashboard_payload(self, payload):
        self.dashboard_payload = payload
        pass

    def upload_file(self, upload_contents, filename):
        if upload_contents is not None:
            content_type, content_string = upload_contents.split(',')
            decoded = base64.b64decode(content_string)
            try:
                with open(f"uploads/{filename}", "wb") as f:
                    f.write(decoded)
                self.add_message("System", "Upload succeeded")
                self.uploaded_files.append(filename)
            except Exception as e:
                self.add_message("System", f"Error uploading file: {str(e)}")
        pass

    def get_uploaded_files(self):
        return self.uploaded_files
        pass