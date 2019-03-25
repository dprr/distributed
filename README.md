# README

## Claim 
This system provides a group chat such that there is anonymity and liveness.

### Assumptions
* The clients follow the protocol. We assume such because the system creates 
a closed chat group, and that means that the users will only allow trusted new
users to join the group.
* Three servers are following the protocol and one may be byzantine.

### Normal run of the system
1. There are 4 servers and 1 of them may be byzantine.
1. Clients connect to the servers. The order of connection 
to the servers is important.
1. Every epoch, each client send either one message or no messages to the 
servers.
    1. If the client has a message to send then the client will send 
that message.
    1. If the client does not want to send a message, then an empty
message will be sent.
1. A half an epoch later, the clients receive from the servers parts from
**all** of the messages send during the previous epoch.
1. The client receives either three or four parts of the messages
from the servers, depending on how the byzantine server acts.
1. The client recovers the message using a method described later.
1. Each client has the ability to read previous messages. A message can 
be read if it was sent after the client joined and before the last epoch.
1. Each client can quit the group whenever they want.

### Client sending procedure
1. Decide what message to send. That message can be changed as many times
as wanted, within the sending time frame.
1. Convert the message to an integer using hexlify, with the value of the 
empty message being zero.
1. Create a list of size LEN_OF_BOARD.
1. Choose one polynomial of degree one 
(because there exists at most one byzantine server) such that f(0) 
is equal to the message and LEN_OF_BOARD - 1 polynomials such that f(0) is 0.
1. Order the polynomials in a random order.
1. Create four lists such that list j has f<sub>i</sub>(j) for all i indices
in the list.
1. Every epoch on the epoch send list j to server j.

### Server storage method
1. Store a list of size LEN_OF_BOARD full of zeros.
1. Whenever given a new list from a client, sum the new list to the stores list.
1. Send the list to all of the clients each epoch on the half epoch
and zero the stored list.

### Client recovery procedure
1. Receive 4 or 3 vectors from the server 
(3 if of the byzantine server sends nothing).
1. Organize the list by function 
(LEN_OF_BOARD list of 4 points and not 4 list of LEN_OF_BOARD points).
1. Take lists of 2 points and decide what the real message was by checking
if when using one of the server's list, the recovered message is different
then when not using that server's list. And when not using that server's 
list, all other recovered messages recovered regardless of which 2 lists
out of the remaining three lists are chosen.
1. Ignore the empty messages and save the real messages

### Claim for anonymity
A malicious server can only knows who is connect to it and nothing more.
### Proof
* Every client sends a message each epoch, 
so the server can't learn who sent the message.
* No server has access to more than 1 point,
 so it cannot learn what is the message.
* A client sends a message each epoch (really one or dummy), 
so the server can't know when a client sent a real message.

### Claim for liveness
Regardless as to what the byzantine server does, the system is live.
### Proof
Every epoch the clients send their messages and every epoch the clients 
receive at least three parts of their message.
