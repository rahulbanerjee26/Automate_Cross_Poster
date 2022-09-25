from distutils.command.build_scripts import first_line_re
import markdown
import re
import requests
import json

embedGist = {
    "devto": lambda gist: f"{{% embed {gist} %}}",
    "medium": lambda gist: gist,
    "hashnode": lambda gist: f"%[{gist}]",
    "wp": lambda gist: f"[gist {gist}]",
}


def getSnippetName(language, snippet):
    mapLanguagetoFileName = {
        "python": "__init__.py",
        "javascript": "index.js",
        "typescript": "index.ts",
    }
    lines = snippet.split("\n")
    firstLine = lines[0]
    if "#" in firstLine:
        return (firstLine.strip("#").strip("\n"), "\n".join(lines[1:]))
    elif "//" in firstLine:
        return (firstLine.strip("//").strip("\n"), "\n".join(lines[1:]))
    else:
        return (mapLanguagetoFileName.get(language, "newlanguage"), snippet)


def markDownToHtml(markDownContent):
    html = markdown.markdown(markDownContent, extensions=["fenced_code"])
    return html


def getCodeSnippetsFromMarkdown(content):
    start_pat = "```(.*?)\n"
    end_pat = "```"
    snippets = re.findall(start_pat + "(.*?)" + end_pat, content, re.S)
    result = []
    for item in snippets:
        if item[0] != "bash":
            result.append(getSnippetName(item[0], item[1]))
    return result


def createGists(token, snippets, public=False):
    query_url = "https://api.github.com/gists"
    headers = {"Authorization": f"token {token}"}
    urls = []
    for fileName, code in snippets:
        data = {"public": public, "files": {fileName: {"content": code}}}
        # Send the request
        response = requests.post(query_url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            urls.append(response.json()["html_url"])
    return urls


def replaceCodeSnippetsWithGists(
    content, gists, title, hashnode=False, devto=False, medium=False, wp=False
):
    start_pat = "```(.*?)\n"
    end_pat = "```"

    def replaceCode(blg):
        new_content = content
        snippets = re.findall(start_pat + "(.*?)" + end_pat, new_content, re.S)
        counter = 0
        for item in snippets:
            if item[0] != "bash":
                new_content = new_content.replace(
                    "\n".join([f"```{item[0]}", f"{item[1]}```"]),
                    embedGist[blg](gists[counter]),
                )
                counter += 1
        newFileName = f"{blg}_gist"
        with open(newFileName, "w+") as f:
            f.write(new_content)
            print("Saved file with gists for ", blg)
        return new_content

    result = {}

    if hashnode:
        result["hashnode"] = replaceCode("hashnode")

    if devto:
        result["devto"] = replaceCode("devto")

    if medium:
        result["medium"] = replaceCode("medium")

    if wp:
        result["wp"] = replaceCode("wp")
    
    return result
