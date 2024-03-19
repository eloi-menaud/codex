# codex : Linktree as code
Codex is a Linktree-like tool that allows you to build your own link organization, managing images, emojis, directories, etc..

**from a yaml conf :**
```yaml
LINKS:
  link 1: https://
  link 2: https://
  link 3: https://
  directory:
    ✨ keep emoji 👍: https://
    other link: https://
    sub directory:
      Youtube: https://
```
**to a html page :**

![](./rsc/doc.png)

---
<br><br><br>

# 🏁 Get started
### 0. prerequis
you must have
- Python3
- ConfigParser : `pip3 install ConfigParser`
- pyyaml : `pip3 install pyyaml`
### 1. Clone this repo
### 2. Codex as command
Edit and add this function in your shell configuration file, to enable `codex` as command
```
codex(){ python3 -B {path/to/codex}/codex.py $@; }
```
then `source` your shell configuration file or relunch a new terminal
### 3. Test
test by running :
```bash
codex man
```
<br>

# 🖼️ Images
For better organization and beauty, in addition to using emojis, it's possible to put images at the beginning of the link (button) or directory. To do this :

- Put an image named `<targeted yaml key>.png` in the `codex/images/` directory.

Ex : to put an image of the YouTube logo in front of the button named _YouTube_ (as the exemple in top of this file), simply name your image of the YouTube logo `Youtube.png` and put it under `/codex/images/Youtube.png`. it will automatically add the image in front of each element named `Youtube`.

---
<br><br><br>

# 📖 Doc
## Display man : `codex man`
## Edit yours links : `codex edit`
Use `codex edit` to open the `codex.yaml` file which contains your links structure.<br>
When exiting the edition, a build of `codex.html` is triggered.


## Change editor for 'edit' : `codex set-editor`
The default editor is `vi`, but you can change the editor by using `codex set-editor <editor>`, for example: `codex set-editor nvim`.
> /!\ With editors not integrated in the terminal (such as vscode), a manual build will be required after modifications have been made.


## Get the path of the built .html : `codex path`
so you don't have to remember where you cloned codex, especially to retrieve the .html file, you can use `codex path` to get the codex directory/path.

## Remove git link and unnecessary stuff : `codex cleanup`
to avoid having to keep the `.git/` and other files like the `README.md`... , you can do a `codex cleanup` to automatically clean up unnecessary files

## Build manually : `codex build`

