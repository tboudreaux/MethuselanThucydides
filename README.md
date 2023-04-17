# Methuselan Thucydides
A more feature rich implementation of Paper.GPT. This is a webserver which
summarizes ever paper in arxiv categories every morning and allows you to ask
questions of them.

The name is a bit of a joke (albeit an extremley bad one). This app summarized
what has been been put on the arxiv, somewhat of a recent history of the
literature if you will. Thucydides, being one of the earliest rigorus historian
in western culture, seemed to fit. However, Thucydides famously lived <em>a
long time ago</em> so would be extremley old and likely physically incabable of
summarizing modern academic literature. Methusela was famously very old.... 

The joke is stretched and the metaphor is poor; however, what you can't say is
that its not a unique name.

# Installation

## Docker Installation
Much of the install is handled by the Dockerfile. However, in addition to 
docker you will need 

	1) milvis
	2) postgresql
	3) GPT-Retrival-API

Place the configuration information for these in the config.py file before
building the docker container. Once those are setup you can run the following
commands to build and deploy Methuselan Thucydides

```bash
git clone git@github.com:tboudreaux/MethuselanThucydides.git
cd MethuselanThucydides
cp config.py.user config.py
vim config.py # Edit the file as needed
export OPENAI_API_KEY=<Your API KEY>
export BEARER_TOKEN=<Your Bearer Token>
export DATASTORE="milvus"
docker build -t mt:v0.5 .
docker run -p 5516:5000 -d --restart always -e "BEARER_TOKEN=$BEARER_TOKEN" -e "OPENAI_API_KEY=$OPENAI_API_KEY" -e "DATASTORE=$DATASTORE" --name MethuselanThucydides mt:v0.5
```

The website will be accessible at localhost:5516

## Development Installation
Setup the databases and retrieval plugin in the same manner which you would have
for the docker installation. Then 

```bash
git clone git@github.com:tboudreaux/MethuselanThucydides.git
cd MethuselanThucydides
pip install -r requirments.txt
cp config.py.user config.py
vim config.py # Edit the file as needed
export OPENAI_API_KEY=<Your API KEY>
export BEARER_TOKEN=<Your Bearer Token>
export DATASTORE="milvus"
python app.py
```

This will run a server in development mode at 0.0.0.0:5515


## IMPORTANT
Note that there is currently no authentication. Therefore, anyone can ask
questions and CHARGE YOUR API KEY. This is a top priority for me, but be aware
of that!

Also, I am an astronomer, not a security researcher or even software engineer.
This is a hobby project which I am working on and would like to have at least
somewhat okay security. However, do not deploy in a low trust environment as I
am not willing to guarantee that I am following best security practices.

# Other Information

## Basic Usage
Basic usage should be self explanatory. The idea is that the website served
provides a brief summary of each paper posted to the arxiv on the previous day
(or over the weekend / Friday). These summaries are generated using gpt-3.5-tubo
and the abstract of the paper as listed on arxiv. The interface will default to
showing you all papers; however, category filters are shown in a sidebar. 

More complex behavior is enabled through the chat box associated to each paper.
This chat box is connected to gpt-3.5-turbo and a vector database storing all
the currently cached information about the paper (by using the
openai-textembedding-ada002 model). When you ask a question the most relevant
cached information about that paper is passed to the gpt model along with the
question and its response is printed out to the screen. Because by default only
the abstract and title are cached the responses gpt can give are limited.
However, if you click the "Abstract Mode Only" button and wait a few seconds
you will see that it changes to "Full Text Mode" and is no longer clickable.
Behind the scenes the full pdf of that paper has been downloaded and parsed
into text. That is then embedded into the same vector database. Now when you ask
questions the gpt model has far more context to answer them on. Because the
full text is stored in the database after anyone clicks the "Abstract Mode
Only" button one time it will always be greyed out in the future as that chat
box will always then default to considering the entire paper.

## Reverse Proxy
I have tested this running behind a nginx reverse proxy. Its quite
straightforward and no special configuration was needed.

## Screenshot
Simple demo of the state of the app in mid April 2023
![Example Photo](/imgs/demo.png?raw=true "Demo")

A slightly more complex example
![Example Photo 2](/imgs/demo2.png?raw=true "Demo 2")

## Notes
	1) Currently there is a bug in how I have implimented the arxiv API
	   such that it does not actually grab all the papers from a given day.
	2) I need to rework the memory model for a single chat to make it more 
	   robust
	3) Papers are currently not pulled automatically every day. A call to the
	   /api/fetch/latest must be made manually to fetch the latest papers. This
	   will be added as an automated job to the docker container. However for now
	   this should be pretty easy to impliment in cron (See below)
	4) I want to have chat memory stored server side for users once user
	   authentication is enabled. 

Basic crontab configuration to tell the server to fetch the latest papers
every day at 5 am. This assumes that your server is running at
https://example.com

```cron
0 5 * * * curl -v https://example.com/api/fetch/latest
```
