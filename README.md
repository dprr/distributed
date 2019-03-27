# README

## Claim 
This system provides a group chat that preserves anonymity and liveness.

### Assumptions
* The clients follow the protocol. We assume such because the system creates 
a closed chat group, and that means that the users should only allow trusted 
new users to join the group.
* Three servers are following the protocol and one may be malicious.

### Explanation of the protocol
1. There are 4 servers and 1 of them may be malicious.
1. Clients connect to the servers. Every client must connect to the servers
in the same way. For example, the server the all clients connect to first,
is number 1.
1. Every epoch, each client has either one message or no messages to send.
    1. If the client has a message to send then the client will send 
that message.
    1. If the client does not have a message, then an empty
message will be sent.
1. A half an epoch later, the clients receive from the servers parts from
**all** of the messages send during the previous epoch.
1. The client receives either three or four parts of the messages
from the servers, depending on how the malicious server acts.
1. The client recovers the message using a method described later.
1. Each client has the ability to read previous messages. A message can 
be read if it was sent after the client joined and before the current epoch.
1. Each client can quit the group whenever they want.

### Client sending procedure
1. Decide what message to send. That message can be changed as many times
as wanted, within the sending time frame. Alternatively, no message can 
be chosen in which case an empty message will be sent.
1. Convert the message to an integer using hexlify, with the value of the 
empty message being zero.
1. Create a list of size LEN_OF_BOARD.
1. Choose one polynomial of degree one 
(because there exists at most one malicious server) such that f(0)
is equal to the message and `LEN_OF_BOARD - 1` polynomials such that f(0) is 0.
1. Order all of the polynomials in a random order.
1. Create four lists such that list j has f<sub>i</sub>(j) for all i indices
in the list.
1. Every epoch on the epoch send list j to server j.

### Server storage method
1. Store a list of size LEN_OF_BOARD full of zeros.
1. Whenever given a new list from a client, sum the new list to the stored list.
1. Send the list to all of the clients every epoch on the half epoch
and afterwards, zero the stored list.

### Client recovery procedure
1. Receive 4 or 3 vectors from the server 
(3 if of the malicious server sends nothing).
1. Organize the list by the polynomials 
(LEN_OF_BOARD list of 4 points and not 4 list of LEN_OF_BOARD points).
1. Take lists of 2 points and decide what the real message was by checking
if when using one of the server's list, the recovered message is different
then when not using that server's list. And when not using that server's 
list, all other recovered messages recovered regardless of which 2 lists
out of the remaining three lists are chosen, are equal.
1. Ignore the empty messages and save the real messages.

### Claim for correctness
After every epoch, all clients can recover all messages from the previous
epoch.
#### Proof
* If two points on a polynomial of rank one are known. Then the entire 
polynomial is known and calculating its zero is trivial.
* Given two polynomials, the sum of both of the values at point x,
can be used to create a new polynomial that is the sum of both 
starting polynomials. The zero on that new polynomial is equal to the sum
of the zero from both of the starting polynomials.
* Assuming that there is not a conflict, a given point in a server's
vector represents the sum of a polynomial with a zero being equal to 
a message and all other polynomials with a zero equaling zero. Therefore, 
by summing all of the polynomials, the result will be a polynomial that 
has a zero equal to the message.
* Assuming that there is a conflict then either a random string
will be written or `Not ciphertext of utf-8` will be stored. 
If a client sees the message `Not ciphertext of utf-8` and 
not their message, they should try during the next epoch to send 
the message again. 

#### Limitations
* A byzantine client can send a full vector to each server 
thereby guaranteeing that no message will be recovered.


### Claim for anonymity
#### Definition
In this project, we will define anonymity as follows:
1. No party can know any information about which client sent a 
given message.
1. Only the clients can know the contents of the messages.
 
#### Proof
* Every client sends a message each epoch (real or dummy), 
so the server can't learn who sent a message during 
the previous epoch.
* Each client is only given the vector sum that every server holds. 
The client does not know the values that generated that sum.
Therefore, the clients cannot know who sent which message. 
* No server has access to more than 1 point,
so it cannot learn what is the message.

#### Limitations
* Each server knows exactly which clients are connected to it.
    * Onion routing can be used to separate the servers from the clients
    so that the servers wont even know who is connected to it.
* An eavesdropper can read the messages being sent and may be able
to know who sent the message.
    * All traffic can be encrypted in such a way that 
the eavesdropper gets no information from viewing the ciphertext.


### Claim for liveness
Regardless as to what the malicious server does, the system is live.
#### Proof
Every epoch each client sends a message and every epoch the 
clients receive at least three parts of all of the messages. 
Therefore, there is no stage where liveness can be broken. 
