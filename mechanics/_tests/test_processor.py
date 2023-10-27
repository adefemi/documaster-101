from mock import MagicMock
from mechanics.processor import extract_text_from_pdf, ans_question_from_text

class TestExtractTextFromPdf:
    def test_extract_text_from_pdf(self, mocker):
        text_content = "mock text"

        # Mock the fitz.open function to return a mock document
        page_moc = MagicMock(get_text=MagicMock(return_value=text_content))
        mock_doc = MagicMock(
            close=MagicMock(),
            __iter__=MagicMock(return_value=iter([page_moc]))
        )
        mocker.patch('fitz.open', return_value=mock_doc)

        # Mock the os.remove function to prevent it from actually deleting any files
        mocker.patch('os.remove', return_value=None)

        # call the function 
        result = extract_text_from_pdf('dummy.pdf')
        assert result == text_content
        page_moc.get_text.assert_called_once()

    def test_extract_text_from_pdf_error_handling(self, mocker):
        # Mock the fitz.open function to raise an exception
        mocker.patch('fitz.open', side_effect=Exception("Mock error"))

        # call the function 
        try:
            extract_text_from_pdf('dummy.pdf')
        except Exception as e:
            assert str(e) == "Error extracting text from PDF: Mock error"

class TestAnsQuestionFromText:
    def test_ans_question_from_text(self, mocker):
        text_content = "mock text"
        # Mock the openai.ChatCompletion.create function to return a mock response
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": text_content
                    }
                }
            ]
        }
        mocker.patch('openai.ChatCompletion.create', return_value=mock_response)

        # call the function 
        result = ans_question_from_text("mock text", "mock question")
        assert result == text_content

    def test_ans_question_from_text_error_handling(self, mocker):
        # Mock the openai.ChatCompletion.create function to raise an exception
        mocker.patch('openai.ChatCompletion.create', side_effect=Exception("Mock error"))

        # call the function 
        try:
            ans_question_from_text("mock text", "mock question")
        except Exception as e:
            assert str(e) == "Error chatting with OpenAI: Mock error"