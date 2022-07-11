<!-- Intro -->
# **UV_HELPER**
> **Lucas Arroyo Blanco**  
> 
> _PatoOsoPatoso_  

&nbsp;

<!-- Index -->
# Table of contents
## &nbsp;&nbsp;&nbsp;&nbsp;1&nbsp;)&nbsp;&nbsp;[Description](#description)
## &nbsp;&nbsp;&nbsp;&nbsp;1&nbsp;)&nbsp;&nbsp;[Requeriments](#requeriments)
## &nbsp;&nbsp;&nbsp;&nbsp;2&nbsp;)&nbsp;&nbsp;[Modifications to be used](#modifications-to-be-used) 

&nbsp;  
&nbsp; 

<!-- Description -->
## **Description**

This project is focused on making it easier to use and navigate www.uv.es using automated stripts that notify the user when he gets new tasks or mails from their teachers without having the need of login into the website or the movil application.

* [monitor_virtual.py](monitor_virtual.py) is used to monitor the new tasks that appear in the aulavirtual and send a telegram notification when some new task is detected.  
* [monitor_mail.py](monitor_mail.py) is similar but instead of monitoring the new tasks, this script detects new mails and sends a telegram notification.  

&nbsp;

<!-- Requeriments -->
## **Requeriments**

* Telegram Bot
* Bot TOKEN
* Chat ID
* UV student account

&nbsp;   

<!-- Modifications -->
## **Modifications to be used**
To use the code as it is right now first you are going to need to create a **.env** file.  
The file should look like this:  
&nbsp;
```
UV_USER=...
UV_PASS=...
TELEGRAM_TOKEN=...
CHAT_ID=...
```  
In [monitor_virtual.py](monitor_virtual.py)	change `year = '2021-2022'` to your current years.  
&nbsp;  
&nbsp;

<!-- Bye bye -->
<img src="https://static.wikia.nocookie.net/horadeaventura/images/c/c2/CaracolRJS.png/revision/latest?cb=20140518032802&path-prefix=es" alt="drawing" style="width:100px;"/>**_bye bye_**