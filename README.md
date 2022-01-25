# iggy-enrich-demos

This repository hosts demos for using [Iggy](https://www.askiggy.com/) to enrich locations in datasets.

## Contents

- `iggy-metaflow-demo`: Using Iggy + [Metaflow](https://metaflow.org/) to enrich and explore a dataset of residential home sales, plus iterations on modeling flow
- `visualization`: Using Iggy + [kepler.gl](https://kepler.gl/) in a Jupyter notebook to visualize Iggy features

## Getting sample data

Running these demos locally requires you to have a copy of Iggy sample data. 

You can request Iggy sample data [here](https://docs.askiggy.com/download/sample-data). Once downloaded, place it in `./iggy-data` and un-compress it:
  ```
  tar -xzvf ./iggy-data/iggy-package-wkt-20211110214810_fl_pinellas_quadkeys.tar.gz -C ./iggy-data
  ```

## Related Links

- [Iggy Data Readme](https://docs.askiggy.com/reference/place-data)
- [Python `iggyenrich` package](https://pypi.org/project/iggyenrich/)
