import discord
from validation import validate_massage_rule
from config import allowed_chars


class Discensor(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        super().__init__(intents = intents)

    async def on_message(self, message):
        # 自分のメッセージは無視する
        if message.author == self.user:
            return

        # メッセージをログに出力する
        # 例： "user_name(user_id): message"
        print(f"{message.author.name}({message.author.id}): {message.content}")

        # メッセージが日本語のひらがな、カタカナ、漢字以外の文字をALLOWED_CHARS文字以上含んでいる場合は削除する
        result = validate_massage_rule(text = message.content, allowed_chars = allowed_chars)

        if result is False:
            # メッセージを削除する
            await message.delete()

            # メッセージを削除したことをログに出力する
            print(f"{message.author.name}({message.author.id}): {message.content} is deleted.")

            # メッセージを削除したことをメンション付きで通知する
            alert_message = f"日本語のひらがな、カタカナ、漢字以外の文字の使用は{allowed_chars}文字以下にしてください。"
            await message.channel.send(f"{message.author.mention}{alert_message}")
