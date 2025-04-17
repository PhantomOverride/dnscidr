# dnscidr

Ever had a bunch of hostnames, but you only wanted those that mapped to a particular network? Well this is the utility for you!

Given a file with a list of domains in it, this utility will attempt to resolve every domain, and write it to the output file if the resolved IP address belongs to the supplied CIDR(s).


```
% python dnscidr.py
usage: dnscidr.py [-h] -i INPUT -o OUTPUT networks [networks ...]
```
