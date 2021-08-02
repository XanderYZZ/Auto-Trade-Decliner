from discord_webhook import DiscordWebhook, DiscordEmbed
import json

config = json.load(open('./config.json',))

messageColor = 'dc143c'
Webhook_URL = config["Webhook_URL"]

def sendWebhook(hookTitle, hookDescription, opposingUserName):
    webhook = DiscordWebhook(url=Webhook_URL)

    # Color is decimal or hex
    embed = DiscordEmbed(title=hookTitle, description=hookDescription, color=messageColor)

    # Change name to the opposing player later on
    embed.set_author(name=f"Trade with {opposingUserName} declined")

    # Add the embed object to the webhook
    webhook.add_embed(embed)

    response = webhook.execute()