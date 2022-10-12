# 📁 About the project

Python project developed for System Integration Coding Challenge

The project consists in an implementation between a local Zammad Helpdesk with a Zammad API and two Python scripts
One for importing all tickets from a dataset of customer issues/complains [huggingface](https://huggingface.co/)
and the other one for predicting the sentiment of the issue and correctly updating the priority of it using a model of [sentimental classification](https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis?text=I+like+you.+I+love+you). 


# 📋 Run explanation and 💻 Requirements


Clone this repository with:
```bash
git clone https://github.com/masnik1/coding-challenge.git
```

At first you will need to run a local version of the Zammad ticketing tool running.
Do that by going to (make sure docker is running)

```bash
cd zammad-docker-compose-master
```
And then :
```bash
docker-compose up
```

This will serve the application at http://localhost:8080/ - Then make sure to start it with default values
Maybe you'll need to create a new ```ZAMMAD_TOKEN``` Auth token and update the ```.env``` file
I suggest as an example selecting all preferences on Zammad Helpdesk (tried just admin and ticket api and it did not work -> Selecting all worked)

So go to:
1. Your profile photo on Zammad Helpdesk
2. Profile
3. Token Access
4. Select all the permissions you need and copy the new token -> Update it on the ```.env``` file

Later, we just need to set our env to run our python scripts:
If you want to run it in a venv:

```bash
pip install virtualenv
virtualenv venv
```
If you are running LINUX:

```
source venv/bin/activate
```

Windows:
```
venv\Scripts\activate
```

To install the required python libs just go to your project folder (or venv path) and run:
```bash
pip install -r requirements.txt
```

After that you can run first the:
```import_tickets_zammad.py``` and then the ```update_tickets_zammad.py```

--------------------------------------------- ///////// -------------------------

# 🚀 Citations

Transformer model used : https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis?text=I+like+you.+I+love+you
Github repo : https://github.com/pysentimiento/pysentimiento