 # Dumpass: A Fake Outlook Web App Login Page

## Overview
Dumpass is a simple Flask application that simulates a Microsoft Outlook Web App (OWA) login page. It is designed to trick users into entering their login credentials, which are then logged to a file. The application is intended for educational purposes only and should not be used for malicious purposes.

## Prerequisites
To run Dumpass, you will need the following:

* Python 3.6 or later
* Flask
* A web server (e.g. Apache, Nginx)

## Installation
1. Clone the Dumpass repository:

```
git clone https://github.com/username/dumpass.git
```

2. Install the required Python packages:

```
pip install -r requirements.txt
```

3. Configure your web server to serve the Dumpass application. For example, if you are using Apache, you can add the following lines to your Apache configuration file:

```
<VirtualHost *:80>
    ServerName dumpass.example.com
    DocumentRoot /path/to/dumpass/app
</VirtualHost>
```

## Usage
Once you have configured your web server, you can start the Dumpass application by running the following command:

```
python honeypot.py
```

The application will listen on port 5000 by default. You can access the login page by visiting the following URL:

```
http://dumpass.example.com
```

## Features
Dumpass includes the following features:

* A realistic OWA login page that mimics the look and feel of the real thing.
* Logging of user credentials to a file.
* The ability to redirect users to a different URL after they have entered their credentials.

## Security
Dumpass is not a secure application and should not be used in a production environment. The application is intended for educational purposes only and should not be used for malicious purposes.

## Disclaimer
The author of this application is not responsible for any damages or losses incurred as a result of using this application. Use this application at your own risk.
