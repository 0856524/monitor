#!/bin/bash
ssh -i cloud.key ubuntu@$1 "./delete.sh && exit"
