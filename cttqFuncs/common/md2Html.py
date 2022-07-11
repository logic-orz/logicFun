'''
Author: Logic
Date: 2022-06-06 09:51:04
LastEditTime: 2022-06-06 10:04:59
Description: 
'''
import sys
import markdown
import codecs
import os
import importlib
importlib.reload(sys)


def md2htmlFunc(mdStr: str):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
            'markdown.extensions.tables', 'markdown.extensions.toc']

    html = '''
    <html lang="zh-cn">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="github-markdown.css">
    <style>
        .markdown-body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }

</style>

    </head>
    <body>
    <article class="markdown-body">
    %s 
    </article>
    </body>
    </html>
    '''

    ret = markdown.markdown(mdStr, extensions=exts)
    return html % ret


def transfer(mdPath, htmlPath):
    infile = open(mdPath, 'r', encoding="utf8")
    md = infile.read()
    infile.close()

    if os.path.exists(htmlPath):
        os.remove(htmlPath)

    outfile = open(htmlPath, 'a', encoding="utf8")
    outfile.write(md2htmlFunc(md))
    outfile.close()
