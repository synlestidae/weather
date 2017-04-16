class WeatherConfig:
    def __init__(self):
        self.debug = False;
        self.db_path = "./database.db"

def get_config():
    return WeatherConfig()
