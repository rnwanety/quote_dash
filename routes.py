from config import app
from controller_functions import default, register, login, index, add_a_quote, like_quote, user_page, myaccount, edit_account, delete_quote, logout
app.add_url_rule("/", view_func=default)
app.add_url_rule("/register", view_func=register, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/quotes", view_func=index)
app.add_url_rule("/add_a_quote", view_func=add_a_quote, methods=["POST"])
app.add_url_rule("/like/<quote_id>", view_func=like_quote)
app.add_url_rule("/user/<user_id>", view_func=user_page)
app.add_url_rule("/myaccount/<user_id>", view_func=myaccount)
app.add_url_rule("/edit_account", view_func=edit_account, methods=["POST"])
app.add_url_rule("/delete/<quote_id>", view_func=delete_quote)
app.add_url_rule("/logout", view_func=logout)