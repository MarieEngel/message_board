### _This is just a placeholder until details have been specified with our client._
***

# message_board

Message board using geographic location of users

Users can write messages  and these messages are shown to others who are geographically close. Messages can be tagged with categories such as "offer/seek rideshare", "books I want to lend out", "lost house pet", etc. .

## Setup:

- Install Python 3.10

```sh
brew install python@3.10
brew unlink python@3.9
brew link python@3.10
```

- Create a virtual environment

```sh
python3 -m venv venv
```

- Activate the environment and install the dependencies

```sh
source venv/bin/activate
pip install -r requirements.txt
```

## Objectives:

- Design and develop base site with layout, admin area.

- Create base site for signing up, marking other users as connections, etc.

- Create workflow for posting messages and seeing messages from other users

- Create a general sharing workflow. Allow users to share URLs to rides by email and make the URLs unique so that one can track how often a particular email recipient has clicked a specific link.

- Ensure workflow can be used for for ride sharing, seeking lost pets and lending out books.

- Add a way to respond to posted messages.

- Add tests

- Deploy site to cloud


## Stretch goals:

- Integrate Open Layers maps

- Integrate GeoDjango/GIS for making ride sharers find one another

- Integrate payment API for a enhanced accounts whose messages will be shared with a wider group of users

- SEO for public pages

