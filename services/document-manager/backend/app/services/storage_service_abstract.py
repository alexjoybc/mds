import abc


class StorageService(abc.ABC):
    @abc.abstractmethod
    def upload_file(self, file_name):
        """
        Function to persist file on a storage implementation.
        """
        pass

    @abc.abstractmethod
    def download_file(self, path, display_name, as_attachment):
        """
        Function to retrieve file from a storage implementation.
        """
        pass

    @abc.abstractmethod
    def check_file(self, path):
        """
        Function to check if a file exists on a storage implementation.

        :param path: [description]
        :type path: [type]
        """
        pass
