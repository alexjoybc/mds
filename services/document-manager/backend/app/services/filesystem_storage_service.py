from flask import send_file

from storage_service_abstract import StorageService


class FilesystemStorageService(StorageService):
    def upload_file():


    def tus_upload_begin():


    def tus_upload_resume():


    def check_file():
        return 


    def download_file(self, path, display_name, as_attachment):
        send_file(filename_or_fp=path,
                  attachment_filename=display_name,
                  as_attachment=as_attachment)
