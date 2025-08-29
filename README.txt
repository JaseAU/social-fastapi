# Installs needed.
# PostgreSQL
# https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database
# PGADMIN (WIndows - Don't install in WSL)
# https://www.postgresql.org/ftp/pgadmin/pgadmin4/v9.7/windows/
# 


# Password for Postgres is postgresdefault




# Posts table copy
# -- Table: fapisysdb.posts

-- DROP TABLE IF EXISTS fapisysdb.posts;

CREATE TABLE IF NOT EXISTS fapisysdb.posts
(
    id integer NOT NULL DEFAULT nextval('fapisysdb.posts_id_seq'::regclass),
    title character varying COLLATE pg_catalog."default" NOT NULL,
    content character varying COLLATE pg_catalog."default" NOT NULL,
    published boolean NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT posts_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fapisysdb.posts
    OWNER to postgres;





select * from fapisysdb.votes;
select * from fapisysdb.users;
select * from fapisysdb.posts;
select p.*, u.user_id from fapisysdb.posts p, fapisysdb.users u
where p.owner_id = u.user_id;

select fapisysdb.users.user_id, count(*)
FROM fapisysdb.POSTS RIGHT JOIN fapisysdb.USERS
ON posts.owner_id = users.user_id
GROUP BY user_id

select users.user_id, users.email, COUNT(posts.id) as user_post_count
FROM fapisysdb.POSTS RIGHT JOIN fapisysdb.USERS
ON posts.owner_id = users.user_id
GROUP BY user_id

select posts.*, count(votes.voter_id) as vote_cnt
from fapisysdb.posts LEFT JOIN fapisysdb.votes
ON posts.id = votes.post_id
GROUP BY posts.id