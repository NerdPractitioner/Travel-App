# Travel-App

## Contents
* [Introduction](#introduction)
* [In Progress](#in-progress)
* [Integrations](#integrations)

## Introduction
This is a Django web application for a travel community. It will include social capabilities such as user profiles and chat groups.
It will also allow users to find each other by proximity and meetup or help each other while traveling. 

This ReadMe will host notes needed to run the app locally and in production on Windows OS
*Jump to: [Integrations](#integrations),[In Progress](#in-progress), [Page Top](#contents)*, 

## In Progress
Working in branch add-react
Installing react frontend using npm, <a href="https://parceljs.org/getting_started.html">Parcel</a> and <a href="https://babeljs.io/setup">Babel</a>.




windows npm help https://www.npmjs.com/get-npm



## Integrations
The current build is entirely run on Django but we are looking into React/Vue front end capabilities. 

###Chat
Chat is running on websockets through "channels". This requires <a href="https://redis.io/topics/introduction">redis</a> 
Windows install help <a href="https://stackoverflow.com/questions/6476945/how-do-i-run-redis-on-windows/19579610#19579610">here</a>

*Jump to: [Introduction](#introduction), [In Progress](#in-progress), [Page Top](#contents)*
