#!/bin/bash
ssh -i cloud.key ubuntu@$1 "/home/ubuntu/monitor/monitor-instance/delete.sh && exit"
