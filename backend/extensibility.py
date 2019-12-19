HTML_INIT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>showRoom</title>
</head>
<body>\n
"""

HTML_FINAL ="""
</body>
</html>
"""

def jsontoHTML(json, h=1):
    html = ""
    if isinstance(json, dict):
        for key in json.keys():
            html += "\t<h{}>{}: {} </h{}>\n".format(h, key, jsontoHTML(json[key], h+1), h)
    
    elif isinstance(json, list):
        if len(json) != 0:
            html += "<ul>"
            for item in json:
                html += "<li> {} </li>".format(jsontoHTML(item, h+1))
            html += "</ul>"
        else: 
            html = "empty"
    
    else:
        html = str(json)
    
    return html

def makeHTML(namefile, strHTML):
    with open("templates/{}.html".format(namefile), "w", encoding="utf-8") as f:
        f.write(HTML_INIT + strHTML + HTML_FINAL)
    return namefile+".html"
