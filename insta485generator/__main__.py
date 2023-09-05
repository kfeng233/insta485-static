"""Build static HTML site from directory of HTML templates and plain files."""
import os
import click
import pathlib
import json
import jinja2
import shutil

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
#@click.option("-o", "--output", type=click.Path(exists=True), help="Output directory.")
#@click.argument("input_dir" "output_dir", nargs=2, type=click.Path(exists=True))

def main(input_dir):
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
    output = template.render(words=json_objects['context']['words'])
    
    # write output
    path = os.path.join(input_dir, "html")
    filename = os.path.join(path, "index.html")
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        f = open(filename, "w")
        f.write(output)
        f.close()

    # copy directory
    dst_dir = path
    src_dir = os.path.join(input_dir, "static")
    if os.path.exists(src_dir):
        print(shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True))
    
if __name__ == "__main__":
    main()
