# Team Tails - Isaac Jon, Brian Lee, Emily Lee, Max Millar

Tailos: A page for high school students (any high school) to use on a daily basis, including components such as the day’s weather and public transportation information (ex: train delays).

## Purpose
Talos is a site that gives high school students access to a variety of useful appliances during their journey through high school, including a built in weather app, traffic information, and news articles. Our site uses a registration system that allows students to create an account, and specify the school they attend. Upon logging in, these apps will be displayed on the home screen. The weather, traffic and public transportation gives information for weather and traffic, as well as public transportation directions based on the location of the student’s school.

## Launching the Site
Create a virtual environment:
```
python3 -m venv <venv_name>
```

Activate the virtual environment:
```
. <path to venv>/bin/activate
```

Run this command in our app’s home directory to install all necessary dependencies:
```
(venv)$pip install -r requirements.txt
```

Prepare the database by running:
```
python resetdb.py
```

Prepare API Keys:
- Acquire API keys for those found in [API Information](#API-Information)
- Load the keys into `keys.json`.
```
{
    "news":"<Insert key here>",
    "weather":"<Insert key here>",
    "traffic":"<Insert key here>",
    "commuteID":"<Insert key here>",
    "commuteCode":"<Insert key here>"
}
```

To run the app: 
```
(venv)$python app.py
```

## API Information
- Traffic: https://developer.mapquest.com/documentation/traffic-api/
- Commute: https://developer.here.com/documentation/transit/topics/what-is.html
- News: https://developer.nytimes.com/
- Weather: https://openweathermap.org/api/


## Dependencies: 
- Flask: Runs the web application on local host.
- Wheel: Used for Flask.
- SQLite: Creates databases for storing information.
- URLLib3: Receives information from APIs.
