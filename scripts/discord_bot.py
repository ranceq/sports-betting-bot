import discord
import pandas as pd
import os
import json
import asyncio

# Dynamically resolve the path to config.json
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "..", "config.json")
with open(config_path) as f:
    config = json.load(f)

TOKEN = os.getenv("DISCORD_BOT_TOKEN") or config.get("discord_bot_token")
CHANNEL_ID = config.get("discord_channel_id")  # Ensure this is an integer

def format_top25_message(df):
    message = "**Top 25 Bets for Today:**\n"
    for idx, row in df.iterrows():
        message += (f"{idx+1}. **{row['Match']}** | Outcome: {row['Bet']} | "
                    f"Odds: {row['Odds']} | Confidence: {row['Confidence']}/10\n")
    return message

async def send_discord_notification():
    client = discord.Client(intents=discord.Intents.default())
    
    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")
        channel = client.get_channel(CHANNEL_ID)
        if channel is None:
            print("Channel not found!")
            await client.close()
            return
        
        # Load top 25 bets
        top25_path = os.path.join(current_dir, "..", "data", "top25_bets.csv")
        df = pd.read_csv(top25_path)
        message = format_top25_message(df)
        await channel.send(message)
        await client.close()
    
    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(send_discord_notification())
