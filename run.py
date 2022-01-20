import argparse
import datetime
import json
import os
import shutil
import subprocess


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--project',
        help='Name of the Hack project to create.',
        required=True,
    )
    parser.add_argument(
        '-a',
        '--author',
        help='Name of the project\'s author.',
        required=True,
        type=str,
    )
    parser.add_argument(
        '-e',
        '--email',
        help='Email of the project\'s author',
        required=True,
        type=str
    )
    return parser.parse_args()


def write_file(path, name, contents):
    with open('{}/{}'.format(path, name), mode='w') as f:
        f.write(contents)


def main():
    args = parse_args()

    path = '{}/../{}'.format(os.getcwd(), args.project)
    shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)

    composer_json = {
        "type": "library",
        "name": '{}/{}'.format(
            args.author.lower().replace(' ', '-'),
            args.project
        ),
        "author": {
            'name': args.author,
            'email': args.email
        },
        "license": [
            "MIT"
        ],
        "require": {},
        "require-dev": {
            "facebook/fbexpect": "^v2.8.0",
            "hhvm/hacktest": "^v2.2.3"
        },
        "autoload": {
            "classmap": [
                "src/"
            ]
        },
        "autoload-dev": {
            "classmap": [
                "tests/"
            ]
        }
    }
    write_file(path, 'composer.json', json.dumps(composer_json, indent=4))

    makefile = """\
.PHONY: build test hh_autoload format

build:
	docker build -t {project_name} .

install: build
	docker run -v `pwd`:/app -it {project_name} composer install

update: build
	docker run -v `pwd`:/app -it {project_name} composer update

hh_autoload:
	docker run -v `pwd`:/app -it {project_name} ./vendor/bin/hh-autoload

test:
	docker run -v `pwd`:/app -it {project_name} ./vendor/bin/hacktest tests

format:
	docker run -v `pwd`:/app -it {project_name} find {{src,tests}} -type f -name "*.hack" -exec hackfmt -i {{}} \;""".format(
        project_name=args.project 
    )
    write_file(path, 'Makefile', makefile)

    license = """\
MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""".format(
            author=args.author,
            year=datetime.datetime.now().year
        )
    write_file(path, 'LICENSE', license)

    subprocess.run(['cp', '-r', 'boilerplate/', path], check=True)

if __name__ == '__main__':
    main()
