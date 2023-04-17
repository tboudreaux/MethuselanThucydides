# Methuselan Thucydides
A more feature ritch implimentation of Paper.GPT. This is a webserver which 
summariezes ever paper in arxiv categories every morning and allows you to ask questions of them.

# Installation
Much of the install is handeled by the Dockerfile. However, in addition to 
docker you will need 

	1) milvis
	2) postgresql
	3) GPT-Retrival-API

Place the configuration information for these in the config.py file before
building the docker container. Once those are setup

```bash
docker build -t mt:v0.5 .
docker run -p 5516:5000 -d --restart always -e "BEARER_TOKEN=$BEARER_TOKEN" -e "OPENAI_API_KEY=$OPENAI_API_KEY" -e "DATASTORE=\'milvus\'" --name MethuselanThucydides mt:v0.5
```

This assumes you have put your OPENAI_API_KEY and BEARER_TOKEN in an
enviromental variable.

The website will be accesable at localhost:5515


Note that there is currently no authentication. Therefore, anyone can ask
questions and CHAREGE YOUR API KEY. This is a top priority for me, but be aware
of that!

## Screenshot
Simple demo of the state of the app in mid April 2023
![Example Photo](/imgs/demo.png?raw=true "Demo")

A slightly more complex example
![Example Photo 2](/imgs/demo2.png$raw=true "Demo 2")

## Notes
	1) Currently there is a bug in how I have implimented the arxiv API
	   such that it does not actually grab all the papers from a given day.
	2) I need to rework the memory model for a single chat to make it more 
	   robust
	3) Papers are currently not pulled automatically every day. A call to the
	   /api/fetch/latest must be made manually to fetch the latest papers. 
	   This will be added as an automated job to the docker container.
	4) I want to have chat memory stored server side for users once user
	   authentication is enabled. 
