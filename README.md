# unbound_ad_blocker
This is basically a ad blocker it uses the [unbound](https://github.com/NLnetLabs/unbound) module "validator python iterator" where it basically hooks into unbound and intercept dns queries

### the project uses two main external modules
* [sqlite3](https://github.com/sqlite/sqlite)
* [requests](https://github.com/psf/requests)

### The project works as follows
You have unbound compiled with --with-python
You cloned the repositor to /usr/local/etc/unbound/
You will then run /usr/local/etc/unbound/blocker/bootstrap.py to create the sqllite3 database with around 7Milion domains to block
Please know that this will cause unwanted blocks for example you won't be able to go to stackoverflow.com so white list it!
you can whitelist a domain as follows i did not bother to write an interface for this yet, and most likely will not
this is not pi-hole!

## Whitelisting!
```
$ sqlite3 /usr/local/unbound/blocker/etc/database.db "INSERT INTO whitelist (tld, lenght, domain) VALUES ('com', 17, 'stackoverflow.com')";
```
now stackoverflow is whitelisted enjoy your skid ripping routines!

## Blacklisting!
```
$ sqlite3 /usr/local/unbound/blocker/etc/database.db "INSERT INTO blacklist (tld, lenght, domain) VALUES ('com', 16, 'www.facebook.com')";

```
## Regexes
The project also uses regex these paterns can be modified in the following file 
```
vim /usr/local/etc/unbound/blocker/etc/paterns.txt
```

## Configuration! chose your lists!
You can remove and add lists to the bootstrapping process in the following json config!
```
vim /usr/local/unbound/blocker/etc/config.json
