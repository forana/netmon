# netmon

This is a dirt-simple, made and deployed in 20 minutes, network-checking script that I run on a Raspberry PI-based kubernetes cluster in my basement to track how often our internet goes down (it's a lot). Done super naively right now (timeseries data in an sqlite db on a hostPath volume - yikes!)- might revisit someday, but it works for now.

[k8s.yml](./k8s.yml) contains the _exact_ config I use on my cluster - no secrets in there. It's not very exciting.
