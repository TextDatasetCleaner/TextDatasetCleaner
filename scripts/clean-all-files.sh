#!/bin/sh

ls -p /tdc/input/ | grep -v / | xargs -I{} tdc -c /tdc/config.yml -i /tdc/input/{} -o /tdc/output/{}
