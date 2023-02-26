#!/bin/bash
# deploy client container

test_host="blackhole.locyl"

function sync_test {
    # sync client to blackhole.local
    rsync -a --progress --delete-after \
        --exclude ".git" \
        --exclude ".gitignore" \
        --exclude "**/cache" \
        --exclude "**/__pycache__/" \
        --exclude "db.sqlite3" \
        . -e ssh "$test_host":tubearchivist-members

    ssh $test_host \
        "docker compose up -d --build"
}

function sync_production {
    # rebuild client on docker hub
    if [[ $(systemctl is-active docker) != 'active' ]]; then
        echo "starting docker"
        sudo systemctl start docker
    fi

    # start build
    sudo docker buildx build \
        --platform linux/amd64,linux/arm64 \
        -t bbilly1/tubearchivist-client --push client
}

if [[ $1 == "test" ]]; then
    sync_test
elif [[ $1 == "docker" ]]; then
    sync_production
elif [[ $1 == "validate" ]]; then
    validate "$2"
else
    echo "valid options are: test | docker"
fi

##
exit 0
