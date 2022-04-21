# iggy-enrich-demos

This repository hosts demos for using [Iggy](https://www.askiggy.com/) to enrich locations in datasets.

## Contents
- `iggy-enrich-demo`: Using Iggy to enrich and explore a dataset of vacation rental homes
- `iggy-metaflow-demo`: Using Iggy + [Metaflow](https://metaflow.org/) to enrich and explore a dataset of residential home sales, plus iterations on modeling flow
- `visualization`: Using Iggy + [kepler.gl](https://kepler.gl/) in a Jupyter notebook to visualize Iggy features

## Getting sample data

Running these demos locally requires you to have a copy of Iggy sample data. 

For the `iggy-enrich-demo` the data download is included in the demo notebook.

For the `iggy-metaflow-demo` and the `visualization` demo you can request Iggy sample data [here](https://docs.askiggy.com/download/sample-data). Once downloaded, place it in `./iggy-data` and un-compress it:
  ```
  tar -xzvf ./iggy-data/iggy-package-wkt-20211110214810_fl_pinellas_quadkeys.tar.gz -C ./iggy-data
  ```

## Kepler

For the demo visualizations, when using Kepler in a Jupiter notebook running on a conda virtual environment you will need to enable a notebook extension per [this issue](https://github.com/keplergl/kepler.gl/issues/583)

- Install Jupyter extensions to aide Kepler visualizations:
    ```sh
    jupyter nbextension install --py --sys-prefix keplergl
    jupyter nbextension enable --py --sys-prefix keplergl
    ```

## Related Links

- [Iggy Data Readme](https://docs.askiggy.com/reference/place-data)
- [Python `iggyenrich` package](https://pypi.org/project/iggyenrich/)
