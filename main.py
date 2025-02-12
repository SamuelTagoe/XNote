from website import create_app

app = create_app()

if __name__ == '__main__':  # Only if this file runs, app.run()
    app.run(debug = True)     # debug=True which means the webserver should auto run anytime we make changes