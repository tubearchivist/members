# Tube Archivist Members Client
This is a client container for https://members.tubearchivist.com.

This will keep a websocket connection open listening for notifications for new videos. Add your favorite channels to monitor on the [subscriptions](https://members.tubearchivist.com/subscriptions/) page.

## Install
Docker compose:
```yml
version: '3.5'
  services:
    tubearchivist-client:
      image: bbilly1/tubearchivist-client
      container_name: tubearchivist-client
      restart: "always"
      environment:
        - "MB_TOKEN=aaaaaaaaa"
        - "TA_URL=http://tubearchivist:8000"
        - "TA_TOKEN=bbbbbbbbb"
        - "TZ=America/New_York"
```

For `restart` policy use *always*, *on-failure* or *unless-stopped* to guarantee the listener stays open.

## Configure
You can configure the members client with various environment variables:
- **MB_TOKEN**: This is the access token you can find on your [members profile page](https://members.tubearchivist.com/profile/).
- **TA_URL**: Define the URL where your Tube Archivist instance is reachable, add protocol and port number if needed.
- **TA_TOKEN**: This is the access token for your Tube Archivist server, you can find that on the settings page.
- **TZ**: Defaults to UTC, optionally configure your timezone to adjust log output timestamps.
- **AUTOSTART**: Automatically prioritize and start videos sent from this service. Set to anything, except empty string, e.g. `AUTOSTART=True`.

## About the Licence
This project is licensed under GPL-3, with all the freedom attached to it. This client is preconfigured to interact with the server with defined timeouts, pings and other functionality that are verified server side. This includes server side rate limiting and blocking of malicious traffic. Modifying the client code to change functionality may result in triggering these limits and may automatically temporarily or permanently ban your connection and profile. If you see ways to improve this code, reach out first.

TLDR: The code is open source, but please don't modify the connection details with the server.
