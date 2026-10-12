import argparse

import uvicorn

from .app import create_app
from .runner import Runner


def main():
    parser = argparse.ArgumentParser(description='Quantic Studio local project API')
    parser.add_argument('--project-root', required=True)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--timeout', type=float, default=30)
    args = parser.parse_args()
    uvicorn.run(create_app(args.project_root, runner=Runner(args.timeout)), host='127.0.0.1', port=args.port)


if __name__ == '__main__':
    main()
