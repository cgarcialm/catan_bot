import json
from telegram import ReplyKeyboardMarkup, KeyboardButton

FILL_OR_NOT, FILL_WOOD, FILL_CLAY, FILL_SHEEP, FILL_WHEAT, FILL_ROCK, DADOS = range(7)

def clear_all_resources(update, context):
    cleared_resources = {"madera": [], "arcilla": [], "ovejas": [], "trigo": [], "piedra": []}
    
    with open("resources.json", "w") as json_file:
        json.dump(cleared_resources, json_file)

def type_resource_dice(update, context, resource):
    """Run desired function to create return"""
    
    keyboard = [['1', '2', '3', '4'],
                ['5', '6', '7', '8'], 
                ['9', '10', '11', '12'], 
                [f'Terminar {resource}']]
    
    with open("resources.json", "r") as json_file:
        resources = json.load(json_file)
    if len(resources[resource])==0:

        context.bot.send_message(chat_id=update.message.chat.id,
                            text=f"Seleccioná un número para {resource} o Terminar",
                            reply_markup=ReplyKeyboardMarkup(
                            keyboard, input_field_placeholder=f"Número para {resource}",
                            ),
                        parse_mode='HTML')
    else:
        context.bot.send_message(chat_id=update.message.chat.id,
                            text=f"{resource}: {resources[resource]}",
                            reply_markup=ReplyKeyboardMarkup(
                            keyboard, input_field_placeholder=f"Número para {resource}",
                            ),
                        parse_mode='HTML')


def save_resource_dados(update, context, resource):
    result_dados = update.message.text

    with open("resources.json", "r") as json_file:
        resources = json.load(json_file)

    resources[resource].append(result_dados)

    with open("resources.json", "w") as json_file:
        json.dump(resources, json_file)

def fill_this_resource(update, context, resource):
    if update.message.text in [str(res) for res in list(range(1, 13))]:
        save_resource_dados(update, context, resource)
    type_resource_dice(update, context, resource)
    

def fill_wood(update, context):
    resource = 'madera'
    fill_this_resource(update, context, resource)

    return FILL_WOOD

def fill_clay(update, context):
    resource = 'arcilla'
    fill_this_resource(update, context, resource)

    return FILL_CLAY

def fill_sheep(update, context):
    resource = 'ovejas'
    fill_this_resource(update, context, resource)

    return FILL_SHEEP

def fill_wheat(update, context):
    resource = 'trigo'
    fill_this_resource(update, context, resource)

    return FILL_WHEAT

def fill_rock(update, context):
    resource = 'piedra'
    fill_this_resource(update, context, resource)

    return FILL_ROCK

# def next_resource(update, context):
    # if 