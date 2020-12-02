#!/bin/bash
ps aux | grep RPC_Consumer | awk '{print $2}' | xargs kill -9
exit

