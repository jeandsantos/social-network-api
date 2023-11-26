from social_network_api.typings import PostType


def find_post(post_table: dict[int, PostType], post_id: int) -> PostType:
    return post_table.get(post_id)
