# CSV Change Report

Compare two CSV exports by a stable key. The JSON report lists added and removed records and individual changed cells.

## Run

From this folder with Python 3.9 or later:

```sh
python main.py before.csv after.csv id
```

Use headers `id,price` in both files. Changing `A,10` to `A,12` produces one change for column `price`. Keys must be unique. Column order and row order may differ.

## Limitations

The two files need matching columns and unique, nonblank record keys.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and test commands, and the [changelog](CHANGELOG.md) for project history.

## License

[MIT License](LICENSE). Copyright (c) 2026 csv-change-report contributors.
