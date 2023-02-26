# Members Websocket client


## Configure
Environment variables:
- **MB_TOKEN**: Access token from members.tubearchivist.com
- **TA_URL**: Url of you Tube Archivist instance
- **TA_TOKEN**: Access token from your TA instance, accessible from the settings page.


## Build
```
docker build -t mb-client client
```

## Run
```
docker run \
    -e MB_TOKEN=xxxxxxxxxx \
    -e TA_URL=http://ta.blackhole.local \
    -e TA_TOKEN=yyyyyyyyyyy \
    --network=host \
    mb-client
```

## Compose
```yml
version: '3.3'

services:
  tubearchivist-client:
    image: bbilly1/tubearchivist-client
    container_name: tubearchivist-client
    restart: unless-stopped
    environment:
      - "MB_TOKEN=xxxxxxxxxx"
      - "TA_URL=http://tubearchivist.local"
      - "TA_TOKEN=yyyyyyyyyyy"
```
