from Project_public import create_app

app = create_app()
# if there is no "import", __name__ will be '__main__', if imported, __name__ will be 'app'
if __name__ == '__main__':

    app.run()
# port and ip in edit configurations: additional option: --host=x.x.x.x --port=xxxx. debug is also there,
# I don't know why I cannot edit it in run()
