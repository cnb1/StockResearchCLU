# StockResearchCLU

This program is a python command line utility that allows for viewing stock research information.
This is done by doing multitrheaded web scraping.

- Uses multithreading to make multiple requests within an execution much faster
- Caches the currently used and last used requests with an expiration of 7 days. After 7 days it will
  grab the data again from the websites
