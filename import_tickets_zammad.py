import pandas as pd
from datasets import load_dataset
from zammad_utils.zammad import ticket

class DataAndAPI:

    def __init__(self):
        #Call the ticket Class
        self.ticketAPI = ticket.TicketAPI()

        #Here we load our dataset - convert do pandas format - select the first 50 from train
        #Also reset_index so we can store the position of the complain
        self.consumer_complaints = load_dataset("milesbutler/consumer_complaints")['train'].to_pandas().head(50).reset_index()

def formatTicket(row):
    ''' This small function will format the correct text for creating a ticket with an article '''
    title = "Complaint " + str(row['index'] + 1)
    subject =  row['Issue'] + ' ' + str(row['index'] + 1)
    body_text = row['Consumer Complaint']

    #Create the ticket
    filesAndAPI.ticketAPI.create_ticket_with_article(title, subject, body_text)
    print(f'Created title with name: {title}')

if __name__ == '__main__':

    filesAndAPI = DataAndAPI()

    #Here we creat the tickets based on the task
    filesAndAPI.consumer_complaints.apply(formatTicket, axis = 1 )

    print('Done all ticket creation')