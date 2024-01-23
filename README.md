# cs4700-project1

In developing the provided script, I employed the argparse module to handle command line arguments, allowing users to specify parameters such as the port, TLS encryption, hostname, and Northeastern username. The script then establishes a socket connection to the server (proj1.3700.network) on the default port 27993 or the specified port. Following the connection, a "hello" message is sent to the server, conveying the Northeastern username.

To populate the word list, the script reads the content of the "project1-words.txt" file, storing the words in memory. The guessing mechanism initiates with a predefined guess ("aahed"). If the server responds with a "retry" type, indicating an incorrect guess, the script updates the word list based on the received guess marks and positions. Subsequently, another guess is made, and this process continues until the server responds with a "bye" type. Upon receiving the "bye" response, the script prints the secret flag.

I am definitely not familiar with python. I spent a lot of time on the use of syntax and application of modules. moreover, Ensuring proper socket communication and handling diverse server responses presented complexities. Implementing TLS encryption correctly, particularly when the user specifies the --socket option, required careful attention. Additionally, managing the recursive guessing mechanism posed challenges to prevent potential infinite loops.

In terms of testing, most to running the python file to server to check whether i can get the secret flag from the server.
