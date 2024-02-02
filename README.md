
# Command and Control (C2) Program
Cole Cirillo
cac2107@rit.edu
## Features

  

- Use the help command in pycontrol.py to see all features.

### list-connected
Prints all connected devices with their corresponding integer id. You can use the id to send commands specifically to that machine.

### clear-command-queue
This will clear the queued commands for every machine. However, you must use it before the next get request is received.

### list-cmd-queue
This will list all currently queued commands.

### set-interval &lt;int&gt;
This will set the time interval that the target computer sends out get requests. By default, it is 10 seconds.

### set-buffer &lt;int&gt;
This sets the buffer for time intervals between get requests for randomization. For example, if the time interval is 10 seconds and the buffer is 2 seconds, the target computer will send out a get request at a random interval to the 100th place between 8 and 12 seconds (10 plus/minus 2).

### cd, ls, mkdir &lt;name&gt;, pwd
All work as you would expect them to.

### get-users
WINDOWS ONLY. This will print all active directory users, groups, and names. Assuming that the target computer is connected to an AD domain.

### powershell &lt;cmd&gt;
WINDOWS ONLY. This will run the given powershell command. However, if you need to run multiple at once, use this command like this: `powershell &lt;cmd&gt;; &lt;cmd&gt;; &lt;cmd&gt;;` You can add as many cmds as you would like.

### scan-ports &lt;min&gt; &lt;max&gt;
This will find all open ports within the specified range on the target computer.

### keylogger
WINDOWS ONLY. This starts the keylogger. It will send a report after 128 characters have been typed. It stores it in a log file named as “&lt;mac address&gt;.log”. It will also print in the server that it has received a report.

### kill-keylogger
WINDOWS ONLY. This will kill the keylogger. Since the keylogger is running on a different thread than the main command handler on the target computer, the keylogger will send one more report, and the reply to the report gives it the command to end the thread. Therefore, it is not an instantaneous ending of the keylogger.

### screenshot
This will take a screenshot of the target computer’s screen and save it to the uploads folder. Ensure that there is an uploads folder in the directory of the server as I did not set up handling for there being no folder. I also botched the encryption for this so it takes 5+ seconds to decrypt.

### screenshot &lt;interval&gt; &lt;quantity&gt;
This parameterized version of the screenshot command will continually take screenshots every interval of seconds for a total of quantity times.

### audio-record &lt;seconds&gt;
WINDOWS ONLY. Will record audio for *seconds* seconds. Current bug: If a microphone is plugged into target machine after payload has already been started, this function will not work.

### downloader &lt;path&gt; &lt;filename&gt;
This will download a file from the target computer to the uploads folder.

### get-processes &lt;process name&gt;
This will get all processes that are running on the target computer. The process name parameter is optional. If you choose to use it, it will find all processes with the given name. It kind of works like a search function, so, for example, if you just provide a process name of “e” it will return all processes that contain the letter “e”.

### kill &lt;pid&gt;
This will kill the process with the associated pid.

### kill-by-name &lt;process name&gt;
This will kill all processes with the associated name. Be careful as it also works like the search function described in get-processes. It is useful for processes that have numerous pids. For example, chrome always has a million processes running, so if you were to provide a process name of chrome.exe, all instances of chrome will close.

### repeat-kill-proc &lt;process name&gt; &lt;reps&gt; &lt;sleep time&gt;
This will continually repeat the kill-by-name command for reps repetitions with a pause interval of sleep time. I decided to not allow it to just go infinitely as there is no easy way to end the thread that kills the processes.

### get-all-services &lt;r?&gt;
This will return all services on the target computer. Make the command `get-all-services r` if you only want to see running services.

### stop-service &lt;service name&gt;
This will stop the service of service name. On windows (and likely linux; I have not verified), you need administrative privileges to do so.

### ip-add &lt;ip&gt;
This will add an ip to the ip pool. Currently, if the target computer fails to connect to the main server 3 times in a row, it will try a different ip in the pool.

### ANY COMMAND
If you do not use one of the commands listed, and just give it a regular terminal command, it will attempt to execute it on the target computer.



  

## Table of Contents

  

- [Installation](#installation)

- [Configuration](#configuration)

  

## Installation

  

pip install requirements.txt

  

## Configuration

First, Configure constants.py to the correct ip address.

You can use the payloadgen.py to generate a payload with the libraries that you want. From there, use autopytoexe to turn that generated file into an exe.

You can then drop that exe on the victim computer and start it.

Start pycontrol.py on the server computer.

  

Alternatively, for testing, you can just put all of these files on both computers (or even just one). Start the pycontrol.py, and then start the main_command.py

  

## Notes

The keylogger was taken from another github repository (https://github.com/secureyourself7/python-keylogger/blob/master/logger%20-%20light.py) and slightly modified for efficiency with this prorgram.