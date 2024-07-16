
# Inpsired by - https://github.com/mrocklin/arxiv-matplotlib
# Released with BSD-3-Clause license - https://opensource.org/license/bsd-3-clause'

from google.cloud import storage
import coiled

# set key credentials file path
# import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:\\Users\\\USERNAME_GOES_HERE\\AppData\\Roaming\\gcloud\\application_default_credentials.json'

# define function that list files in the bucket
def list_cs_files(bucket_name, path, limit=1000): 
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    print("Bucket is: "+str(bucket))

    blobs = bucket.list_blobs(prefix=path, max_results=limit)

    file_list = [file.name for file in blobs]

    return file_list

# Path - 'gs://arxiv-dataset/arxiv/' -  gs://<bucket_name>/<file_path_inside_bucket>.

file_list = list_cs_files('arxiv-dataset', 'arxiv', limit=1000)
pdf_files = [filename for filename in file_list if filename.endswith(".pdf")]
print(pdf_files[:10])
print("Length of PDF List: "+str(len(pdf_files)))


def extract(file_set):
    """ Extract and process one directory of arXiv data
    
    Returns
    -------
    filename: str
    contains_matplotlib: boolean
    """
    out = []
    
    # Create a connection per file_set
    storage_client = storage.Client()
    bucket = storage_client.bucket('arxiv-dataset')

    for filename in file_set:

        """Read the content of a PDF file from Google Cloud Storage."""
        # client = storage.Client()
        # bucket = client.bucket(bucket_name)
        blob = bucket.blob(filename)

        try:
            # Download the PDF content as bytes
            pdf_bytes = blob.download_as_bytes()
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
        
        out.append((
            filename, 
            b"matplotlib" in pdf_bytes.lower()
        ))

    return out

out = extract(pdf_files[0:10])
print(out)

############

chunk_size = 10
chunked_list = [pdf_files[i:i + chunk_size] for i in range(0, len(pdf_files), chunk_size)]
print(chunked_list[0])
print("Number of chunks: "+str(len(chunked_list)))

############

cluster = coiled.Cluster(
    n_workers=5,
    name="arxiv",
    package_sync=True, 
    backend_options={"region": "us-east1"},  # faster and cheaper
)
# Start cluster. Billing starts.
#client = cluster.get_client()
from dask.distributed import Client, wait
client = Client(cluster)
############


futures = client.map(extract, chunked_list)
wait(futures)

# We had one error in one file.  Let's just ignore and move on.
good = [future for future in futures if future.status == "finished"]

lists = client.gather(good)

print(lists)
print("Closing cluster")
cluster.close()