from os import environ
from project import create_app


app = create_app()

if __name__ == "__main__":
    HOST = environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(environ.get("SERVER_HOST", "5555"))
    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)
