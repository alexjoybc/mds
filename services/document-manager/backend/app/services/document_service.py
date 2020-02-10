
from app.constants import FILE_UPLOAD_SIZE, FILE_UPLOAD_OFFSET, FILE_UPLOAD_PATH, DOWNLOAD_TOKEN, TIMEOUT_24_HOURS, TUS_API_VERSION, TUS_API_SUPPORTED_VERSIONS, FORBIDDEN_FILETYPES
from werkzeug.exceptions import BadRequest, NotFound, Conflict, RequestEntityTooLarge, InternalServerError
from app.config import Config

from app.models.document import Document

from filesystem_storage_service import FilesystemStorageService
from object_store_storage_service import ObjectStoreStorageService


class DocumentService:
    fs_store = FileStorageService()
    object_store = ObjectStoreStorageService() if Config.OBJECT_STORE_ENABLED else None

    def transfer_to_object_store(self, document_guid):
        """
        Will change a document's storage location from the file system to the configured object store
        
        :param document_guid: Document GUID to be transferred
        :type document_guid: str
        """
        return NotImplementedError

    def transfer_to_fs(self, document_guid):
        """
        Will change a document's storage location from the configured object store to the file system
        
        :param document_guid: Document GUID to be transferred
        :type document_guid: str
        """
        return NotImplementedError


    def download_file(self, document_guid, as_attachment=True):
        """[summary]
        
        :param document_guid: [description]
        :type document_guid: str
        :param as_attachment: Force download as attachment or let the browser determine, defaults to True
        :type as_attachment: bool, optional
        :return: File download response
        """

        document = Document.query.filter_by(document_guid=document_guid).first()

        if not document:
            raise NotFound('Could not find the document corresponding to the token')
        
        return NotImplementedError


    def tus_upload_begin(self, document_guid, data):

        fs_store.tus_upload_begin()

        file_size = request.headers.get('Upload-Length')
        max_file_size = current_app.config["MAX_CONTENT_LENGTH"]
        if not file_size:
            raise BadRequest('Received file upload of unspecified size')
        file_size = int(file_size)
        if file_size > max_file_size:
            raise RequestEntityTooLarge(
                f'The maximum file upload size is {max_file_size/1024/1024}MB.')

        data = self.parser.parse_args()
        filename = data.get('filename')
        if not filename:
            raise BadRequest('File name cannot be empty')
        if filename.endswith(FORBIDDEN_FILETYPES):
            raise BadRequest('File type is forbidden')

        document_guid = str(uuid.uuid4())
        base_folder = current_app.config['UPLOADED_DOCUMENT_DEST']

        # BEGIN Document Save
        try:
            DocumentService.save(data.get('folder'))
        folder = data.get('folder')
        folder = os.path.join(base_folder, folder)
        file_path = os.path.join(folder, document_guid)
        pretty_folder = data.get('pretty_folder')
        pretty_path = os.path.join(base_folder, pretty_folder, filename)

        try:
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(file_path, "wb") as f:
                f.seek(file_size - 1)
                f.write(b"\0")
        except IOError as e:
            raise InternalServerError('Unable to create file')

        cache.set(FILE_UPLOAD_SIZE(document_guid), file_size, TIMEOUT_24_HOURS)
        cache.set(FILE_UPLOAD_OFFSET(document_guid), 0, TIMEOUT_24_HOURS)
        cache.set(FILE_UPLOAD_PATH(document_guid), file_path, TIMEOUT_24_HOURS)

        document_info = Document(
            document_guid=document_guid,
            full_storage_path=file_path,
            upload_started_date=datetime.utcnow(),
            file_display_name=filename,
            path_display_name=pretty_path,
        )
        document_info.save()

        return document_guid



    def tus_upload_resume(self, document_guid):

        file_path = cache.get(FILE_UPLOAD_PATH(document_guid))
        if file_path is None or not os.path.lexists(file_path):
            raise NotFound('PATCH sent for a upload that does not exist')

        request_offset = int(request.headers.get('Upload-Offset', 0))
        file_offset = cache.get(FILE_UPLOAD_OFFSET(document_guid))
        if request_offset != file_offset:
            raise Conflict("Offset in request does not match uploaded file's offset")

        chunk_size = request.headers.get('Content-Length')
        if chunk_size is None:
            raise BadRequest('No Content-Length header in request')
        chunk_size = int(chunk_size)

        new_offset = file_offset + chunk_size
        file_size = cache.get(FILE_UPLOAD_SIZE(document_guid))
        if new_offset > file_size:
            raise RequestEntityTooLarge(
                'The uploaded chunk would put the file above its declared file size.')

        try:
            with open(file_path, "r+b") as f:
                f.seek(file_offset)
                f.write(request.data)
        except IOError as e:
            raise InternalServerError('Unable to write to file')

        if new_offset == file_size:
            # File transfer complete.
            doc = Document.find_by_document_guid(document_guid)
            doc.upload_completed_date = datetime.utcnow()
            doc.save()

            cache.delete(FILE_UPLOAD_SIZE(document_guid))
            cache.delete(FILE_UPLOAD_OFFSET(document_guid))
            cache.delete(FILE_UPLOAD_PATH(document_guid))
        else:
            # File upload still in progress
            cache.set(FILE_UPLOAD_OFFSET(document_guid), new_offset, TIMEOUT_24_HOURS)

        response = make_response('', 204)
        response.headers['Tus-Resumable'] = TUS_API_VERSION
        response.headers['Tus-Version'] = TUS_API_SUPPORTED_VERSIONS
        response.headers['Upload-Offset'] = new_offset
        response.headers[
            'Access-Control-Expose-Headers'] = "Tus-Resumable,Tus-Version,Upload-Offset"
        return response