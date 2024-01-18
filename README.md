# ing-balance-crawler
### Python tool to read balance of ING accounts

The crawler logs in to ing via chrome browser, sends an email via gmail to notify for two-factor-authentication and logs the balance of accounts in a csv file in Dropbox.
Have a look at main.py to see which environment variables you need. Refer to Dropbox and gmail instructions to setup the necessary credentials and tokens.

Execution is automated to run as a cron job once a day via Github actions.