curl.exe -X POST -d "username=administrator" -d "password=administrator" -G http://192.168.0.105/authorize/login -c cookie.txt
curl.exe -X PUT http://192.168.0.105/kas/state?newstate=started -b cookie.txt
