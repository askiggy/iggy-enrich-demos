# iggy-metaflow-demo

This repo contains code for a simple demo of using Iggy feature enrichment
for the task of predicting real estate sales prices in Pinellas County, FL.

**Related blog post:** [tbd]

## Getting started

- Un-compress the benchmark dataset in `./data/benchmark`:
  ```sh
  tar -xvf data/benchmark/iggy_re_salesprice_pinellas_20211203.tar.gz -C data/benchmark/
  ```

- [Request Iggy sample data](https://docs.askiggy.com/download/sample-data) if you haven't already. Once downloaded, you have two options to use it within your work:
  - Option 1: Place it in `../iggy-data` and un-compress it:
  ```
  tar -xzvf ../iggy-data/iggy-package-wkt-20211110214810_fl_pinellas_quadkeys.tar.gz -C ../iggy-data
  ```
  - Option 2: Place it (un-compressed) in an S3 bucket and replace the path denoted by `IGGY_DATA_BASE_LOCATION` in line 7 of `iggy_metaflow_base.py` with your S3 path (e.g. `s3://bucket/path/to/data/`)
  

- From the root directory of the repo, set up virtual environment and install dependencies, e.g.:
  ```sh
  python3 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
  ```

- Run the demo with Metaflow (requires a `S3` datastore) : 
  ```sh
  # For baseline 
  python iggy_baseline_flow.py run
  # For Iggy Enriched data 
  python iggy_enrich_flow.py run 
  # For Running Per District parallelized model training. 
  python iggy_perdistrict_flow.py run 
  ```

- Accessing results (feature importances) after running with `metaflow`
  ```python
  # For Baseline Model
  from metaflow import Flow
  results = Flow('IggyBaselineFlow').latest_run.data.results

  # For Enriched Model  
  from metaflow import Flow
  results = Flow('IggyEnrichFlow').latest_run.data.results

  # For Per-District Model 
  from metaflow import Flow
  results = Flow('IggyPerDistrictFlow').latest_run.data.results
  ```

## What's in the demo

The demo here follows our related blog post.

- `IggyBaselineFlow`: Run the baseline (load benchmark data, feature selection, model training and eval)
- `IggyEnrichFlow`: Run the iggy-enriched model (load benchmark data, iggy enrich, feature selection, model training and eval)
- `IggyPerDistrictFlow`: Run an iggy-enriched model for each tax zone in Pinellas (load benchmark data, iggy enrich, segment by tax district, feature selection, model training and eval)

## Results in current demo

| Iteration | Val MAE (scaled) | Test MAE (scaled) | Test MAE (unscaled) |
| --- | --- | --- | --- |
| 1 (Baseline) | 0.798 | 0.744 | 0.104 |
| 2 (Enriched) | 0.744 | 0.711 | 0.100 |
| 3 (District-Specific Enriched): CLEARWATER | 0.849 | 0.522 | 0.097 |
| 3 (District-Specific Enriched): DUNEDIN | 0.442 | 0.590 | 0.088 |
| 3 (District-Specific Enriched): LARGO | 0.753 | 0.666 | 0.096 |
| 3 (District-Specific Enriched): PALM HARBOR COM SVC | 0.682 | 0.518 | 0.078 |
| 3 (District-Specific Enriched): SEMINOLE FIRE | 0.473 | 0.948 | 0.099 |
| 3 (District-Specific Enriched): ST PETERSBURG | 0.914 | 0.958 | 0.116 |

Can you do better? If so, write or tweet about it and tag us ([@askiggyapp](https://twitter.com/askiggyapp)) or link to our repo!