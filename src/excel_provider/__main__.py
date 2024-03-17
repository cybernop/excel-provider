import argparse
from pathlib import Path

import yaml

from .rest.api import create_app


def get_args():
    parser = argparse.ArgumentParser(description="Excel Provider")
    parser.add_argument(
        "--config", required=True, type=Path, help="Path to the config file"
    )
    return parser.parse_args()


args = get_args()

config = yaml.safe_load(args.config.read_text())

app = create_app(config)
app.run(**config.get("server", {}))
