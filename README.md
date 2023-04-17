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
