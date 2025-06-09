import logging
from google.cloud.storage import Client, transfer_manager

logging.basicConfig(level=logging.INFO)
PROJECT = "ia-contra-golpes"
STAGING_BUCKET = "base-golpes-sumarizado"


def download_summaries():
    logging.info(f"Baixando conteúdo sumarizado...")
    storage_client = Client(project=PROJECT)
    bucket = storage_client.bucket(STAGING_BUCKET)

    blob_names = [blob.name for blob in bucket.list_blobs()]

    results = transfer_manager.download_many_to_path(
        bucket, blob_names, destination_directory="./data/downloaded"
    )

    for name, result in zip(blob_names, results):
        if isinstance(result, Exception):
            print("Falha no download {} pelo seguinte motivo: {}".format(name, result))
        else:
            print(
                "Feito download de {} para {}.".format(name, "data/downloaded/" + name)
            )


if __name__ == "__main__":
    download_summaries()
