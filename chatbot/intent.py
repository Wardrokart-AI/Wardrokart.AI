

from chatbot.command import GreetCommand
class Intent(object):

    def __init__(self, bot, intent_name, context):
        
        self.chatbot = bot
        self.name = intent_name
        self.context = context
        self.commands = []
        self.initCommands()

    def execute(self, nlu_data):
        """
        Executes given intent by applying appropriate command to the given
        parsed NLU data response
        """
        for c in self.commands:
           
            val = c.do(self.chatbot, None)
          
            return val

    def initCommands(self):
        """
        The method to init specific to particular intent.
        """
        pass

