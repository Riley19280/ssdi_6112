
## Getting Started

#### Start docker
    docker-compose up --build
    
#### Starting webserver locally
    python manage.py runserver
    
#### Runing migrations
    python manage.py migrate

### Data files

I have provided example data files that show the format of the data we are dealing with. The first one is a direct message conversation, and the second is a group chat with 100+ people. The data goes back until around November 2019.

### Using your own data
https://www.facebook.com/settings?tab=your_facebook_information

Download your personal Facebook Messenger data [here](https://www.facebook.com/settings?tab=your_facebook_information).

Select "Download Your Information"

Change the format to "JSON", then click "Deselect All" on the right.

Scroll down and choose "Messages", this will only download the required data.

Scroll back up and press "Create File". Facebook will then  begin processing your data request and send you an email when your data is ready to download.

Once you have download the .zip provided by Facebook, extract the contents to a folder. Within that folder, navigate to messages => inbox. This is where all of your current conversations are. You can choose the one you want here. Open the chosen folder and upload the message_1.json file.