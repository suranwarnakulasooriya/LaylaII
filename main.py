# ==============================================================================
# run this file to run the bot
# ==============================================================================

from commands_help import *
'''
# uncomment if you want to run in cloud
app = Flask('')

@app.route('/')
def home():
  return "Hi there hello."

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
'''
@client.event
async def on_ready():
    print('\nLayla II is online.\n')

if __name__ == '__main__':
    #keep_alive() # uncomment if you want to run in cloud
    client.run(Bot.token)
