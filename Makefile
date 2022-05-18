NAME	:= build2022/app

all:
	docker build -t $(NAME) -f python/dockerfile .
	docker run -d -p 9000:9000 $(NAME):latest

fclean:
	-docker stop $(shell docker ps -aq)
	-docker rmi -f $(shell docker images -aq)