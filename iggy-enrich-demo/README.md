# iggy-enrich-demo

This repo contains code for a simple demo of using Iggy feature enrichment.
We will enrich some vacation rental data, explore it and then apply the dataset to two tasks:
- vacation rental recommendation
- vacation rental ratings prediction

## Getting started


- From the root directory of the repo, set up virtual environment and install dependencies, e.g.:
    ```sh
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

- Add virtual environment to Jupyter:
    ```sh
    python -m ipykernel install --name=env
    ```

- Install Jupyter extensions to aide Kepler visualizations:
    ```sh
    jupyter nbextension install --py --sys-prefix keplergl
    jupyter nbextension enable --py --sys-prefix keplergl
    ```

- Launch Jupyter Notebook and run demo notebook `web_demo.ipynb`
    ```sh
    jupyter notebook
    ```