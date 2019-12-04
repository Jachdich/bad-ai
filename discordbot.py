import discord
from discord.ext import commands
import ai, os, json, random, requests

bot = commands.Bot(command_prefix="-")

@bot.command()
async def generate(ctx, filename:str, length:int):
    try:
        with open("models/" + filename + ".model", "r") as f:
            x = json.loads(f.read())
            model = x[0]
            raw = x[1]
    except IOError:
        await ctx.send("Error - Specified model does not exist.")
        return

    memsize = int(filename.split("-")[1])
    
    y = random.randint(0, len(raw) - memsize - 1)
    out = ai.predict(raw[y:y + memsize], length, model)
    if len(out) < 2000:
        await ctx.send(out)
    else:
        await ctx.send("Error - texts larger than 2000 chars will be supported soon.")

@bot.command()
async def list(ctx):
    files  = [x.strip(".model") for x in os.listdir("models") if x.endswith(".model")]
    files2 = [x.strip(".txt") for x in os.listdir("training_data") if x.endswith(".txt")]
    out = "Models available are:\n```\n" + "\n".join(files) + "```\n"
    out += "Training data files available are:\n```\n" + "\n".join(files2) + "```"
    await ctx.send(out)

@bot.command()
async def upload_file(ctx, remote_filename):
    attachment_url = ctx.message.attachments[0].url
    file_request = requests.get(attachment_url)
    with open("training_data/" + remote_filename + ".txt", "w") as f:
        f.write(file_request.content.decode("utf-8"))
        
@bot.command()
async def train(ctx, filename:str, memsize:int):
    try:
        with open("training_data/" + filename + ".txt", "r") as f:
            tdata = f.read()
    except IOError:
        await ctx.send("Error - Specified model does not exist.")
        return

    model = ai.train(tdata, memsize)

    with open("models/" + filename + "-" + str(memsize) + ".model", "w") as f:
        f.write(json.dumps([model, tdata]))

    await ctx.send("Done!")


bot.run(open("token").read())
