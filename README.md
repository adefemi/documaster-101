# Documaster

Documaster is a simple Python-based platform that lets you upload your PDF files, then you can ask questions on the PDF documents

### Prerequisities

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/).

### Setup and Installation

1. Clone the repository
   
   ```
   git clone https://github.com/adefemi/documaster-101.git
   cd documaster-101
   ```

2. Rename the `.env_local` file to `.env` and update the environment variables as necessary:
   
   ```
   mv .env_local .env
   nano .env  # or open .env in your preferred text editor
   ```

3. Build the Docker image for the app:
   
   ```
   docker-compose build
   ```

4. Start the app using Docker Compose:
   
   ```
   docker-compose up
   ```

### Usage

Once the app is running, test [http://localhost:9001](http://localhost:9001) on your preferred API tester, I'll recommend [Postman](https://www.postman.com/).

### Endpoints
- Upload File:
    - Endpoint: `/upload`
    - Method: `POST`
    - Description: Upload a PDF file.
    - Form Data:
        - file: The PDF file you want to upload.

- List Files:
    - Endpoint: `/list`
    - Method: `GET`
    - Description: Retrieve a list of uploaded files.
  
- Inquire:
    - Endpoint: `/inquire`
    - Method: `POST`
    - Description: Submit a question and optionally specify document IDs to use for answering the question.
    - Request Body:
        - `question`: The question you want answered.
        - `doc_ids`: (Optional) A list of document IDs to use for answering the question. *NB* this just the docs name, the extension is not needed.

