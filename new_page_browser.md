# set as default new pages
to use codex as the default page for your browser's new windows, follow the instructions below according to your browser:

## Firefox (only temporary extension load)
### 1
add a `manifest.json` in the `codex/` dir, past it this :
```json
{
  "manifest_version": 2,
  "name": "Codex",
  "version": "1.0",
  "description": "Codex as new tab page",
  "permissions": ["tabs"],
  "chrome_url_overrides": {
    "newtab": "codex.html"
  }
}
```
### 2
- got to `about:debugging#/runtime/this-firefox` on firefox
- click on `Load Temporary Add-on…`
- chose the `.../codex/manifest.json` that you created


## Chrome
### 1
add a `manifest.json` in the `codex/` dir, past it this :
```json
{
    "name": "Codex",
    "description": "Codex as new tab page",
    "version": "0.1",
    "incognito": "split",
    "chrome_url_overrides": {
      "newtab": "codex.html"
    },
    "manifest_version": 2
  }
```
### 2
- got to `chrome://extensions/` on firefox
- click on `Developer mode` toggle-switch
- click on `Load unpacked` button
- chose the `.../codex/` directory