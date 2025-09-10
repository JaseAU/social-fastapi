import pytest
from app import models

@pytest.fixture(scope="function")
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, voter_id=test_user['user_id'])
    #models.Vote(post_id=vote.post_id, voter_id=current_user.user_id)
    #new_vote = {"post_id": test_posts[3].id, "updown": 1}
    #new_vote_v = models.Vote(new_vote)
    session.add(new_vote)
    session.commit()
    

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "updown": 1})
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "updown": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "updown": 0})
    assert res.status_code == 201

def test_delete_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "updown": 0})
    assert res.status_code == 409


def test_vote_post_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 80000, "updown": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "updown": 1})
    assert res.status_code == 401