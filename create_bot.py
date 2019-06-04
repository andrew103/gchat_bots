# Use this script to create new bots based off of `meta_skeleton`
import subprocess, os, sys

if len(sys.argv) != 2:
    print("Must specify a name for the new bot and no other parameters")
    sys.exit(1)

if sys.executable == "/usr/bin/python3":
    subprocess.call([sys.executable, "-m", "pip", "install", "--user", "virtualenv", "jinja2"])
else:
    print("This script must be run with Python3")
    sys.exit(1)

import virtualenv
from jinja2 import Environment, FileSystemLoader

# Create the bot folder and virtual environment
path = os.path.join(os.getcwd(), sys.argv[1])
os.mkdir(path)
venv_dir = os.path.join(path, "venv")
virtualenv.create_environment(venv_dir)

# Copy and render files from meta_skeleton
meta_path = os.path.join(os.getcwd(), "meta_skeleton")
env = Environment(loader=FileSystemLoader(meta_path))
files = env.list_templates()
for filename in files:
    template = env.get_template(filename)
    output = template.render(bot_name=sys.argv[1])

    with open(os.path.join(path, filename), "w") as fh:
        fh.write(output)

# Activate the virtual environment and install bot dependencies
os.system("source "+venv_dir+"/bin/activate && pip install -r "+path+"/requirements.txt")
