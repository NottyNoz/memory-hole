# memory-hole
There's no good reason to archive everything that's ever been said.

This cog will make your redbot continuously and repeatedly scan every channel of every guild it's in and delete every message older than 7 days.

Every other bot I've found which can delete stuff will not delete anything older than 14 days because of how the bulk delete api works. This bot deletes messages one by one which doesn't have that limitation. It continuously runs in the background while the cog is loaded. Discord rate limits this pretty bad, so the first pass over a large guild can take days.

To install put memoryhole.py in the root redbot folder (alongside cogs/ and core/).

There is no config. Just modify the code.
