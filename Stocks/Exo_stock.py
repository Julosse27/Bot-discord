import discord

class Question(discord.ui.Button):
    def __init__(self, label: str, nb: int):
        self.rep = False
        self.nb = nb
        super().__init__(style= discord.ButtonStyle.blurple, label= label)

    async def callback(self, interaction: discord.Interaction):
        self.rep = True
    
class View_question(discord.ui.View):
    def __init__(self, labels: list[str]):
        super().__init__(timeout=500)
        for i in range(len(labels)):
            self.add_item(Question(labels[i], nb= i))

view = View_question(["test"])

view.children

exos = [
    {'nom': "Types de variables", 
     "questions": [
        (View_question(["test", "test2"]),
         "test",
         0
        )
    ]
    }
]
