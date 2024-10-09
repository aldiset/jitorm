import json
from faker import Faker
import random

fake = Faker()

# Menghasilkan data dummy untuk Users
def generate_users(n):
    users = []
    for _ in range(n):
        users.append({
            "id": _ + 1,
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(),
            "biography": fake.text(max_nb_chars=200)
        })
    return users

# Menghasilkan data dummy untuk Followers
def generate_followers(n, user_ids):
    followers = []
    for _ in range(n):
        user_id = random.choice(user_ids)
        follower_id = random.choice([id_ for id_ in user_ids if id_ != user_id])
        followers.append({
            "id": _ + 1,
            "user_id": user_id,
            "follower_id": follower_id
        })
    return followers

# Menghasilkan data dummy untuk Posts
def generate_posts(n, user_ids):
    posts = []
    for _ in range(n):
        posts.append({
            "id": _ + 1,
            "user_id": random.choice(user_ids),
            "content": fake.text(max_nb_chars=300),
            "image_url": fake.image_url()
        })
    return posts

# Menghasilkan data dummy untuk Likes
def generate_likes(n, post_ids, user_ids):
    likes = []
    for _ in range(n):
        likes.append({
            "id": _ + 1,
            "post_id": random.choice(post_ids),
            "user_id": random.choice(user_ids)
        })
    return likes

# Menghasilkan data dummy untuk Comments
def generate_comments(n, post_ids, user_ids):
    comments = []
    for _ in range(n):
        comments.append({
            "id": _ + 1,
            "post_id": random.choice(post_ids),
            "user_id": random.choice(user_ids),
            "comment": fake.text(max_nb_chars=200)
        })
    return comments

# Fungsi utama untuk generate dan simpan data ke JSON
def generate_data_to_json():
    user_count = 1000  # Jumlah users
    post_count = 20000  # Jumlah posts
    followers_count = 15000  # Jumlah followers
    likes_count = 50000  # Jumlah likes
    comments_count = 4000  # Jumlah comments

    users = generate_users(user_count)
    user_ids = [user["id"] for user in users]

    posts = generate_posts(post_count, user_ids)
    post_ids = [post["id"] for post in posts]

    followers = generate_followers(followers_count, user_ids)
    likes = generate_likes(likes_count, post_ids, user_ids)
    comments = generate_comments(comments_count, post_ids, user_ids)

    # Gabungkan semua data
    data = {
        "users": users,
        "followers": followers,
        "posts": posts,
        "likes": likes,
        "comments": comments
    }

    # Simpan ke file JSON
    with open('dummy.json', 'w') as f:
        json.dump(data, f, indent=4)

    print("Data dummy berhasil disimpan ke dummy_social_media_data.json")

if __name__ == "__main__":
    generate_data_to_json()
