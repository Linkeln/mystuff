from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = 'uploads'

        if not os.path.exists(self.app.config['UPLOAD_FOLDER']):
            os.makedirs(self.app.config['UPLOAD_FOLDER'])

        self.notification_service = NotificationService()
        self.auth_service = AuthService(self.app)
        self.blog_service = BlogService(self.app)
        self.post_service = PostService(self.app)
        self.user_service = UserService(self.app, self.notification_service, self.post_service)
        self.comment_service = CommentService(self.app)
        self.reaction_service = ReactionService(self.app)
        self.subscription_service = SubscriptionService(self.app)
        self.tag_service = TagService(self.app, self.post_service)
        self.service_type = ServiceType(self.app)
        self.message_service = MessageService(self.app)

        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/login', 'login', self.auth_service.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/register', 'register', self.auth_service.register, methods=['GET', 'POST'])
        self.app.add_url_rule('/main_page', 'main_page', self.user_service.main_page)
        self.app.add_url_rule('/popular', 'popular', self.post_service.popular)
        self.app.add_url_rule('/my_feed', 'my_feed', self.post_service.my_feed)
        self.app.add_url_rule('/subscriptions', 'subscriptions', self.subscription_service.subscriptions)
        self.app.add_url_rule('/tags', 'tags', self.tag_service.tags)
        self.app.add_url_rule('/tag/<tag_name>', 'tag_posts', self.tag_service.tag_posts)
        self.app.add_url_rule('/services', 'services', self.service_type.services)
        self.app.add_url_rule('/service/<service_name>', 'service_detail', self.service_type.service_detail)
        self.app.add_url_rule('/add_comment/<int:post_id>', 'add_comment', self.comment_service.add_comment, methods=['POST'])
        self.app.add_url_rule('/add_reaction/<int:post_id>', 'add_reaction', self.reaction_service.add_reaction, methods=['POST'])
        self.app.add_url_rule('/guest', 'guest', self.user_service.guest)
        self.app.add_url_rule('/edit_profile', 'edit_profile', self.user_service.edit_profile, methods=['GET', 'POST'])
        self.app.add_url_rule('/create_blog', 'create_blog', self.blog_service.create_blog, methods=['GET', 'POST'])
        self.app.add_url_rule('/create_post', 'create_post', self.post_service.create_post, methods=['GET', 'POST'])
        self.app.add_url_rule('/get_notifications', 'get_notifications', self.notification_service.get_notifications, methods=['GET'])
        self.app.add_url_rule('/profile', 'profile', self.user_service.profile)
        self.app.add_url_rule('/profile/<username>', 'user_profile', self.user_service.user_profile)
        self.app.add_url_rule('/subscribe/<username>', 'subscribe', self.subscription_service.subscribe)
        self.app.add_url_rule('/send_message/<username>', 'send_message', self.message_service.send_message, methods=['POST'])
        self.app.add_url_rule('/search', 'search', self.search)

    def index(self):
        return redirect(url_for('login'))

    def search(self):
        query = request.args.get('query')
        # Здесь можно добавить логику для поиска постов, пользователей и т.д.
        # В данном примере мы просто вернем строку поиска
        return render_template('search_results.html', query=query)

    def run(self):
        self.app.run(debug=True)

class NotificationService:
    def __init__(self):
        self.notifications = []

    def add_notification(self, message):
        self.notifications.append({"message": message})

    def get_notifications(self):
        return jsonify(self.notifications)

class AuthService:
    def __init__(self, app):
        self.app = app

    def login(self):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            return redirect(url_for('main_page'))
        return render_template('login.html')

    def register(self):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            username = request.form['username']
            info = request.form['info']
            photo = request.files['photo']
            if photo:
                photo.save(os.path.join(self.app.config['UPLOAD_FOLDER'], photo.filename))
            return redirect(url_for('main_page'))
        return render_template('register.html')

class BlogService:
    def __init__(self, app):
        self.app = app

    def create_blog(self):
        if request.method == 'POST':
            blog_name = request.form['blog_name']
            blog_description = request.form['blog_description']
            blog_service_type = request.form['blog_service_type']
            blog_photo = request.files['blog_photo']
            if blog_photo:
                blog_photo.save(os.path.join(self.app.config['UPLOAD_FOLDER'], blog_photo.filename))
            return redirect(url_for('main_page'))
        return render_template('create_blog.html')

class PostService:
    def __init__(self, app):
        self.app = app
        self.popular_posts = [
            {
                "id": 1,
                "title": "Пост 1",
                "content": "Это содержимое первого поста.",
                "author": "Автор 1",
                "date": "2023-10-01",
                "comments": [
                    {"author": "Комментатор 1", "text": "Это комментарий 1."},
                    {"author": "Комментатор 2", "text": "Это комментарий 2."}
                ],
                "reactions": 5,
                "tags": ["еда"]
            },
            {
                "id": 2,
                "title": "Пост 2",
                "content": "Это содержимое второго поста.",
                "author": "Автор 2",
                "date": "2023-10-02",
                "comments": [
                    {"author": "Комментатор 3", "text": "Это комментарий 3."}
                ],
                "reactions": 3,
                "tags": ["спорт"]
            }
        ]
        self.my_feed_posts = [
            {
                "id": 3,
                "title": "Пост 3",
                "content": "Это содержимое третьего поста.",
                "author": "Автор 3",
                "date": "2023-10-03",
                "comments": [
                    {"author": "Комментатор 4", "text": "Это комментарий 4."}
                ],
                "reactions": 2,
                "tags": ["кино"]
            },
            {
                "id": 4,
                "title": "Пост 4",
                "content": "Это содержимое четвертого поста.",
                "author": "Автор 4",
                "date": "2023-10-04",
                "comments": [
                    {"author": "Комментатор 5", "text": "Это комментарий 5."},
                    {"author": "Комментатор 6", "text": "Это комментарий 6."}
                ],
                "reactions": 4,
                "tags": ["еда", "спорт"]
            }
        ]

    def popular(self):
        return render_template('popular.html', posts=self.popular_posts)

    def my_feed(self):
        return render_template('my_feed.html', posts=self.my_feed_posts)

    def create_post(self):
        if request.method == 'POST':
            post_title = request.form['post_title']
            post_content = request.form['post_content']
            post_tags = request.form['post_tags']
            post_photos = request.files.getlist('post_photos')
            for photo in post_photos:
                if photo:
                    photo.save(os.path.join(self.app.config['UPLOAD_FOLDER'], photo.filename))
            return redirect(url_for('main_page'))
        return render_template('create_post.html')

class UserService:
    def __init__(self, app, notification_service, post_service):
        self.app = app
        self.notification_service = notification_service
        self.post_service = post_service

    def main_page(self):
        notifications = self.notification_service.get_notifications()
        return render_template('main_page.html', notifications=notifications)

    def guest(self):
        return redirect(url_for('main_page'))

    def edit_profile(self):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            username = request.form['username']
            info = request.form['info']
            photo = request.files['photo']
            if photo:
                photo.save(os.path.join(self.app.config['UPLOAD_FOLDER'], photo.filename))
            return redirect(url_for('main_page'))
        return render_template('edit_profile.html')

    def profile(self):
        return render_template('profile.html')

    def user_profile(self, username):
        # Здесь можно добавить логику для получения постов конкретного пользователя
        user_posts = [post for post in self.post_service.popular_posts + self.post_service.my_feed_posts if post['author'] == username]
        return render_template('user_profile.html', username=username, posts=user_posts)

class CommentService:
    def __init__(self, app):
        self.app = app

    def add_comment(self, post_id):
        comment_text = request.form['comment_text']
        comment_author = request.form['comment_author']
        # Здесь можно добавить логику для сохранения комментария в базе данных
        return redirect(request.referrer)

class ReactionService:
    def __init__(self, app):
        self.app = app

    def add_reaction(self, post_id):
        reaction = request.form['reaction']
        # Здесь можно добавить логику для сохранения реакции в базе данных
        return redirect(request.referrer)

class SubscriptionService:
    def __init__(self, app):
        self.app = app
        self.subscriptions_list = [
            {"username": "Пользователь 1"},
            {"username": "Пользователь 2"},
            {"username": "Пользователь 3"},
            {"username": "Пользователь 4"}
        ]

    def subscriptions(self):
        return render_template('subscriptions.html', subscriptions=self.subscriptions_list)

    def subscribe(self, username):
        # Здесь можно добавить логику для подписки на пользователя
        return redirect(url_for('user_profile', username=username))

class TagService:
    def __init__(self, app, post_service):
        self.app = app
        self.post_service = post_service
        self.tags_list = [
            {"name": "еда", "posts": [post for post in self.post_service.popular_posts + self.post_service.my_feed_posts if "еда" in post["tags"]]},
            {"name": "спорт", "posts": [post for post in self.post_service.popular_posts + self.post_service.my_feed_posts if "спорт" in post["tags"]]},
            {"name": "кино", "posts": [post for post in self.post_service.popular_posts + self.post_service.my_feed_posts if "кино" in post["tags"]]}
        ]

    def tags(self):
        return render_template('tags.html', tags=self.tags_list)

    def tag_posts(self, tag_name):
        tag_posts = [post for post in self.post_service.popular_posts + self.post_service.my_feed_posts if tag_name in post["tags"]]
        return render_template('tag_posts.html', posts=tag_posts, tag_name=tag_name)

class ServiceType:
    def __init__(self, app):
        self.app = app
        self.services_list = [
            {
                "name": "Блог о еде",
                "theme": "Еда",
                "subscribers": 1500
            },
            {
                "name": "Блог о спорте",
                "theme": "Спорт",
                "subscribers": 2000
            },
            {
                "name": "Блог о кино",
                "theme": "Кино",
                "subscribers": 1200
            }
        ]

    def services(self):
        return render_template('services.html', services=self.services_list)

    def service_detail(self, service_name):
        service = next((s for s in self.services_list if s["name"] == service_name), None)
        if service:
            return render_template('service_detail.html', service=service)
        else:
            return "Блог не найден", 404

class MessageService:
    def __init__(self, app):
        self.app = app

    def send_message(self, username):
        message_text = request.form['message_text']
        # Здесь можно добавить логику для сохранения сообщения в базе данных
        return redirect(url_for('user_profile', username=username))

if __name__ == '__main__':
    app = App()
    app.run()
