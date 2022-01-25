# unbound_ad_blocker
This is basically a ad blocker it uses the [unbound](https://github.com/NLnetLabs/unbound) module "validator python iterator" where it basically hooks into unbound and intercept dns queries

### the project uses two main external modules
* [sqlite3](https://github.com/sqlite/sqlite)
* [requests](https://github.com/psf/requests)

## The project works as follows
### you have unbound compiled with --with-python
