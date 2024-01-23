#!/usr/bin/env python3

import json
import ssl
import argparse
import socket


# Your client program must execute on the command line using the following command.
# $ ./client <-p port> <-s> <hostname> <Northeastern-username>

# set up the command line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-p", '--port', type=int, help = 'TCP socket bound to port 27993')
parser.add_argument("-s", '--socket', action="store_true", help = 'TLS encrypted requests on a TCP socket bound to port 27994')
parser.add_argument("hostname", type=str, default = 'proj1.3700.network', help = 'DNS or IP address')
parser.add_argument("username", type = str, default = 'wang.yunk', help = 'Northeastern username')

args = parser.parse_args()

hostname = args.hostname
username = args.username 

# connect to the server
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# The server runs on the machine proj1.3700.network and 
# listens for non-encrypted requests on a TCP socket bound to port 27993 
# it also listens for TLS encrypted requests on a TCP socket bound to port 27994

# If this parameter is not supplied on the command line, your program must assume that the port is 27993.
port = 27993
if args.port:
    port = args.port

# If this parameter is supplied on the command line and -p is not specified, your program must assume that the port is 27994.
elif args.socket:
    port = 27994
if args.socket:
    socket = ssl.wrap_socket(socket)

socket.connect((hostname, port))

# Send the hello message to the server
# {"type": "hello", "northeastern_username": <your-My.Northeastern-username>}\n
def send_hello_message(username):
    hello_message = '{"type": "hello", "northeastern_username": "' + username + '"}\n'
    socket.send(hello_message.encode())

# Open the text file "project1-words.txt" and read its content
with open("project1-words.txt", "r") as file:
    # Use a list comprehension to create a list of words
    project1_words = file.read().split()


# Exclude letters that the server returns as 0, and letters that are not in the correct position. All that's left are the secret flag
def filter(position, value, alphabet):
    filtered_words = []
    
    # Filter words based on the given criteria
    for word in project1_words:
        if (value == 0 and word[position] != alphabet) or (value == 2 and word[position] == alphabet):
            filtered_words.append(word)
    
    return filtered_words

# to send the guess to the server
def make_guess(server_id, guess_word):
    guess_message = '{"type": "guess", "id": "' + server_id + '","word": "' + guess_word + '"}\n'
    # send to the server
    socket.send(guess_message.encode())
    # receive and decode the server's response
    output = socket.recv(1024).decode()
    output = json.loads(output)

    # check the repond message
    # if we received retry, update the word list bsed on the given value
    if output["type"] == "retry":
        guess_mark = output["guesses"][0]["value"]
        for position, mark in enumerate(guess_mark):
            project1_words = filter(position, mark, guess_word[position])

        # make another guess
        make_guess(server_id, project1_words[0])

    # if we received bye, print the secret flag
    elif output["type"] == "bye":
        print(output["flag"])

#get the server id
send_hello_message(username)
output = socket.recv(1024)
output = output.decode()
output = json.loads(output)

server_id = output['id']
make_guess(server_id, 'aahed')

# close the socket
socket.close()





