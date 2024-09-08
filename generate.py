from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

with open("chantiers.json", "r") as chantiers_file:
  chantiers = json.load(chantiers_file)

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)

template = env.get_template("index.html.jinja")

print(template.render(chantiers=chantiers))
