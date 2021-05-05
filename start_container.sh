gunzip /tmp/emoji-michigan-bot.tar.gz 
docker image load -i /tmp/emoji-michigan-bot.tar
docker run -d --restart always emoji-michigan-bot