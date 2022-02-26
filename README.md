# Analytics

## Streamlit
Loads data from AWS and generates a series of reports.  
Results are cached.  


## AWS
Data is provided in S3 in a YYYY/MM/DD format.  
Each file has a JSON of information about each record.  
More than one record can be in a json file.


## Docker
Runs with the following 4 services.  
Supervisor handles the starting of each service.
- supervisor
- oauth2-proxy
- caddy
- streamlit app

External request -> caddy -> oauth2-proxy -> streamlit

### Supervisor
Handles the starting and initial health-check of each service.  
It also ensures each service starts with the correct user and environment.

### Caddy
Terminates https and redirects http. Uses on-demand certs (rate limited).  
Serves requests to oauth2-proxy.

### oauth2-proxy
Handles incoming requests from Caddy.  
Configured to only permit emails with a certain domain.