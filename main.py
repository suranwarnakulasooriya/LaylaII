# ==============================================================================
# run this file to run the bot
# ==============================================================================

from commands_help import *
'''
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
    #keep_alive()
    client.run(Bot.token)
