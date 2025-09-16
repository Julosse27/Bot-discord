import discord

class Tuto_1(discord.ui.View):
    def __init__(self, *,  timeout: float | None = None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label= "Testez moi!", style= discord.ButtonStyle.red)
    async def button_callback(self, interaction: discord.Interaction, bouton):
        await interaction.user.send(f"Tu m'as testé !")
        await interaction.response.send_message(f"Bouton testé par {interaction.user.name}")