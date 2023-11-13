from typing import List, Any, Dict

import redis
from redis_lru import RedisLRU
from Conf.models import Author, Quote
from Conf.db_mongo import URI
from mongoengine import connect

connect(host=URI)
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    qoutes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in qoutes]
    return result


@cache
def find_by_tags(tags: str) -> List[str | None]:
    tag_list = tags.split(',')
    regex_pattern = '|'.join(tag_list)
    print(f"Find by tags: {tags}")
    quotes = Quote.objects(tags__iregex=regex_pattern)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> dict[Any, list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        qoutes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in qoutes]
    return result


if __name__ == "__main__":
    while True:
        command = input("Введіть команду ('tag: тег', 'author: автор', або 'exit' для виходу): ")

        if command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            print(find_by_tag(tag))
        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip()
            print(find_by_tags(tags))
        elif command.startswith("name:"):
            author = command.split(":")[1].strip()
            print(find_by_author(author))
        elif command == "exit":
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")
            continue
