from sqlalchemy.orm import Session

from models import posts, tags


def save_posts(db: Session, company_id: int, posts_with_query: dict[str, list[posts.Post]]):
    keys_object = posts_with_query.keys()

    try:
        result_array = []
        for key in keys_object:
            tag = db.query(tags.Query).where(tags.Query.name == key and tags.Query.company_id == company_id).first()

            if tag and tag.id:
                for post in posts_with_query[key]:
                    post['tag_id'] = tag.id
                    result_array.append(posts.Post(title=post['title'], link=post['link'], label=post['label'], tag_id=post['tag_id']))
        db.add_all(result_array)

    except ExceptionGroup as e:
        print(e)




