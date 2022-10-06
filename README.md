ReadMe:
My approach to the wordle game was
to have an object that communicates with the server
and is equipped to recursively handle a message from the server
and appropriately responds with a new message.
This new message is a guess which is made after filtering
out words from the word list given the previous message
and the information about what letters are valid. The validity
of letters is stored in a dictionary where each letter
is associated with an boolean array of size 5 indicating
which places this letter is valid in. Once the guess is made
the server responds and repeats the filter and guess process until
the correct word is identified.

The main challenges that I faced while working on this project
were both the challenge of filtering out the right words and
having new guesses implement information from previous guesses as
well as trouble implementing the TLS connection.

I tested my code mainly by running the game and printing out
removed words and checking the validity of the removed words
and checking if new guesses were actually optimal.
