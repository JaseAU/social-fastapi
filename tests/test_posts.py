from typing import List
import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    #print(res.json())
    #posts = schemas.PostOut(res.json())

    def validate(post):
        return schemas.PostVote(**post)
    

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    print(posts_list)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[0].post.id == test_posts[0].id # only if order by in use.
    assert posts_list[0].post.title == test_posts[0].title
    assert posts_list[0].post.content == test_posts[0].content


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    def validatePost(post):
        return schemas.PostVote(**post)
    
    post = validatePost(res.json())
    print(post)

    assert post.post.id == test_posts[0].id
    assert post.post.title == test_posts[0].title
    assert post.post.content == test_posts[0].content
    assert res.status_code == 200
    #assert posts_list[0].Post.id == test_posts[0].id # only if order by in use.


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "This is some content of awesome", True),
    ("epic new title", "This is epic new content", False),
    ("favourite pizza", "I love pinapple", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['user_id']
    assert res.status_code == 201


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "arbitary title", "content": "arbitary content"})
    created_post = schemas.Post(**res.json())
    assert created_post.title == "arbitary title"
    assert created_post.content == "arbitary content"
    assert created_post.published == True # Creates with default true?
    assert created_post.owner_id == test_user['user_id']
    assert res.status_code == 201


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitary title", "content": "arbitary content"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/88888")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.id == test_posts[0].id
    assert updated_post.content == data['content']
    assert updated_post.title == data['title']


def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/88888", json=data)
    assert res.status_code == 404
