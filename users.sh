#!/bin/bash

anonymous_sudo_users=(
    "thecondor"
    "solo"
    "thehomelesshacker"
    "darkdante"
    "vigilante"
)

anonymous_normal_users=(
    "shinobi"
    "sabu"
    "topiary"
    "shadowfax"
    "kayla"
    "anarchaos"
    "tflow"
    "vince"
    "ryan"
    "morpheus"
)

underground_sudo_users=(
    "darksoul"
    "nullvoid"
    "spectre"
    "ghostuser"
    "blackhatcat"
)

underground_normal_users=(
    "reaper"
    "404"
    "echelon"
    "thejester"
    "madfrog"
    "mafiaboy"
    "jok3r"
    "c0br4"
    "shadow"
    "zodiac"
)

anonymous_password="An0nymous_123"
underground_password="Und3rground_123"

if [[ $1 == "anonymous" ]]; then
    for user in "${anonymous_sudo_users[@]}"; do
        if ! id "$user" &>/dev/null; then
            sudo useradd "$user"
            echo "$user:$anonymous_password" | sudo chpasswd
            sudo usermod -aG sudo "$user"
        fi
    done

    for user in "${anonymous_normal_users[@]}"; do
        if ! id "$user" &>/dev/null; then
            sudo useradd "$user"
            echo "$user:$anonymous_password" | sudo chpasswd
        fi
    done
elif [[ $1 == "underground" ]]; then
    for user in "${underground_sudo_users[@]}"; do
        if ! id "$user" &>/dev/null; then
            sudo useradd "$user"
            echo "$user:$underground_password" | sudo chpasswd
            sudo usermod -aG sudo "$user"
        fi
    done

    for user in "${underground_normal_users[@]}"; do
        if ! id "$user" &>/dev/null; then
            sudo useradd "$user"
            echo "$user:$underground_password" | sudo chpasswd
        fi
    done
else
    echo "Usage: $0 <userbase>"
    echo "Valid options for <userbase>: anonymous, underground"
    exit 1
fi
