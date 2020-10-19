from app_web import app

if __name__ == "__main__":

    app.run(debug=True, host=app.config['IP_Server'], port=app.config['PORT_server'])
    # app.run(debug=False, ssl_context='adhoc', host=app.config['IP_Server'], port=app.config['PORT_server'])