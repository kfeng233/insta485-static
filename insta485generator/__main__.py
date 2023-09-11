"""Build static HTML site from directory of HTML templates and plain files."""
import os
import pathlib
import json
import shutil
import click
import jinja2
from jinja2 import TemplateSyntaxError


def read_config(input_dir):
    """Read and load config file, return JSON data."""
    input_dir = pathlib.Path(input_dir)
    config_path = os.path.join(input_dir, "config.json")
    config_filename = pathlib.Path(config_path)
    try:
        with config_filename.open(encoding="utf-8") as config_file:
            config_objects = json.load(config_file)
        return config_objects
    except FileNotFoundError:
        click.echo(f"Error: {config_file} not found")
        return None
    except json.JSONDecodeError as err:
        click.echo(f"Error: {config_file}")
        click.echo(f"Expecting value: line {err.lineno}\
        column {err.colno} (char {err.pos})")
        return None


def fill_template(input_dir, config_object, template):
    """Fill template with JSON data and return a rendered template."""
    template_dir = os.path.join(input_dir, "templates")
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    try:
        template = template_env.get_template(template)
        data = {}
        for elem in config_object['context']:
            data.update({elem: config_object['context'][elem]})
        rendered_template = template.render(data)
        return rendered_template
    except TemplateSyntaxError as err:
        click.echo(f"Error: {err} ")
        click.echo(f"Unexpected end of template. Jinja was looking \
        for the following tags: {'endfor'} or {'else'}. The \
        innermost block that needs to be closed is {'for'}.")
        return None


def write_output(output_dir, rendered_template, config_obj, verbose):
    """Write a output HTML file and copy static directory."""
    output_file = pathlib.Path(output_dir/"index.html")
    if os.path.exists(output_file):
        click.echo(f"Error: {output_file} already exists")
    else:
        os.makedirs(pathlib.Path(output_dir), exist_ok=True)
        try:
            with open(output_file, 'w', encoding="utf-8") as file:
                file.write(rendered_template)
            if verbose:
                click.echo(
                    f"Rendered {config_obj['template']} -> {output_file}")
        except FileNotFoundError:
            click.echo(f"Error: {output_dir} not found")


def copy_dir(input_dir, output, verbose):
    """Copy static directory to the input directory."""
    src_dir = os.path.join(input_dir, "static")
    try:
        shutil.copytree(src_dir, output, dirs_exist_ok=True)
        # verbose option
        if verbose:
            click.echo(f"Copied {src_dir} -> {output}")
    except FileNotFoundError:
        click.echo(f"Error: {src_dir} not found")


@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help="Output directory.")
@click.option('--verbose', '-v', is_flag=True, help="Print more output.")
def main(input_dir, output, verbose):
    """Templated static website generator."""
    input_dir = pathlib.Path(input_dir)
    config_objects = read_config(input_dir)
    if config_objects is None:
        return
    # non --output option -> use default
    if output is None:
        output = pathlib.Path(input_dir/"html")
    copy_dir(input_dir, output, verbose)
    for obj in config_objects:
        rendered_template = fill_template(input_dir, obj, obj['template'])
        if rendered_template is None:
            return
        url = pathlib.Path(obj['url'].lstrip("/"))
        output_dir = pathlib.Path(output/url)
        write_output(output_dir, rendered_template, obj, verbose)


if __name__ == "__main__":
    main()
