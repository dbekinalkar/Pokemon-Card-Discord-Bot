import discord
from pokemoncard import getCard

from db import addTradeList
from db import removeTradeList
from db import addToCollection
from db import getCollection

from db import getTradeList

async def help(message):
    await message.channel.send("<@"+str(message.author.id)+"> Valid use of the command:\n"+
    "c.trade <mention> [yourPokemon1(quantity), yourPokemon2(quantity)...] [traderPokemon1(quantity), traderPokemon2...]")

async def trade(message):
    content = message.content.lower()
    tradeDetails = content[8:]

    try:

        mentionList = message.mentions
        receiver = mentionList[0]

        # if receiver == message.user: raise Error("Same person")

        # if tradeDetails.index("[") == tradeDetails.rindex("[") or tradeDetails.index("[") == tradeDetails.rindex("["):
            # raise  Exception('only 1 array') # Make sure the two are not the same

        # if tradeDetails[tradeDetails.index("["):tradeDetails.index("[")] == tradeDetails[tradeDetails.rindex("["):tradeDetails.rindex("[")]:
            # raise Exception('Same Card')



        sCards = ( tradeDetails[ tradeDetails.index("[")+1:tradeDetails.index("]") ] ).split(", ")
        rCards = ( tradeDetails[ tradeDetails.rindex("[")+1:tradeDetails.rindex("]") ] ).split(", ")



        sCardsDict = {}
        for card in sCards:
            if card.strip()!="":

                if card.find("(")>0 and card.find(")")>0:
                    name=card[:card.find("(")]

                    if getCard(name.lower()) == None:

                        raise Exception('Not a card')

                    quantity=int(card[card.find("(")+1:card.find(")")])
                    sCardsDict[name]= quantity

                else:

                    name=card
                    if getCard(name.lower()) == None:
                        print("Not a card")
                        raise Exception('Not a card')

                    quantity=1
                    sCardsDict[name]= quantity



        rCardsDict = {}
        for card in rCards:
            if card.strip()!="":
                if card.find("(")>0 and card.find(")")>0:
                    name=card[:card.find("(")]
                    if getCard(name.lower()) == None: raise Exception('Not a card')

                    quantity=int(card[card.find("(")+1:card.find(")")])
                    rCardsDict[name]= quantity

                else:
                    name=card
                    print(name)
                    if getCard(name.lower()) == None: raise Exception('Not a card')

                    quantity=1
                    rCardsDict[name]= quantity



        await sendTradeMsg(sender=message.author, sCards=sCardsDict, receiver=receiver, rCards=rCardsDict)



        # After Successful Trade Message Sent
        embed = discord.Embed(title = "Trade", description="Trade successfuly sent!")
        await message.channel.send(embed=embed)
    except:
        await help(message)


async def sendTradeMsg(sender, sCards, receiver, rCards): # Edit messages to show trade has been accepted, commence trade



    embedS = discord.Embed(title="Trade Sent to " + receiver.name)



    embedR = discord.Embed(title="Trade Request from " + sender.name)



    sCardValue=""
    for key in sCards.keys():
        sCardValue += key.title()+" [x"+str(sCards[key])+"]\n"
    if sCardValue=="":sCardValue="_Nothing_"


    rCardValue=""
    for key in rCards.keys():
        rCardValue += key.title()+" [x"+str(rCards[key])+"]\n"
    if rCardValue=="":rCardValue="_Nothing_"


    embedS.add_field(name="You give:",value=sCardValue)
    embedS.add_field(name="You get:", value=rCardValue)
    embedS.set_footer(text="React with '❌' to decline")

    mSender = await sender.send(embed=embedS)
    await mSender.add_reaction("❌")


    embedR.add_field(name="You give:",value=rCardValue)
    embedR.add_field(name="You get:", value=sCardValue)
    embedR.set_footer(text="React with '✅' to accept, with '❌' to decline")

    mReceiver = await receiver.send(embed=embedR)
    await mReceiver.add_reaction("✅")
    await mReceiver.add_reaction("❌")

    sendPair = (mSender.channel.id,mSender.id)
    print(str(sendPair))
    recPair = (mReceiver.channel.id,mReceiver.id)
    addTradeList((sendPair, recPair))


async def tradeAccepted(client, message):
    print("trade accepted")
    pair = removeTradeList(message.channel.id, message.id)
    message2 = None
    if message.channel.id == pair[0][0]:
        channel = await client.fetch_channel(pair[1][0])
        message2 = await channel.fetch_message(pair[1][1])
    elif message.channel.id == pair[1][0]:
        channel = await client.fetch_channel(pair[0][0])
        message2 = await channel.fetch_message(pair[0][1])

    if message2 != None: print("message2 exists")

    tradeDetails = message.embeds[0].fields

    trader1give = {}
    for line in tradeDetails[0].value.split("\n"):
        if line!="_Nothing_":
            pokemon = line[:line.find(" [")]
            quantity = line[line.find(" [x")+3:line.find("]")]
            trader1give[pokemon] = int(quantity)

    trader2give = {}
    for line in tradeDetails[1].value.split("\n"):
        if line!="_Nothing_":
            pokemon = line[:line.find(" [")]
            quantity = line[line.find(" [x")+3:line.find("]")]
            trader2give[pokemon] = int(quantity)


    #Need to lock access to people's collection while trade is happening
    if checkCardAvailable(message.channel.recipient.id, trader1give) and checkCardAvailable(message2.channel.recipient.id, trader2give):

        for cardName in trader1give: # Nothing is getting added to the collection, fix it
            addToCollection(message.channel.recipient.id, getCard(cardName), quantity=-1 * trader1give[cardName])
            addToCollection(message2.channel.recipient.id, getCard(cardName), quantity=trader1give[cardName])
        for cardName in trader2give:
            addToCollection(message2.channel.recipient.id, getCard(cardName), quantity=-1 * trader2give[cardName])
            addToCollection(message.channel.recipient.id, getCard(cardName), quantity=trader2give[cardName])

        embed1 = discord.Embed(title = "Trade Accepted!")
        embed1.add_field(name=tradeDetails[0].name, value=tradeDetails[0].value)
        embed1.add_field(name=tradeDetails[1].name, value=tradeDetails[1].value)
        embed1.set_footer(text="Traded with "+message2.channel.recipient.name+"#"+message2.channel.recipient.discriminator)

        embed2 = discord.Embed(title = "Trade Accepted!")
        embed2.add_field(name=tradeDetails[0].name, value=tradeDetails[1].value)
        embed2.add_field(name=tradeDetails[1].name, value=tradeDetails[0].value)
        embed2.set_footer(text="Traded with "+message.channel.recipient.name+"#"+message.channel.recipient.discriminator)

        await message.edit(embed = embed1)
        await message2.edit(embed = embed2)
    else:
        embed1 = discord.Embed(title = "Trade Failed")
        embed1.add_field(name=tradeDetails[0].name, value=tradeDetails[0].value)
        embed1.add_field(name=tradeDetails[1].name, value=tradeDetails[1].value)
        embed1.set_footer(text="Not enough cards")

        embed2 = discord.Embed(title = "Trade Failed")
        embed2.add_field(name=tradeDetails[0].name, value=tradeDetails[1].value)
        embed2.add_field(name=tradeDetails[1].name, value=tradeDetails[0].value)
        embed2.set_footer(text="Not enough cards")

        await message.edit(embed = embed1)
        await message2.edit(embed = embed2)


def checkCardAvailable(id, cardDict): # check if people have enough cards to trade
    bool = True
    collection=getCollection(id)
    for card in cardDict:
        if not card in collection or cardDict[card] > collection[card]:
            print(str(id))
            print(cardDict)
            print(collection)
            bool = False
    return bool


async def tradeDeclined(client, message): # Edit messages to show that trade has been declined
    print("It worked")
    pair = removeTradeList(message.channel.id, message.id)
    print(pair)
    message2 = None
    if message.channel.id == pair[0][0]:
        channel = await client.fetch_channel(pair[1][0])
        message2 = await channel.fetch_message(pair[1][1])
    elif message.channel.id == pair[1][0]:
        channel = await client.fetch_channel(pair[0][0])
        message2 = await channel.fetch_message(pair[0][1])

    embed = discord.Embed(title = "Trade Declined", description="Trade Declined by " + message.channel.recipient.name+"#"+message.channel.recipient.discriminator)

    await message.edit(embed=embed)
    await message2.edit(embed=embed)

    print(getTradeList())
