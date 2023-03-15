# Pystation-RestAPI
A simple API Framework built from scratch, *for learning purposes*.

# Motivation
The main intention behind this project is to strengthen the theoritical background of how APIs work, and also to build up some additonal functionalities that are currently don't exist in some famous backend frameworks.

# Some of the features exists in the current version V1.1:
- :white_check_mark: **CORS**: Make exclusions in the HTTP headers to permit the trusted hosts with the specified HTTP methods.
- :white_check_mark: **SQLite**: Used as the debugging database to store the user's info. 
- :white_check_mark: **User Authentication**: The Framework till now, Implements the Login Functionality and the users who have  the right credintals would be permitted to access the API's functionalities.
- :white_check_mark: **SHA256**:  Used as an extra layer of protection to save the passwords in the databse as encrpyted 256-bits.
- :white_check_mark: **Levenshtein Distance**: which is used to give a hint when an existing username is misspelled.

# How to use the Framework:
First of all, installing the requirements needed for the framework, the requirements are in the "requirements.txt" file, and can be installed using the following command:
``` bash
pip install -r requirements.txt
```
For now, to make excluding for some hosts from the CORS protection you can do so by alternating the desired server by the server in the following:
``` python
# Set the Allowed Host for the CORS permissions
allowedHost = "http://localhost:8000"
```

To experement with the methods currently provided (GET, POST) you can use any HTTP client software such as Postman and cURL, by sending for example to the following server, which is defined in the server.py:

``` bash
http://localhost:4000/login
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
