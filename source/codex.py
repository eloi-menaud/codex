from mdX import mdX
import os
import re
from config import config
import markdown



# funciton to generate an header with script, css ... from the config
def generate_head():
    head = f'<meta charset="UTF-8">\n<meta http-equiv="X-UA-Compatible" content="IE=edge">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>{config["doc_title"]}</title>\n'
    for css in config['css']:
        head += f"<link rel='stylesheet' href='../../../rsc/{css}'>\n"
    for script in config['local_script']:
        head += f'<script src="../../../rsc/{script}"></script>'
    for script in config['script']:
        head += f'<script src="{script}"></script>'
    return "<head>\n" + head + "\n</head>"
head = generate_head()


def wrap(src:str,tag:str):
    return f"<{tag}>\n{src}\n</{tag}>"


# sort file path regarding x- prefix
# theoretically, it is just a classic alphanumeric sort, but I have implemented more complex functions to make it easily customizable.
def sort_path(page):
    section, category, md_name =  page.replace('./mds/','').split('/')
    r = 0
    nb_section=re.findall('^(.*?)-',section)
    if (nb_section != []) and (nb_section != ['']):
        r += int(nb_section[0])*200_000

    nb_category=re.findall('^(.*?)-',category)
    if (nb_category != []) and (nb_category != ['']):
        r += int(nb_category[0])*200

    nb_md_name=re.findall('^(.*?)-',md_name)
    if (nb_md_name != []) and (nb_md_name != ['']):
        r += int(nb_md_name[0])
    return r



# remove the X- from resource name like 10-page_name.md
def rm_prefix_number(word):
    return re.sub('^[0-9]+-','',word)

class Page:
    def __init__(self,md_path):
        self.md_path = md_path
        self.section, self.category, self.md_name =  self.md_path.replace('./mds/','').split('/')
        self.display_name = rm_prefix_number(self.md_name.replace('.md',''))
        self.html_name = self.md_name.replace('.md','.html')
        self.relative_path_to_html_file = f"../../../pages/{self.section}/{self.category}/{self.html_name}"
        
    # create the <a> tag to redirect to this page, for placing it into the navbar
    # class_active is used to create a visual marker in the navbar to show the current page 
    def get_nav(self,active=False):
        class_active = ""
        if active:
            class_active = " class='active'"          
        return f"<a{class_active} href='{self.relative_path_to_html_file}'>{self.display_name}</a>\n"
    
    def generate(self,select,nav):
        md = '' # final page string
        with open(self.md_path,'r') as md_file:
            md = md_file.read()
        
        md = mdX(md) # apply all transformation
        md = markdown.markdown(md) # fix markdown to html
        md = f"<h1 class='title'>{self.display_name}</h1>" + md # Add page title
        md = wrap(md,'article') # <article>{titre}{content}<article>
        md = nav + md # adding the nav on the side -> <nav>...</nav><article>...<article>

        #changing the default non-active <a> in the nav by the active one
        md = md.replace(self.get_nav(),self.get_nav(True))
        md = wrap(md,'main') # <main><nav>...</nav><article>...<article></main>

        # add 'selected' attibut to the option corresponding to the current section 
        select = select.replace(f">{rm_prefix_number(self.section)}</option>",f"selected>{rm_prefix_number(self.section)}</option>")

        # Really otptional, just a script to dynamicly fit the select len to the section name
        select += """
        <script defer>
            select = document.querySelector("select")
            window.addEventListener("load", ()=>{console.log('hehe'); select.style.width = select.options[select.selectedIndex].text.length * 13 + 20 + 'px'}); 
        </script>""" #resize the width depending on content
        header = f"<header>\n{select}</header>\n" # 
        md = header + md # <header>...</header><main>...</main>
        md = wrap(md,'body') # <body><header>...</header><main>...</main></body>
        md = head + md # add html head <heade></heade><body>...</body>

        # create dir if not exist and create page
        os.makedirs("pages/" + self.section+"/"+self.category , exist_ok=True) 
        with open( "pages/" + self.section+"/"+self.category+"/" + self.html_name ,'w') as html_file:
            html_file.write(md)





#get all the pages wit 3 deep
all_md_pages = os.popen(f"find ./mds -mindepth 3 -maxdepth 3 -name '*.md'").read().split('\n')[:-1]
all_md_pages = sorted(all_md_pages, key=sort_path)

pages = []
tree = {}
all_sections = [] #

# Create Page object
# + create a dict with the navbar for a specific section AND remember the default page (first page) of a section to redirect to
for md_path in all_md_pages:
    page = Page(md_path)
    pages.append(page)
    section = page.section
    if not(section in all_sections):
        all_sections.append(section)
    if not(section in tree):
        tree[section] = {
            "first_page": page.relative_path_to_html_file,
            'categories':[],
            'nav':''
            }
    if page.category not in tree[section]['categories']:
        tree[section]['categories'].append(page.category)
        tree[section]['nav'] += f"<p>{rm_prefix_number(page.category)}</p>\n"
    tree[section]['nav'] += page.get_nav()


# creating the <select> with all sections
select = "<select onchange='window.location.href = this.value'>\n"
select += f"<option value='../../../index.html'>home</option>\n"
for section in all_sections:
    select += f"<option value='{tree[section]['first_page']}'>{rm_prefix_number(section)}</option>\n"
select += "</select>\n"


# generate .html pages from Page objec previously create
for page in pages:
    nav = "<nav>" + tree[page.section]['nav'] + "</nav>"
    page.generate(select,nav)
    print(f"{page.section}/{page.category}/{page.display_name}  ✓")

# generate home.html page 
home = f"""
{generate_head()}
<body id='home'>
<header>{select}</header>
<main>
<h1 class='title'>{config['doc_title']}</h1>
<p>made with <a href='https://github.com/eloi-menaud/codex'>codex</a><img src='rsc/img/logoCodex.svg'></p>
</main>
</body>
""".replace('../../../','')


with open('index.html' ,'w') as html_file:
    html_file.write(home)


