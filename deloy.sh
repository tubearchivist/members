#!/bin/bash
# deploy client container

test_host="blackhole.local"

function sync_test {
    # sync client to blackhole.local
    rsync -a --progress --delete-after \
        --exclude ".git" \
        --exclude ".gitignore" \
        --exclude "**/cache" \
        --exclude "**/__pycache__/" \
        --exclude "db.sqlite3" \
        . -e ssh "$test_host":tubearchivist-members

    ssh "$test_host" \
        'docker build -t bbilly1/tubearchivist-client tubearchivist-members'
    ssh $test_host "docker compose up -d"
}

function sync_production {
    # rebuild client on docker hub
    if [[ $(systemctl is-active docker) != 'active' ]]; then
        echo "starting docker"
        sudo systemctl start docker
    fi

    echo "latest tags:"
    git tag | tail -n 5 | sort -r

    printf "\ncreate new version:\n"
    read -r VERSION

    echo "push new tag: $VERSION?"
    read -rn 1

    git tag -a "$VERSION" -m "new release version $VERSION"
    git push origin "$VERSION"

    # start build
    sudo docker buildx build \
        --platform linux/amd64,linux/arm64 \
        -t bbilly1/tubearchivist-client:"$VERSION" \
        -t bbilly1/tubearchivist-client --push .
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
