import nextcord
from nextcord.ext import commands
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class Chatbot(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.conversing = False
        self.chat_history_ids = torch.zeros([1, 1]) # Empty Torch tensor for now
        self.strikes = 0 # Three strikes and the chatbot automatically stops

    @commands.command(aliases=["start_convo", "convo_start", "start_conversation", "conversation_start", "start_conversing"])
    async def chatbot_on(self, ctx):
        self.conversing = True
        await ctx.send("Commencing conversation mode.")
        await ctx.send("When finished, please remember to end conversation with 'eve chatbot_off'.")

    @commands.command(aliases=["end_convo", "convo_end", "end_conversation", "conversation_end", "stop_conversing"])
    async def chatbot_off(self, ctx):
        self.conversing = False
        await ctx.send("Ending conversation mode.")
        await ctx.send("Thank you for talking to me.")
        self.chat_history_ids = torch.zeros([1, 1])

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error): 
        '''This is just to block out a dumb error that occurs with the bot's set prefix.'''
        if isinstance(error, commands.CommandNotFound): 
            if not self.conversing:
                await ctx.send("Apologies, I don't recognize that command.")
                await ctx.send("If you would like to converse with me, please switch my chatbot feature on with 'eve chatbot_on'.")
            elif self.conversing:
                pass
    
    @commands.Cog.listener()
    async def on_message(self, message):
        '''Questions should be formatted like "eve how are you?"
        The sentence will remove the "eve " part and feed it into the DiabloGPT to receive a response.
        It will keep doing so as long as the chatbot feature is on.
        Note: The transformer often gets stuck and can't output proper sentences. I have to do more research into why.'''
        wakeword = message.content.lower()[:3]
        question = message.content.lower()[4:]
        if wakeword == "eve" and self.conversing and question != "chatbot_on":
            # Encode the input and add end of string token
            input_ids = self.tokenizer.encode(question + self.tokenizer.eos_token, return_tensors="pt")

            # Concatenate new user input with chat history (if there is)
            bot_input_ids = torch.cat([self.chat_history_ids, input_ids], dim=-1) if self.chat_history_ids.sum().data != 0 else input_ids

            # Generate a response
            self.chat_history_ids = self.model.generate(
                bot_input_ids,
                max_length=1000,
                do_sample=True,
                top_k=100,
                temperature=0.62, # The lower it is, the closer it is to greedy search
                pad_token_id=self.tokenizer.eos_token_id
            )

            output = self.tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
            if len(output.split()) < 3: 
                self.strikes += 1
                await message.channel.send("I'm not sure what to say.")
            else:
                self.strikes = 0 # Reset if the transformer climbs out of a crappy spiral
                await message.channel.send(output.capitalize())
            
            if self.strikes == 2: # Sometimes the transformer returns nothing repeatedly.
                await message.channel.send("Error in chatbot feature detected. Now ending conversation mode...")
                self.conversing = False
                self.chat_history_ids = torch.zeros([1, 1])
                await message.channel.send("If you would like to chat again, reinitiate chatbot mode with 'eve chatbot_on'.")
    
    @commands.command(aliases=["question"])
    async def q(self, ctx, *, question):
        '''Much more stable chatbot function. 
        Single question-and-answer format, no input of chat history.'''
        input_ids = self.tokenizer.encode(question + self.tokenizer.eos_token, return_tensors="pt")

        # Generate a response
        chat_history_ids = self.model.generate(
            input_ids,
            max_length=1000,
            do_sample=True,
            top_k=100,
            temperature=0.62,
            pad_token_id=self.tokenizer.eos_token_id
        )

        output = self.tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        await ctx.send(output)


def setup(client):
    client.add_cog(Chatbot(client))
