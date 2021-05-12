rm -f emoji-michigan-bot.tar emoji-michigan-bot.tar.gz
docker build . -t emoji-michigan-bot
docker image save emoji-michigan-bot:latest -o emoji-michigan-bot.tar
gzip emoji-michigan-bot.tar
ssh -i "emoji-michigan.pem" ubuntu@ec2-3-134-76-49.us-east-2.compute.amazonaws.com "./stop_containers.sh"
scp -i "emoji-michigan.pem" emoji-michigan-bot.tar.gz ubuntu@ec2-3-134-76-49.us-east-2.compute.amazonaws.com:/tmp
ssh -i "emoji-michigan.pem" ubuntu@ec2-3-134-76-49.us-east-2.compute.amazonaws.com "./start_container.sh"