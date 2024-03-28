#!/usr/bin/env python3

import sys
import subprocess
import yaml
import os
import configparser
import io

codex_dir = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(f'{codex_dir}/config.ini')

man="""\
┌─ man
│ codex build               - build codex.html using default path
│ codex build <dir>         - build codex.html using <dir> path
│
│ codex set-default <dir>   - use <dir> as default path
│
│ codex cleanup             - auto remove unecessary files from clone (README.md,...) and remove .git/
│ codex man                 - print this
└─"""


def generate(obj,path):
    images_path = f"{path}/images"
    res="<section>\n"
    for key in [k for k in obj.keys() if not isinstance(obj[k], dict)]:
        img = f"<img src='./images/{key}.png'>" if os.path.exists(f"{images_path}/{key}.png") else ""
        res += f"<button data-url='{obj[key]}'>{img}{key}</button>\n"
        del obj[key]
    res+="</section>\n"

    for key in [k for k in obj.keys() if isinstance(obj[k], dict)]:
        img = f"<img src='./images/{key}.png'>" if os.path.exists(f"{images_path}/{key}.png") else ""
        res += f"""<div class='folded'><h2>{img}{key}</h2>{generate(obj[key],path)}</div>"""
    return res

def build(path):
    build_path=path
    with open(f'{path}/codex.yaml', 'r') as file:
        yml=yaml.safe_load(file)

    subprocess.run(f"mkdir {build_path}",shell=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(f"mkdir {build_path}/rsc/",shell=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    html=f"<body><h1>{yml['TITLE'] if 'TITLE' in yml.keys() != '' else 'Codex'}</h1><main>"
    html+=generate(yml['LINKS'],path)
    subprocess.run(f'cat "{codex_dir}/rsc/base.html" > {build_path}/codex.html',shell=True)
    with open(f'{build_path}/codex.html', 'a') as file:
        file.write(html)

    subprocess.run(f"echo '</main></body></html>' >> {build_path}/codex.html",shell=True)
    subprocess.run(f"cp {codex_dir}/rsc/script.js {build_path}/rsc/",shell=True)
    subprocess.run(f"cp {codex_dir}/rsc/fav.ico {build_path}/rsc/",shell=True)
    subprocess.run(f"cp {codex_dir}/rsc/style.css {build_path}/rsc/",shell=True)
    print('built')

args=sys.argv
if len(args) < 2:
    print('too few arguments, need to specify an action')
    print(man)
    exit()

match args[1]:
    case 'set-default':
        if len(args) >= 3:
            abs_path = os.path.abspath(args[2])
            config['GENERAL']['default'] = abs_path
            with open(f'{codex_dir}/config.ini', 'w') as configfile:
                config.write(configfile)
            print(f'default codex dir set to {abs_path}')
        else:
            print('too few arguments')
            print(man)

    case 'build':
        if len(args) >= 3:
            build(args[2])
        else:
            default=config['GENERAL']['default']
            if default == '':
                print('no default dir set-up\n> codex set-defaut <dir>  (set-up defaut codex dir)\n> codex build <dir>       (build specific dir)\n')
                exit()
            build(default)

    case 'cleanup':
        subprocess.run(f"rm {codex_dir}/LICENSE", shell=True)
        subprocess.run(f"rm {codex_dir}/README.md", shell=True)
        subprocess.run(f"rm {codex_dir}/rsc/doc.png", shell=True)
        subprocess.run(f"rm {codex_dir}/new_page_browser.md", shell=True)
        subprocess.run(f'rm -r -f {codex_dir}/.git', shell=True)

    case 'man':
        print(man)
    case _:
        print('wrong command')
        print(man)
