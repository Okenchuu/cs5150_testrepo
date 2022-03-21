import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    # 0: {
    #     "id": 0,
    #     "upvotes": 1,
    #     "title": "My cat is the cutest!",
    #     "link": "https://i.imgur.com/jseZqNK.jpg",
    #     "username": "alicia98",
    #     "comments":{
    #         0: {
    #             "id": 0,
    #             "upvotes": 8,
    #             "text": "Wow, my first Reddit gold!",
    #             "username": "alicia98",
    #         }
    #     }
    # },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98",
        "comments":{}
    }
}

comment_id_counter = 1
post_id_counter = 2

@app.route("/")
def hello_world():
    return "Hello world!"


@app.route("/api/posts/", methods=["GET"]) 
def get_tasks():
    """Get All Posts"""
    result = {"posts": list(posts.values())}
    return json.dumps(result), 200


@app.route("/api/posts/", methods=["POST"])
def create_task():
    """Create new post"""
    global post_id_counter
    body = json.loads(request.data)
    title = body.get("title")
    link = body.get("link")
    username = body.get("username")
    if not title or not link or not username: 
        return json.dumps({"error": "Missing fields in the body"}), 400
    post = {
        "id": post_id_counter,
        "upvotes": 1,
        "title": title,
        "link": link,
        "username": username,
        "comments": {}
        }
    posts[post_id_counter] = post
    post_id_counter += 1
    return json.dumps(post), 201


@app.route("/api/posts/<int:post_id>/", methods=["GET"])
def get_specific_post(post_id):
    """Get specific post"""
    value = posts.get(post_id)
    if not value: 
        return json.dumps({"error": "Post Not Found"}), 404
    return json.dumps(value), 200


@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    """Delete specific post"""
    post = posts.get(post_id)
    if not post: return json.dumps({"error": "Post Not Found"}), 404
    del posts[post_id]
    return json.dumps(post), 200


@app.route("/api/posts/<int:post_id>/comments/", methods=["GET"])
def get_comments(post_id):
    """Get comments for a specific post"""
    post = posts.get(post_id)
    if not post: 
        return json.dumps({"error": "Post Not Found"}), 404
    comments = post.get("comments")
    result = {"comments": list(comments.values())}
    return json.dumps(result), 200

@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def post_comments(post_id):
    """Create a new comment for a specific post"""
    global comment_id_counter
    post = posts.get(post_id)
    if not post: 
        return json.dumps({"error": "Post Not Found"}), 404
    comments = post["comments"]
    body = json.loads(request.data)
    if not body:
        return json.dumps({"error": "Input value invalid"}), 400
    text = body.get("text")
    username = body.get("username")
    if not text or not username: 
        return json.dumps({"error": "Missing fields in the body"}), 400
    comment = {
        "id": comment_id_counter,
        "upvotes": 1,
        "text": text,
        "username": username,
        }
    comments[comment_id_counter] = comment
    comment_id_counter += 1
    return json.dumps(comment), 201
    
@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def edit_comment(post_id, comment_id):
    """Edit a comment from a specific post"""
    post = posts.get(post_id)
    if not post: 
        return json.dumps({"error": "Post Not Found"}), 404
    comments = post["comments"]
    comment = comments.get(comment_id)
    if not comment: 
        return json.dumps({"error": "Comment Not Found"}), 404
    body = json.loads(request.data)
    text = body.get("text")
    if not text: 
        return json.dumps({"error": "Missing fields in the body"}), 400
    comment["text"] = text
    return json.dumps(comment), 200


    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
