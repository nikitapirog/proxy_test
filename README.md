## PROXY

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
