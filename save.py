import json


def save(self):
    self.properties["time"] = self.game_time = time.time() - self.game_time

    with open("saves/{}.json".format(ex.get_name_user()), mode="w",
              encoding="utf-8") as file:
        file.write(dumps(self.properties) + "\n")

