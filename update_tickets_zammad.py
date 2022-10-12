import pandas as pd
from zammad_utils.zammad import ticket
import torch
from transformers import pipeline
from pysentimiento import create_analyzer


class Models:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        self.predictionDictScore = {'POS': 1, 'NEU': 2, 'NEG': 3}
        
        MODEL_CHECKPOINT = "finiteautomata/bertweet-base-sentiment-analysis"

        self.sentimentalTransformer = pipeline(task = 'sentiment-analysis', model=MODEL_CHECKPOINT)

        self.analyzerPySentimiento = create_analyzer(task="sentiment", lang="en")

        #Call the ticket Class
        self.ticketAPI = ticket.TicketAPI()

def getAllTickets():
    ''' Function to return all tickets in the system '''
    return pd.DataFrame( AllFilesModels.ticketAPI.list_tickets() )

def predictSentiment(row, usePysentimiento):
    ''' Function to predict the sentiment of the text based on Pysentimiento or direct transformer model'''
    ''' We will also Update the ticket if there is a difference between prediction and '''

    #Get the complaint based on article id
    complain = AllFilesModels.ticketAPI.get_articles_by_ticket_id(row['id'])

    #Here I've done with two approaches
    #Not sure the correct one
    #One using the lib pysentimento and other using directly the transformer lib
    if usePysentimiento:
        prediction = AllFilesModels.analyzerPySentimiento.predict(complain[0]['body']).output
    else:

        #need to use truncation = True -> Tried to change tokenizer length to bigger one but model was trained with max of 128
        #So the change did not help
        prediction = AllFilesModels.sentimentalTransformer(complain[0]['body'], truncation = True)[0]['label']
        print(prediction)

    #In case the current priority is different than the predicted priority -> We update it based on the new priority (by the model)
    if row.priority_id != AllFilesModels.predictionDictScore[prediction]:
        AllFilesModels.ticketAPI.update_ticket(row['id'], AllFilesModels.predictionDictScore[prediction])
        print(f'Ticket {row["id"]} priority updated from {row.priority_id} to {AllFilesModels.predictionDictScore[prediction]}')

        ''' Comments on task '''
        #For some reason all tickets were predicted between NEU and NEG
        #Reading all the reviews this seems correct, as there aren't any positive ones besides the one that was already there
        #All tickets were on priority 2 -> So just had changes from 2 to 3 -> That is why the prints show just changes from 2 to 3

if __name__ == '__main__':

    AllFilesModels = Models()
    all_tickets = getAllTickets()

    #If you want to use pysentimento just change it to True
    usePysentimiento = False
    all_tickets.apply(predictSentiment, usePysentimiento = usePysentimiento , axis = 1)

    print('All analysis and corrections on priority done')