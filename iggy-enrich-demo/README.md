# iggy-enrich-demo

This repo contains code for a simple demo of using Iggy feature enrichment.
We will enrich some vacation rental data, explore it and then apply the dataset to two tasks:
- vacation rental recommendation
- vacation rental ratings prediction

## Getting started


- From the root directory of the demo, set up virtual environment and install dependencies, e.g.:
    ```sh
    python3 -m venv iggy-enrich-demo
    source iggy-enrich-demo/bin/activate
    pip install -r requirements.txt
    ```

- Add virtual environment to Jupyter:
    ```sh
    python -m ipykernel --user install --name=iggy-enrich-demo
    ```

- Install Jupyter extensions to aide Kepler visualizations:
    ```sh
    jupyter nbextension install --py --sys-prefix keplergl
    jupyter nbextension enable --py --sys-prefix keplergl
    ```

- Launch Jupyter Notebook and run demo notebook `iggy_enrich_demo.ipynb`
    ```sh
    jupyter notebook
    ```