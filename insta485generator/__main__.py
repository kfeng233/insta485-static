"""Build static HTML site from directory of HTML templates and plain files."""
import os
import click
import pathlib
import json
import jinja2

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))

def main(input_dir):
    # read the config file
    input_dir = pathlib.Path(input_dir)
    abs_path = os.path.join(input_dir, "config.json")
    config_filename = pathlib.Path(abs_path)
    with config_filename.open() as config_file: 
        config_objects = json.load(config_file)
    # parse json objects
    for obj in config_objects:
        print(obj)
    '''
    # read template file
    template_env = jinja2.Environment(
        template_dir = os.path.join(input_dir, "templates")
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    '''

if __name__ == "__main__":
    main()
