# CSV Change Report

Compare two CSV exports by a stable key. The JSON report lists added and removed records and individual changed cells.

## Run

From this folder with Python 3.9 or later:

```sh
python main.py before.csv after.csv id
```

Use headers `id,price` in both files. Changing `A,10` to `A,12` produces one change for column `price`. Keys must be unique. Column order and row order may differ.
