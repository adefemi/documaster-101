from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestUploadEndpoint:
    def test_upload_endpoint_with_invalid_file_type(self, mocker):
        # Call the endpoint
        response = client.post("/upload", files={"file": ("filename.txt", "file content", "text/plain")})     
        assert response.status_code == 400
        assert response.json() == {"detail": "Only PDF files allowed"}
        
    def test_upload_endpoint_with_valid_file_type(self, mocker):
        # Mock the upload_file function to return a mock response
        mocker.patch('main.upload_file', return_value="mock-url")
        response = client.post("/upload", files={"file": ("test.pdf", "content", "application/pdf")})
        assert response.status_code == 200
        assert response.json()["url"] == "mock-url"

    def test_expection_in_process(self, mocker):
        # Mock the upload_file function to raise an exception
        mocker.patch('main.upload_file', side_effect=Exception("Mock error"))
        response = client.post("/upload", files={"file": ("test.pdf", "content", "application/pdf")})
        assert response.status_code == 500
        assert response.json() == {"detail": "Error uploading file"}

class TestListEndpoint:
    def test_list_endpoint(self, mocker):
        # Mock the list_files_in_folder function to return a mock response
        mocker.patch('main.list_files_in_folder', return_value=["mock-file-1", "mock-file-2"])
        response = client.get("/list")
        assert response.status_code == 200
        assert response.json() == {"files": ["mock-file-1", "mock-file-2"]}

    def test_expection_in_process(self, mocker):
        # Mock the list_files_in_folder function to raise an exception
        mocker.patch('main.list_files_in_folder', side_effect=Exception("Mock error"))
        response = client.get("/list")
        assert response.status_code == 500
        assert response.json() == {"detail": "Error getting files"}

class TestInquireEndpoint:
    def test_inquire_endpoint_with_empty_doc_ids(self, mocker):
        # Mock the list_files_in_folder 
        mocker.patch('main.list_files_in_folder', return_value=["mock-file-1", "mock-file-2"])

        # Mock download file
        mocker.patch('main.download_file', return_value="mock-file-path")

        # Mock extract text from pdf
        mocker.patch('main.extract_text_from_pdf', return_value="mock-text")

        # Mock the ans_question_from_text 
        mocker.patch('main.ans_question_from_text', return_value="mock-answer")
        response = client.post("/inquire", json={"question": "mock-question"})
        assert response.status_code == 200
        assert response.json() == {"answer": "mock-answer"}

    def test_inquire_endpoint_with_doc_ids(self, mocker):
        # Mock the get_file_in_folder
        mocker.patch('main.get_file_in_folder', return_value="mock-file")

        # Mock download file
        mocker.patch('main.download_file', return_value="mock-file-path")

        # Mock extract text from pdf
        mocker.patch('main.extract_text_from_pdf', return_value="mock-text")

        # Mock the ans_question_from_text 
        mocker.patch('main.ans_question_from_text', return_value="mock-answer")

        response = client.post("/inquire", json={"question": "mock-question", "doc_ids": ["mock-id"]})
        assert response.status_code == 200
        assert response.json() == {"answer": "mock-answer"}

    def test_inquire_endpoint_with_empty_doc_ids_and_no_files(self, mocker):
        # Mock the list_files_in_folder
        mocker.patch('main.list_files_in_folder', return_value=[])
        response = client.post("/inquire", json={"question": "mock-question"})
        assert response.status_code == 400
        assert response.json() == {"detail": "You need to upload at least one PDF file"}

    def test_inquire_endpoint_with_empty_doc_ids_and_error_getting_files(self, mocker):
        # Mock the list_files_in_folder function to raise an exception
        mocker.patch('main.list_files_in_folder', side_effect=Exception("Mock error"))
        response = client.post("/inquire", json={"question": "mock-question"})
        assert response.status_code == 500
        assert response.json() == {"detail": "Error getting files"}