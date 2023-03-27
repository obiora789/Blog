from flask import Flask, render_template, redirect, url_for, session, request
import requests
import os
import dotenv
from datetime import datetime
import smtplib

new_file = dotenv.find_dotenv()
dotenv.load_dotenv(new_file)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET")
LINKEDIN = os.environ.get("LINKED-IN")
GITHUB = os.getenv("GIT-HUB")
TWITTER = os.environ.get("TWITTER_")
MY_RESUME = os.getenv("RESUME")
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASS = os.getenv("EMAIL_PASSWORD")
ANOTHER_EMAIL = os.environ.get("OTHER_EMAIL")
mail_list = ["vanessanwolisa64@gmail.com", MY_EMAIL, ANOTHER_EMAIL]
blogger = os.environ.get("NAME")
# api_url = "https://api.npoint.io/c790b4d5cab58020d391"
api_url = "https://api.npoint.io/82616525f477bf9308d1"
# api_url = "https://api.npoint.io/19ea8c2059c45a9d6742"
response = requests.get(api_url)
all_posts = response.json()# ["posts"]


@app.route("/")
def home():
    num_of_posts = len(all_posts)
    current_year = session.get("c_year")
    return render_template("index.html", posts=all_posts, name=blogger, resume=MY_RESUME, sum_of_posts=num_of_posts,
                           year=current_year, github=GITHUB, linkedin=LINKEDIN, twitter=TWITTER)


@app.route("/<blog_id>")
def article(blog_id):
    current_year = session.get("c_year")
    return render_template('post.html', posts=all_posts, article_id=int(blog_id), year=current_year, github=GITHUB,
                           linkedin=LINKEDIN, twitter=TWITTER, name=blogger, resume=MY_RESUME)


@app.route("/about")
def about():
    current_year = session.get("c_year")
    return render_template("about.html", year=current_year, github=GITHUB, linkedin=LINKEDIN, twitter=TWITTER,
                           name=blogger)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    current_year = session.get("c_year")
    if request.method == "POST":
        user = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("phone")
        message = request.form.get("message")
        with smtplib.SMTP(host="smtp.office365.com:587") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASS)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=mail_list,
                                msg=f"Subject: Notification from {user.title()} with email {email}.\n\n"
                                    f"Hello {blogger.title()}, {user.title()} has left you a message."
                                    f"Details below:\n"
                                    f"Name: {user.title()}\n"
                                    f"Email: {email}\n"
                                    f"Mobile: {mobile}\n"
                                    f"Message: {message}\n")
    return render_template("contact.html", year=current_year, github=GITHUB, linkedin=LINKEDIN, twitter=TWITTER,
                           name=blogger)


@app.route("/footer")
def footer():
    year = str(datetime.now().year)
    session["c_year"] = year
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

