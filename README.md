# unbound_ad_blocker
This is basically a ad blocker it uses the [unbound](https://github.com/NLnetLabs/unbound) module "validator python iterator" where it basically hooks into unbound and intercept dns queries

### the project uses two main external modules
* [sqlite3](https://github.com/sqlite/sqlite)
* [requests](https://github.com/psf/requests)

### The project works as follows
you have unbound compiled with --with-python
you cloned the repositor to /usr/local/etc/unbound/
you will then run /usr/local/etc/unbound/blocker/bootstrap.py to create the sqllite3 database with around 6k domains to block
Please know that this will cause unwanted blocks for example you won't be able to go to stackoverflow.com so white list it!
you can whitelist a domain as follows i did not bother to write an interface for this yet, and most likely will not
this is not pi-hole!
``
$ sqlite3 /usr/local/unbound/blocker/etc/database.db "INSERT INTO whitelist (tld, lenght, domain) VALUES ('com', 17, 'stackoverflow.com')";
``
now stackoverflow is whitelisted enjoy your skid ripping routines!
the project also uses regex these paterns can be modified in the following file /usr/local/etc/unbound/blocker/etc/paterns.txt
