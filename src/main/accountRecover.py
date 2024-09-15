from __main__ import app

from flask import Response

@app.route('/account/recover', methods = ['GET'])
def accountRecover():
    return Response("Building")
