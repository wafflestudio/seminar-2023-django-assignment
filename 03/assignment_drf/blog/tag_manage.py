from .models import Tag, Post, Comment

def postCreateNewTag(texts, post):
    if texts:
        tags = [tag.strip() for tag in texts.split(",")]
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(content=tag)
            post.tagPost.add(tag)

def postUpdateTag(texts, post):
    old_tags = [old_tag.content for old_tag in post.tagPost.filter(post=post)]
    update_tags = []
    if texts:
        tags = [tag.strip() for tag in texts.split(",")]
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(content=tag)
            update_tags.append(tag.content)
    for old_tag in old_tags:
        if old_tag not in update_tags:
            tag = Tag.objects.get(content=old_tag)
            post.tagPost.remove(tag)
            if not Post.objects.filter(tags__content=old_tag).exists():
                Tag.objects.get(content=old_tag).delete()
    for update_tag in update_tags:
        if update_tag not in old_tags:
            post.tagPost.add(Tag.objects.get(content=update_tag))

def DeleteTag():
    post_tags = [tag.content for tag in Tag.objects.all()]
    for post_tag in post_tags:
        if not ((Post.objects.filter(tags__content=post_tag).exists()) or (Comment.objects.filter(tags__content=post_tag).exists())):
            Tag.objects.get(content=post_tag).delete()

def commentCreateNewTag(texts, comment):
    if texts:
        tags = [tag.strip() for tag in texts.split(",")]
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(content=tag)
            comment.tagComment.add(tag)

def commentUpdateTag(texts, comment):
    old_tags = [old_tag.content for old_tag in comment.tagComment.filter(comment=comment)]
    update_tags = []
    if texts:
        tags = [tag.strip() for tag in texts.split(",")]
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(content=tag)
            update_tags.append(tag.content)
    for old_tag in old_tags:
        if old_tag not in update_tags:
            tag = Tag.objects.get(content=old_tag)
            comment.tagComment.remove(tag)
            if not Comment.objects.filter(tags__content=old_tag).exists():
                Tag.objects.get(content=old_tag).delete()
    for update_tag in update_tags:
        if update_tag not in old_tags:
            comment.tagComment.add(Tag.objects.get(content=update_tag))
