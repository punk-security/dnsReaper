$ORIGIN punksecurity.io.
@	3600	IN	SOA	punksecurity.io. root.punksecurity.io. 2041230773 7200 3600 86400 3600
        IN      NS      ns1.localhost.net.

;; NS Records
vulnerable 1	IN	NS	ns-40.awsdns-05.com.
cname 1 IN CNAME kfsdjlf8324n23jkhsdf.github.io.
relcname 1 IN CNAME cname

ayy 1 IN A 10.10.10.10
relayy 1 IN CNAME ayy

recursive1 1 IN CNAME relcname
recursive2 1 IN CNAME recursive1
recursive3 1 IN CNAME recursive2
recursive4 1 IN CNAME recursive3
recursive5 1 IN CNAME recursive4
recursive6 1 IN CNAME recursive5

circular1 1 IN CNAME circular2
circular2 1 IN CNAME circular3
circular3 1 IN CNAME circular4
circular4 1 IN CNAME circular5
circular5 1 IN CNAME circular1
