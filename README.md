# Proton captcha documented & solved
This repository contains files that will make solving Proton captchas simple. This solver worked on
**July 10th 2023**. It is possible that something in Proton's security has changed since then. It is possible for this solver to be flagging,
although I am not sure if Proton has a trust score system.

## How Proton captcha works
Proton captcha is a custom captcha only used for the [proton.me](https://proton.me/) website. At the time of uploading this repo
the captcha is being used interchangeably with HCaptcha. You can see it in both signup and login.
The captcha itself doesn't collect much user information. The main challenges are the proof of work and image challenge.

## clientData parameter
The clientData parameter is an (AES?) encrypted list of mouse movements (grabbed every second) and mouse clicks.
This could be one of the harder parts in this challenge, only if it was required. Turns out you can just pass null as the clientData parameter
and avoid getting flagged that way. You cannot do this with any other parameter in the payload.

## How to try this and continue development?
All the required files are in this repository. The `pow` directory stands for **proof of work** and contains files
that are made to solve that challenge. The proof of work part of this solver is written in Rust to make the sovler faster.
During testing the solver in Rust was about 5x faster than the one in node or browser JavaScript.
In the folder you can find the main file (works as an api) and the dependencies you need to compile it.
If you don't want to put up with all the compiling stuff you can just use the ready binary I compiled myself.
This binary will only work on Linux though. As for continuing development... there's not much that's changing in this captcha so chances are you won't have to :)