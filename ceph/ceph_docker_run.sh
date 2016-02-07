#!/bin/bash
docker run -d --net=host -v /etc/ceph:/etc/ceph -e MON_IP=$1 -e CEPH_NETWORK=$2 ceph-demo
