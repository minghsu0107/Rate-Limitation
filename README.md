# Rate Limitation Implementation
### How to Run
Start with docker:
```
cd rate_limitation
docker-compose up
```
Next, browse http://127.0.0.1/ with your web browser. You can see a response like this:
![](https://i.imgur.com/JFgXnZH.png)


If your api rate limit exceeds, your request will be limited:
![](https://i.imgur.com/7GcuDrI.png)
### Testing
```
docker exec -it api-container python manage.py test
```
### Project Structure
I choose Redis as the database for saving states of requests from each IP (IP as the key). The state of an IP is presented as an object and hashed in the database, as shown below.
```python
{'reset_at': 1583264306, 'current': 15}
```
`reset_at` is the timestamp that this key entry expires, and `current` is the current accumulated number of requests from an IP.

In addition, I use Nginx as the reverse proxy for the API service. Thus, in order to get client's real IP, we must define X-Forwarded-For and X-Real-IP in the header in Nginx before passing requests to the api server.