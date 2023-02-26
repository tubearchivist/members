# Tube Archivist Members Client
This is a client container for https://members.tubearchivist.com.

This will keep a websocket connection open listening for notifications for new videos. Add your favourite channels to monitor on the [subscriptions](https://members.tubearchivist.com/subscriptions/) page.

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

## Configure
You can configure the members client with various environment variables:
- **MB_TOKEN**: This is the access token you can find on your [members profile page](https://members.tubearchivist.com/profile/).
- **TA_URL**: Define the URL where your Tube Archivist instance is reachable, add protocoll and port number if needed.
- **TA_TOKEN**: This is the access token for your Tube Archivist server, you can find that on the settings page.
- **TZ**: Defaults to UTC, optionally configure your timezone to adjust logoutput timestamps.
