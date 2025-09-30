# BlogWriter

**BlogWriter** is a full-featured blogging website built with **Django**. It allows users to create, edit, and manage blogs, interact via comments and likes, and even generate AI-powered summaries of posts.

---

## Features

- **User Authentication:** Register, login, and logout functionality with custom user creation.
- **Blog Management:** Create, edit, and delete your own blog posts.
- **Tags:** Add multiple tags to a blog and explore related posts based on tags.
- **Comments:** Authenticated users can comment on posts with instant updates.
- **Likes:** Users can like or unlike posts with real-time feedback.
- **AI Summarization:** Generate a concise summary of a blog post using Hugging Face Transformers.
- **User Dashboard:** View all blogs authored by the logged-in user.
- **Responsive UI:** Works seamlessly on desktops and mobile devices.

---

## Tech Stack

- **Backend:** Django, Python  
- **Frontend:** HTML, CSS, JavaScript, AJAX  
- **Database:** SQLite (default)  
- **AI Integration:** Hugging Face Transformers (`sshleifer/distilbart-cnn-12-6`) for summarization  
- **Version Control:** Git & GitHub  

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/madhumathidhonuri/BlogWriter.git
   cd BlogWriter
