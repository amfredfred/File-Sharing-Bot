import json
import hashlib

class CallbackDataManager:
    def __init__(self, json_file):
        self.json_file = json_file
        self.load_mappings()

    def load_mappings(self):
        try:
            with open(self.json_file, "r") as file:
                self.callback_data = json.load(file)
        except FileNotFoundError:
            self.callback_data = {}

    def save_mappings(self):
        with open(self.json_file, "w") as file:
            json.dump(self.callback_data, file, indent=4)

    def generate_callback_data(self, data):
        # Generate a unique hash for the data
        data_hash = hashlib.sha256(data.encode()).hexdigest()[:8]

        # Store the mapping between the data and the callback data
        self.callback_data[data_hash] = data
        self.save_mappings()

        return data_hash

    def get_data_from_callback(self, callback):
        # Retrieve the original data from the callback data
        return self.callback_data.get(callback)

    def remove_callback_data(self, callback):
        # Remove the mapping for the given callback
        if callback in self.callback_data:
            del self.callback_data[callback]
            self.save_mappings()


# Example usage
callback_manager = CallbackDataManager("callback_data.json")