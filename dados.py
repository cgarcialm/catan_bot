import csv
from telegram import ReplyKeyboardMarkup

# import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

DADOS = 6


def type_result_dice(update, context):
    keyboard = [['1', '2', '3'], 
                ['4', '5', '6'],
                ['7', '8', '9'], 
                ['10', '11', '12']]
    context.bot.send_message(chat_id=update.message.chat.id,
                     text="Resultado de los dados?",
                     reply_markup=ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=False,
                                       resize_keyboard=True,
                                       ),
                     parse_mode='HTML')


def save_dados(update):
    result_datos = update.message.text

    with open(r'dados.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([result_datos])

def load_dados(update):
    with open("dados.csv") as f:
        all_results_datos = [int(res[0]) for res in list(csv.reader(f))]
        # print(all_results_datos)

    return all_results_datos

def print_dados(update):
    all_results_datos = load_dados(update)
    update.message.reply_text(all_results_datos)
    # update.message.reply_text(update.message.text)

def plot_dados(update):
    all_results_datos = [[res] for res in load_dados(update)]
    df = pd.DataFrame.from_records(all_results_datos, columns=['result'])
    # df = px.data.tips()
    fig = go.Figure(data=[go.Histogram(x=df['result'])])
    layout = go.Layout(
        # title='some title',
        xaxis=dict(
            # title='Xaxis Name',
            range=[0.5, 12.5],
            tickmode='linear'
            ),
        # yaxis=dict(
        #     tickformat ='d'
        # )
        )
    fig.update_layout(layout)
    # fig.show()
    fig.write_image("images/histogram.png")

def process_dados(update, context):
    """Run desired function to create return"""
    type_result_dice(update, context)
    if update.message.text in [str(res) for res in list(range(1, 13))]:
        save_dados(update)
        plot_dados(update)
        print_dados(update)

    return DADOS

def clear_results_dados_csv():
    filename = "dados.csv"
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    f.close()