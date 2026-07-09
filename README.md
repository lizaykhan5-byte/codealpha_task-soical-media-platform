# 🌐 SocialHub – Social Media Platform
A modern full-stack social media platform built with **Django**, inspired by Instagram and Messenger. Users can create accounts, share posts and stories, chat in real-time, follow other users, and interact through likes, comments, and notifications.
---
# 🚀 Features
## 👤 Authentication
- User Registration
- Secure Login & Logout
- Password Hashing (Django Authentication)
- Profile Editing
- Profile Picture & Cover Photo
---
## 📸 Posts
- Create Post
- Edit Post
- Delete Post
- Image Upload
- Like / Unlike Posts
- Comment on Posts
- Save / Unsave Posts
- Saved Posts Page
- Share Post Link
- Post Detail View
- User Feed (shows posts from followed users)
---
## 📖 Stories
- Upload Stories
- Multiple Stories
- Story Progress Bar
- Auto Next Story
- Previous / Next Story Navigation
- Story Views
- Delete Story
- 24-Hour Stories
---
## 👥 Social Features
- Follow Requests
- Accept / Reject Requests
- Follow / Unfollow Users
- Followers List
- Following List
- User Search
- Profile Privacy for Followers/Following Lists

---

## 💬 Real-Time Chat
- One-to-One Messaging
- WebSocket Chat (Django Channels)
- Typing Indicator
- Online / Offline Status
- Read Receipts
- Emoji Support
- Image Sharing
- Delete Chat
- Inbox Search
- Block / Unblock Users

---

## ❤️ Notifications
- Follow Notifications
- Like Notifications
- Comment Notifications
- Notification Counter
---
## 🎨 UI Features
- Responsive Design
- Instagram Inspired Layout
- Dark / Light Mode
- Modern User Interface
- Mobile Friendly
---
# 🛠 Tech Stack
### Backend
- Python
- Django
- Django Channels
- SQLite
### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
### Other
- WebSockets
- Pillow
- Django ORM
---
# 📂 Project Structure
```
socialmedia/
│
├── accounts/
├── posts/
├── stories/
├── inbox/
├── notifications/
├── static/
├── media/
├── templates/
├── manage.py
└── db.sqlite3
```
---
# ⚙ Installation
Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/socialhub.git
```
Go into the project

```bash
cd socialhub
```
Create virtual environment
```bash
python -m venv venv
```
Activate virtual environment
Windows
```bash
venv\Scripts\activate
```
Install dependencies
```bash
pip install -r requirements.txt
```
Run migrations
```bash
python manage.py migrate
```
Run server
```bash
python manage.py runserver
```
Open
```
http://127.0.0.1:8000/
```

# 📸 Screenshots

- Login
- Register
- Home Feed
- Stories
- Profile
- Chat
- Notifications
- Saved Posts

(Add screenshots here)

# 🔮 Future Improvements

- Voice Messages
- Video Calls
- Group Chat
- Story Reactions
- Story Replies
- Video Posts
- Push Notifications
- Email Verification

# 👩‍💻 Developer

**Aleeza Muqadas**
BS Information Technology
International Islamic University Islamabad (IIUI)
GitHub:
https://github.com/lizaykhan5-byte

# 📄 License
This project is developed for educational purposes and internship submission.