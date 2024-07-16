## Getting Started
Install Anaconda and launch the terminal

```
git clone git@github.com:MoCoMakers/coiled-demo.git
cd coiled-demo
python -m venv venv
# Activate the virtual environment
.\venv\Scripts\activate

pip install -r requirements.txt
```

Setup up Google Cloud account and the gcloud CLI - https://cloud.google.com/sdk/docs/install

Follow steps from coiled to set up your system to work with coiled servers for cloud management. Try the automatic setup, but if there are issues do the Manual Setup instead - [https://docs.coiled.io/user_guide/setup/gcp/manual.html](https://docs.coiled.io/user_guide/setup/gcp/manual.html)

Test that things are working with the first script:

```
python 1-script.py
```
Be sure to log into [coiled.io](https://coiled.io) to monitor your dashboard, and make sure that all clusters are shutting down. Always use the `cluster.close()` command to ensure you don't have problems with ongoing billing.

## Next Steps

```
python 2-script.py
```

Note that the `jupyter notebook 2-script.ipynb` version of the code is not yet working at the cluster creation step.