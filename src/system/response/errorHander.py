from __main__ import app

from src.system.response.jsonMsg import returnJsonMsg

@app.errorhandler(405)
@app.errorhandler(500)
def errorHander_common(e):
    retcode = -1
    message = e.description
    content = "error"
    result = returnJsonMsg(retcode, message, content)
    return result


@app.after_request
def apply_global_info(response):
    GLOBAL_TITLE = "Hkrpg-SDK"
    response.headers['X-Custom-Header'] = GLOBAL_TITLE
    
    if response.content_type.startswith('text/html'):
        content = response.get_data(as_text=True)
        
        if '<title>' in content:
            content = content.replace('<title>', f'<title>{GLOBAL_TITLE} - ', 1)
        else:
            content = content.replace('<head>', f'<head><title>{GLOBAL_TITLE}</title>', 1)
        response.set_data(content)
    return response
