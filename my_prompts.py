def get_comment_to_post_prompt(post):
    return f"""
        This is a reddit post: 
        ---
        Post Title: {post.title}
        Post Text: {post.selftext}
        --- 

        I need you to comment on this post.

        You are free to make grammatical errors in 1 or 2 places so that it seems as if a human wrote it.

        You need to provide real value with this comment. If the answer can be short, write a short answer. If not, write a lengthy one with lots of effort in it.
        If you feel like a few sentences answer the question, just stop.

        IMPORTANT: Directly answer the question, don't fool around at the beginning with something like "Hey there, great question" etc. Be serious about it.

        Don't try to make the comment look too perfect, you can structure it sometimes but sometimes leave it without paragraphs. Your chioice.

        You should contradict the author of the post if what they say is not true, or doesn't make sense.

        Go:
        """