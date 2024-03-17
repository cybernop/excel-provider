# Excel Provider

[![Tests](https://github.com/cybernop/excel-provider/actions/workflows/python-app-test.yml/badge.svg)](https://github.com/cybernop/excel-provider/actions/workflows/python-app-test.yml) [![Package](https://github.com/cybernop/excel-provider/actions/workflows/python-app-package.yml/badge.svg)](https://github.com/cybernop/excel-provider/actions/workflows/python-app-package.yml) [![PYPI](https://github.com/cybernop/excel-provider/actions/workflows/python-app-publish.yml/badge.svg)](https://github.com/cybernop/excel-provider/actions/workflows/python-app-publish.yml) [![Docker Image](https://github.com/cybernop/excel-provider/actions/workflows/docker-dev-image.yml/badge.svg)](https://github.com/cybernop/excel-provider/actions/workflows/docker-dev-image.yml) [![Docker Hub](https://github.com/cybernop/excel-provider/actions/workflows/docker-latest-image.yml/badge.svg)](https://github.com/cybernop/excel-provider/actions/workflows/docker-latest-image.yml)

## Usage

The configuration is done using a YAML file providing the following information

```yaml
server:
  host: "0.0.0.0"
  port: 5000
handler:
  excel_file: path/to/file.xlsx
  sheets:
    - "sheet 1"
    - "sheet 2"
  data_cols:
    - "column 1"
    - "column 2"
```

While `column 1` is the data column on `sheet 1` and `column 2` on `sheet 2`.

### Docker Image

Run a Docker image providing the providing backend, for example

```bash
docker run \
  -v /path/to/config:/app/config.yaml \
  -v /path/to/data.xlsx:/app/data.xlsx \
  -p 5000:5000 \
  cybernop/excel-provider
```

### Python Package

Start the server from the Python package providing the config

```bash
python -m excel_provider --config <config file>
```

## Tests

_pytest_ is used for unit tests. Run all tests from the project root.

```bash
pytest
```
