"""Build static HTML site from directory of HTML templates and plain files."""
import os
import click
import pathlib
import json
import jinja2
import shutil
from jinja2 import TemplateSyntaxError

def read_config(input_dir):
    # read the config file
    input_dir = pathlib.Path(input_dir)
    config_path = os.path.join(input_dir, "config.json")
    config_filename = pathlib.Path(config_path)
    try:
        with config_filename.open() as config_file: 
            config_objects = json.load(config_file)
        return config_objects[0]
    except FileNotFoundError:
        click.echo(f"Error: {config_file} not found")
        return None
    except json.JSONDecodeError as e:
        click.echo(f"Error: {config_file}")
        click.echo(f"Expecting value: line {e.lineno} column {e.colno} (char {e.pos})")
        return None

def fill_template(input_dir, config_objects):
    template_dir = os.path.join(input_dir, "templates")
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    try:
        template = template_env.get_template("index.html")
        output_file = template.render(words=config_objects['context']['words'])
        return output_file
    except TemplateSyntaxError as e:
        click.echo(f"Error: {e} ")
        click.echo(f"Unexpected end of template. Jinja was looking for the following tags: 'endfor' or 'else'. The innermost block that needs to be closed is 'for'.")
        return None
    
def write_output(output_dir, config_objects, rendered_template, verbose):
    if os.path.exists(output_dir):
        click.echo(f"Error: {output_dir} already exists")
        return None
    else:
        os.makedirs(output_dir)
        url = pathlib.Path(config_objects['url'].lstrip("/"))
        output_path = pathlib.Path(output_dir/url/"index.html")
        with open(output_path, 'w') as f:
            f.write(rendered_template)
        # verbose option
        if verbose:
            click.echo(f"Rendered index.html -> {output_path}")
'''       
def copy_dir(input_dir, output, verbose):
    # copy directory
    dst_dir = output
    src_dir = os.path.join(input_dir, "static")
    isExist = os.path.exists(src_dir)
    if isExist:
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
        # verbose option
        if verbose:
            click.echo(f"Copied {src_dir} -> {dst_dir}")
'''                

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help="Output directory.")
@click.option('--verbose', '-v', is_flag=True, help="Print more output.")

def main(input_dir, output, verbose):
    input_dir = pathlib.Path(input_dir)
    config_objects = read_config(input_dir)
    if config_objects is None:
        return
    rendered_template = fill_template(input_dir, config_objects)
    if rendered_template is None:
        return
    
    # non --output option -> use default
    if output is None:
        output = pathlib.Path(input_dir/"html")   
    write_output(output, config_objects, rendered_template, verbose)

    
    # copy directory
    dst_dir = output
    src_dir = os.path.join(input_dir, "static")
    isExist = os.path.exists(src_dir)
    if isExist:
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
        # verbose option
        if verbose:
            click.echo(f"Copied {src_dir} -> {dst_dir}")

'''
def main(input_dir, output, verbose):
    # read the config file
    input_dir = pathlib.Path(input_dir)
    config_path = os.path.join(input_dir, "config.json")
    config_filename = pathlib.Path(config_path)
    with config_filename.open() as config_file: 
        config_objects = json.load(config_file)
    # parse json objects
    json_objects = config_objects[0]
    
    # read template file
    template_dir = os.path.join(input_dir, "templates")
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    template = template_env.get_template("index.html")
    output_file = template.render(words=json_objects['context']['words'])
    
    # update output option
    url = pathlib.Path(json_objects['url'].lstrip("/"))
    # not using '--output'
    if not output:
        output = pathlib.Path(input_dir/"html") # default, can be changed with --output option
    output_path = pathlib.Path(output/url/"index.html")

    # write output (add err msg)
    isExist = os.path.exists(output_path)
    if not isExist:
        os.makedirs(output)
        f = open(output_path, "w")
        f.write(output_file)
        f.close()

    # copy directory
    dst_dir = output
    src_dir = os.path.join(input_dir, "static")
    isExist = os.path.exists(src_dir)
    if isExist:
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
    
    # verbose option
    if verbose:
        if isExist:
            print(f"Copied {src_dir} -> {output}")
        print(f"Rendered index.html -> {output_path}")
'''

if __name__ == "__main__":
    main()



