 ______    _____    _    _  ________   ________  ___  __     ________   ______    ___     _       _    ________    _    _              _      
|   ___|  |  __ |  | |  || |__   ___| |___   __| \  \/ /    |___   __| |   ___|  |  _\   | \     / |  |__   ___|  | \  | |     /\     | |     
|  |____  | |  ||  | |  ||    |  |        | |     \   /         | |    |  |____  | |/ )  |  \   /  |     |  |     |  \ | |    /  \    | |     
|   ____| | |  ||  | |  ||    |  |        | |      \ /          | |    |   ____| |   /   | \ \ / / |     |  |     | \ \| |   / /\ \   | |     
|  |___   | |__\ \ | |__||  __|  |__      | |      | |          | |    |  |___   | ||\   |  \ V /  |   __|  |__   |  \   |  / /__\ \  | |____ 
|______|  |_____\_\|_____| |________|     |_|      |_|          |_|    |______|  |_||_\  |__|\_/|__|  |________|  |__|\__| /_/    \_\ |______|


This program is a python command line utility that allows for viewing stock research information.
This is done by doing multitrheaded web scraping.

- Uses multithreading to make multiple requests within an execution much faster
- Caches the currently used and last used requests with an expiration of 7 days. After 7 days it will
  grab the data again from the websites
