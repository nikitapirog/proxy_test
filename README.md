## PROXY

### hint
If you encounter an error when trying to bind to an address.

Then star locally via
    
    sudo %path/to/your/interpreter% proxy.py

For test star

    sudo %path/to/your/interpreter% -m pytest test.py

    

### start
To start the server, lift the container
    
    docker-compose up -d

### commands for checking
Get 200 status

    curl -x 0.0.0.0:80 0.0.0.0:8000 -i

Get 666 status

    curl -x 0.0.0.0:80 -H "User-Agent: Netscape" 0.0.0.0:8000 -i

### tests
Run test by this command

    pip install -r requirements.txt
    pytest test.py
