# Terminal 1
code --new-window --title "Zookeeper" "cd /usr/local/kafka_2.13-3.3.1/ && sudo bin/zookeeper-server-start.sh config/zookeeper.properties"

# Terminal 2
code --new-terminal --title "Kafka" "cd /usr/local/kafka_2.13-3.3.1/ && sudo bin/kafka-server-start.sh config/server.properties"

# Terminal 3
code --new-terminal --title "User emulation" "bash -c 'cd /home/conor/Documents/Coding/Pinterest; python3 User_Emulation/user_posting_emulation.py; exec bash'"

# Terminal 4
code --new-terminal --title "API" "bash -c 'cd /home/conor/Documents/Coding/Pinterest; python3 API/pin_api.py; exec bash'"
