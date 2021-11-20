

from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
import os
# import warnings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# warnings.filterwarnings('always',"error", "ignore", "always", "default", "module" , "once")



from chatbot.intent import HelloIntent

class ShoppingBot(object):
    def __init__(self, training_data_file = BASE_DIR+"/chatbot1/data/shopping-list/rasa/shopping-list-small.json", config_file = BASE_DIR+"/chatbot1/config/shopping-list/config_spacy.json"):
        training_data = load_data(training_data_file)

        trainer = Trainer(config.load(config_file))
        self.interpreter = trainer.train(training_data)
        self.shopping_list = {}
        self.temp = 0
        self.other = {}
        self.phone = 0
        self.address = ""

        # Create supported intents
        context = {'confidence_threshold':0.72}
        context1 = {'confidence_threshold':0.65}

        self.intents = {
                "greet"     : HelloIntent(self, "greet", context),
              




            }


    def handle(self, message):
        """
        Handles incoming message using trained NLU model and prints response to
        the system out
        Arguments:
            message the message from user to be handled with known intents
            (greet, add_item, clear_list, show_items, _num_items)
        """
        if message == '_num_items':
            val = self.intents['_num_items'].execute(None)
        else:
            nlu_data = self.interpreter.parse(message)
            intent = nlu_data['intent']['name']
            if self.intents[intent] is not None:
                val = self.intents[intent].execute(nlu_data)
                print("VALUE")

        return val