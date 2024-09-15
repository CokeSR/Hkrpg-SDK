from __main__                       import app
from flask                          import redirect, render_template_string, request
from src.system.logging.systemctl   import logger


@app.route('/', methods=['GET'])
def index():
    logger.info(f"Request:{request.url_rule}")
    return render_template_string("""
        <html>
        <head>
            <title>Home</title>
            <style>
                body {
                    background:#ffffff;
                }
                addresses a {
                    text-decoration: none;
                }
                addresses a:hover {
                    color: red;
                }
            </style>
        </head>
        <body>
            <span>Welcome to visit SDK for <font color="red">Hongkai: Star Rail</font> (ver 0.8.2 By CokeSR)</span>
            <br>
            <span>Please click link below to continue</span>
            <hr>
            <addresses>
                <a href="/account/register" target="_blank">|&nbsp;account register</a>&nbsp;|
                <a href="/account/recover" target="_blank">account recover</a>&nbsp;|
                <a href="https://blog.cokeserver.com/" target="_blank">author's blog</a>&nbsp;|
                <a href="https://gitlab.cokeserver.com/Coke/hkrpg-sdk" target="_blank">project address</a>&nbsp;|
            </addresses>
        </body>
        </html>
    """)


@app.route('/favicon.ico')
def favicon():
    logger.info(f"Request:{request.url_rule}")
    icon_url = "https://blog.cokeserver.com/upload/Blog_IconMain_20240129_640x640.ico"
    return redirect(icon_url)
