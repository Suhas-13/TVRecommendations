from main import app

if __name__ == "__main__":
    app.config["APPLICATION_ROOT"] = "/api"
    app.run()
