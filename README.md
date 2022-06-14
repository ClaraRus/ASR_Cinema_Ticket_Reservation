# ASR_Cinema_Ticket_Reservation

## Description
This repo contains the code used to create an IVR using VoiceXML for a cinema ticket reservation system within the scope of the Automatic Speech Recognition course.  

The research focuses on answering the following research questions:  
Q1: Does the ASR system for cinema ticket reservation discriminate against gender?  
Q2: Does it perform better when using male voices than female voices or vice-versa?  

The IVR's dialogue is described in the figure below:
![ASRAppdialogue](https://user-images.githubusercontent.com/43996861/173687790-f3f6e3a1-93d9-4598-8d20-55902429fc0d.png)

## Requirements
* Python
* Django
* Ngrok
* Twilio 

## Start the Cinema Ticket Reservation System

1. Create a Twilio account and get a phone number
2. Start the application running the following commands
 ```
cd ivr
python manage.py runserver

cd <ngrok install folder>
ngrok http 8000
```
3. Connect the Twilio phone number to the application using the ngrok address 

