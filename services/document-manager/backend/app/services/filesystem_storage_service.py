from flask import send_file

from storage_service_abstract import StorageService


class FilesystemStorageService(StorageService):
    def upload_file():
        

    def download_file(self, path, display_name, as_attachment):
        send_file(filename_or_fp=path,
                  attachment_filename=display_name,
                  as_attachment=as_attachment)
