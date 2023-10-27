from mock import MagicMock
from mechanics.storage import upload_file, list_files_in_folder, get_file_in_folder, download_file

class TestUploadFile:
    def test_upload_file(self, mocker):
        # Mock the s3.put_object function to return a mock response
        mock_response = {}
        mocker.patch('mechanics.storage.s3.put_object', return_value=mock_response)

        # define a mock file that has a file name and a read method
        name = "mock-file"
        file = MagicMock(filename=name, file=MagicMock(read=MagicMock(return_value="mock-file-content")))

        # call the function 
        result = upload_file(file)
        assert f"s3.amazonaws.com/pdf_files/{name}" in result

    def test_upload_file_error_handling(self, mocker):
        # Mock the s3.put_object function to raise an exception
        mocker.patch('mechanics.storage.s3.put_object', side_effect=Exception("Mock error"))

        # call the function 
        try:
            upload_file("mock file")
        except Exception as e:
            assert str(e) == "Error uploading file"


class TestListFilesInFolder:
    def test_list_files_in_folder(self, mocker):
        # Mock the s3.list function to return a mock response
        mock_response = {
            "Contents": [
                {"Key": "pdf_files/mock-file-1"},
                {"Key": "pdf_files/mock-file-2"},
            ]
        }
        mocker.patch('mechanics.storage.s3.list_objects_v2', return_value=mock_response)

        # call the function 
        result = list_files_in_folder()
        assert result == ["pdf_files/mock-file-1", "pdf_files/mock-file-2"]

    def test_list_files_in_folder_error_handling(self, mocker):
        # Mock the s3.list function to raise an exception
        mocker.patch('mechanics.storage.s3.list_objects_v2', side_effect=Exception("Mock error"))

        # call the function 
        try:
            list_files_in_folder()
        except Exception as e:
            assert str(e) == "Error listing files in folder: Mock error"


class TestGetFileInFolder:
    def test_get_file_in_folder(self, mocker):
        # Mock the s3.head_object function to return a mock response
        mock_response = {
            "Metadata": {
                "mock-key": "mock-value"
            }
        }
        mocker.patch('mechanics.storage.s3.head_object', return_value=mock_response)

        # call the function 
        result = get_file_in_folder("mock-file")
        assert f"s3.amazonaws.com/pdf_files/mock-file.pdf" in result["file_url"]

    def test_get_file_in_folder_error_handling(self, mocker):
        # Mock the s3.head_object function to raise an exception
        mocker.patch('mechanics.storage.s3.head_object', side_effect=Exception("Mock error"))

        # call the function 
        try:
            get_file_in_folder("mock-file")
        except Exception as e:
            assert str(e) == "File not found"


class TestDownloadFile:
    def test_download_file(self, mocker):
        # Mock the s3.download_file function to return a mock response
        mock_response = {}
        mocker.patch('mechanics.storage.s3.download_file', return_value=mock_response)

        # call the function 
        result = download_file("mock-file")
        assert result == "/tmp/mock-file"

    def test_download_file_error_handling(self, mocker):
        # Mock the s3.download_file function to raise an exception
        mocker.patch('mechanics.storage.s3.download_file', side_effect=Exception("Mock error"))

        # call the function 
        try:
            download_file("mock-file")
        except Exception as e:
            assert str(e) == "Error downloading file: Mock error"