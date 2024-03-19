#!/usr/bin/env python3

import sys
import subprocess
import yaml
import os
import configparser
import io
codex_dir = os.path.dirname(os.path.abspath(__file__))
images_path=f"{codex_dir}/images"
yaml_path=f"{codex_dir}/codex.yaml"
html_path=f"{codex_dir}/codex.html"

config = configparser.ConfigParser()
config.read('config.ini')

man="""\
┌─ man
│ codex edit                - edit codex.yaml then build codex.html
│ codex set-editor <editor> - use <editor> for 'codex edit'
│ codex cleanup             - auto remove unecessary files from clone (README.md,...) and remove .git/
│ codex path                - show codex file paths
│ codex build               - build codex.html
│ codex man                 - print this
└─"""

path=f"""\
{codex_dir}
├─ codex.html
├─ codex.yaml
└─ images/"""



def generate(obj):
    res="<section>\n"
    for key in [k for k in obj.keys() if not isinstance(obj[k], dict)]:
        img = f"<img src='./images/{key}.png'>" if os.path.exists(f"{images_path}/{key}.png") else ""
        res += f"<button onclick=\"event.stopPropagation();window.location.href='{obj[key]}';\">{img}{key}</button>\n"
        del obj[key]
    res+="</section>\n"

    for key in [k for k in obj.keys() if isinstance(obj[k], dict)]:
        img = f"<img src='./images/{key}.png'>" if os.path.exists(f"{images_path}/{key}.png") else ""
        res += f"""<div onclick="this.classList.toggle('folded');event.stopPropagation();" class='folded'><h2>{img}{key}</h2>{generate(obj[key])}</div>"""
    return res

def build():
    html=""
    with open(yaml_path, 'r') as file:
        html=generate(yaml.safe_load(file)['LINKS'])
    with open(f'{codex_dir}/tmp.html', 'w+') as file:
        file.write(html)
    subprocess.run(f'cat "{codex_dir}/rsc/template.html" > {html_path}',shell=True)
    subprocess.run(f"head -n -1 tmp.html >> {html_path}",shell=True)
    subprocess.run(f"echo '</main></body></html>' >> {html_path}",shell=True)
    subprocess.run(f"rm {codex_dir}/tmp.html",shell=True)
    print('codex built')


args=sys.argv
if len(args) < 2:
    print('too few arguments')
    print(man)
    exit()

match args[1]:
    case 'set-editor':
        if len(args) >= 3:
            config['GENERAL']['editor'] = args[2]
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print(f'editor set to {args[2]}')
        else:
            print('too few arguments')
            print(man)
    case 'edit':
        subprocess.run([config['GENERAL']['editor'], yaml_path])
        build()
    case 'build':
        build()
    case 'cleanup':
        for file in ['LICENSE','README.md', '.gitignore','rsc/doc.png']:
            try:
                subprocess.run(f"rm {codex_dir}/{file}", shell=True)
            except Exception as e:
                print(f"can't remove {codex_dir}/{file}")
                print(e)

        subprocess.run(f'rm -r -f {codex_dir}/.git', shell=True)
    case 'path':
        print(path)
    case 'man':
        print(man)
    case _:
        print('wrong command')
        print(man)
