# doge-streamlabs-alert
Creates Streamlabs alert for incoming DOGECOIN donations (to locally running Dogecoin Core Wallet)  
This has not been tested well enough! Only tested some stuff on Linux so far. Use at your own risk!

## How to set up
### Python3
Install Python 3 [(Windows instructions)](https://phoenixnap.com/kb/how-to-install-python-3-windows) and install the needed Python packages listed in the requirements.txt using the pip command line tool.

### Dogecoin Core Wallet
First, you need to install and [configure a Dogecoin Core wallet](https://www.reddit.com/r/dogecoin/wiki/dogecoincoreguide). Once that has been set up, find your dogecoin.conf configuration file and add a few lines to it:
```
server=1
rpcallowip=127.0.0.1
rpcallowip=192.168.0.1/24
rpcuser=someusername
rpcpassword=supersafepassword
walletnotify=/full/path/to/notifywallet.py %s
```
You need to replace `someusername` with a username of your liking and `supersafepassword` with an actually safe and unique password. You also need to replace `/full/path/to/` with the actual path to the downloaded `notifywallet.py`. If you are on Windows, you probably have to add the path to the python3 executable in front of this (with a space to seperate it from the rest of the command)

You need to put the same username and password into the `rpccreds.json` file in the `data` folder. Use `rpccreds-exampke.json` as an example as to how the file has to look like.

### Streamlabs

Log into Streamlabs and follow the [instructions on their page](https://dev.streamlabs.com/docs/register-your-application). 
Please copy the Client ID and Client Secret that are generated in the process into the `tokens.json` file in the `data` folder.
If you dont have a `tokens.json` file there, rename the `tokens-example.json` file to `tokens.json` and put the information into there. If the app has not been approved by Streamlabs, it can only send 5 alerts per minute, which is probably the case with this.

Once you have done that, start the donation message relay server by executing server.py using python on your command line/console  
`python3 /full/path/to/downloaded/files/server.py`

Once you have started it. open ``http://localhost:42069/`` in your web browser and click on the Dogecoin. It will lead you to the Streamlabs webpage, where you need to give it the permissions to access your Streamlabs data. Once you have done that, you'll get redirected to a white page that just says Success.

Now, restart your Dogecoin Core wallet, and enjoy notifications for DOGE donations showing up in the default Streamlabs notification box/area!
