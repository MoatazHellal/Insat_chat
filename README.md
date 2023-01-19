# Secured chatroom and security tools 
This is an application made with python using the security package Crypto and it consists of 3 main parts:
  - Registration/Authentication
  - Security tools
  - Secured chatroom

### Registration/Authentication
- Users can make an account that will generate a ciphered token.
- When authenticating, users need to present their ciphered token in order to proceed to the application.

### Security tools
This app provides tools for various security needs such as:
  - Encoding and decoding messages in base64
  - Hashing messages with MD5, SHA-1 or SHA256
  - Symetric ciphering of messages with DES or AES256
  - Assymetric ciphering of messages with RSA or ElGamal

### Secured chatroom
- The chatroom consists of a server that stays running and clients that connect
to the server using a pair of keys and send ciphered messages to each other that are deciphered upon receiving.
