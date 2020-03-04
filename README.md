# Rate Limitation Implementation
### Problem
Dcard 每天午夜都有大量使用者湧入抽卡，為了不讓伺服器過載，請設計一個 middleware：
- 限制每小時來自同一個 IP 的請求數量不得超過 1000
- 在 response headers 中加入剩餘的請求數量 (X-RateLimit-Remaining) 以及 rate limit 歸零的時間 (X-RateLimit-Reset)
- 如果超過限制的話就回傳 429 (Too Many Requests)
- 可以使用各種資料庫達成

### How to Run
Start with docker:
```
cd Rate-limitation
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
