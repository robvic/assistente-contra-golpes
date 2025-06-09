import functions_framework
import logging
import PyPDF2
import io
from google.cloud import storage
from google import genai

logging.basicConfig(level=logging.INFO)

PROJECT = "ia-contra-golpes"
STAGING_BUCKET = "base-golpes-sumarizado"
storage_client = storage.Client()
vertex_client = genai.Client(vertexai=True, project=PROJECT, location="global")


@functions_framework.cloud_event
def process(cloud_event):
    data = cloud_event.data
    logging.info(f"Raw event is: {data}")
    bucket_name = data["bucket"]
    file_name = data["name"]
    logging.info(f"Arquivo {file_name} recebido pelo bucket {bucket_name}.")

    bucket = storage_client.bucket(bucket_name)

    if ".pdf" in file_name:
        logging.info(f"O arquivo é um PDF.")
        blob = bucket.blob(file_name)
        file = blob.download_as_bytes()
        content = extract_pdf(io.BytesIO(file))
        file_name_destination = file_name.replace(".pdf", ".txt")
    elif ".txt" in file_name:
        logging.info(f"O arquivo é um texto simples.")
        blob = bucket.blob(file_name)
        content = blob.download_as_text()
        file_name_destination = file_name
    else:
        logging.info(f"O arquivo não é compatível.")
        return "", 200

    logging.info(f"Arquivo {file_name} lido.")

    summary = summarize(content)
    logging.info(f"Sumário executado.")

    copy(summary, file_name_destination)
    logging.info(f"Cópia para {STAGING_BUCKET} realizada.")

    return "", 200


def extract_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)

    content = ""
    for n in range(pdf_reader.numPages):
        page = pdf_reader.getPage(n - 1)
        text = page.extract_text()
        content = content + text

    return content


def summarize(content):
    model = "gemini-2.5-flash-preview-05-20"
    contents = (
        "Faça um resumo em bullet points do conteúdo do texto a seguir, mantenha em cada bullet o detalhamento dos golpes: "
        + content
    )
    response = vertex_client.models.generate_content(model=model, contents=contents)
    return response


def copy(content, file_name):
    bucket = storage_client.bucket(STAGING_BUCKET)
    blob = bucket.blob(file_name)
    blob.upload_from_string(content, content_type="text/plain")
    logging.info(f"Arquivo {file_name} criado no bucket {STAGING_BUCKET}.")
