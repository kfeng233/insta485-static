"""Build static HTML site from directory of HTML templates and plain files."""
import os
import click
import pathlib
import json
import jinja2
import shutil

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help="Output directory.")
@click.option('--verbose', '-v', is_flag=True, help="Print more output.")

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

    # write output
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

    if verbose:
        if isExist:
            print(f"Copied {src_dir} -> {output}")
        print(f"Rendered index.html -> {output_path}")

if __name__ == "__main__":
    main()
