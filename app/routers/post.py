from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, sessionmaker, query
from sqlalchemy import func
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", status_code=status.HTTP_200_OK)
#@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, searchTitle: Optional[str] = ""):
    #    cursor.execute("""SELECT * FROM fapisysdb.posts""")
    #    posts = cursor.fetchall()
    #    return {"data": posts}
    print(f"Search: {searchTitle}")
    #posts = db.query(models.Post).filter(models.Post.title.contains(
    #    searchTitle)).limit(limit).offset(skip).all()
    #posts = db.query(models.Post, func.count(models.Vote.post_id).label("vote_cnt")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.title.contains(searchTitle)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, 
                     func.count(models.Vote.post_id).label("vote_cnt") # type: ignore
                     ).join(models.Vote, models.Post.id == models.Vote.post_id, isouter= True
                                 ).group_by(models.Post.id
                                            ).filter(models.Post.title.contains(searchTitle)).limit(limit).offset(skip).all()
        #print(posts)
    #print(posts_votes)
    # post_unique = db.query(models.Post).filter(models.Post.owner_id == current_user.userid).all()
    results = [{"post": p, "vote_cnt": v} for p, v in posts]
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #    cursor.execute("""INSERT INTO fapisysdb.posts (title, content, published)
    #                   VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #    new_post = cursor.fetchone()
    #    conn.commit()
    new_post = models.Post(owner_id=current_user.user_id, **post.model_dump())
#        title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # fetch what was committed into our variable

    return new_post


@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = find_post(int(id))
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, 
                     func.count(models.Vote.post_id).label("vote_cnt") # type: ignore
                     ).join(models.Vote, models.Post.id == models.Vote.post_id, isouter= True
                                 ).group_by(models.Post.id
                                            ).filter(models.Post.id == id
                                                     ).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")

    #return post
    results = {"post": post[0], "vote_cnt": post[1]}
    return results


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post_idx = find_post_index(int(id))
    # post_exists = find_post_exists(int(id))
    # if post_idx == None:
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")

    if post.owner_id != current_user.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f"Post with id: {id} can't be deleted by this user {current_user.user_id}")

    post_query.delete(synchronize_session=False)
    db.commit()
    # db.refresh(post)

    # cursor.execute("""DELETE FROM fapisysdb.posts
    #               WHERE id = %s
    #               RETURNING *
    #               """,
    #               (str(id),))
    # db_resp = cursor.fetchall()
    # conn.commit()
    # Don't send data back when a 204 is returned.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, upd_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post_idx = find_post_index(int(id))
    # post_exists = find_post_exists(int(id))
    # if post_idx == None:
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")
    post.update(upd_post.model_dump(), synchronize_session=False)
    db.commit()

    # post_dict = post.model_dump()
    # cursor.execute("""UPDATE fapisysdb.posts (title, content, published)
    #               SET title = %s,
    #                   content = %s,
    #                   published = %s
    #               WHERE id = %s
    #               RETURNING *
    #               """,
    #               (post.title, post.content, post.published, (str(id),)))
    # db_resp = cursor.fetchall()
    # conn.commit()
    # post_dict['id'] = id  # override the id?
    # Update the dictionary to the updated post.
    # my_posts[post_idx] = post_dict
    # return {"message": "Updated Post"}
    return post.first()
