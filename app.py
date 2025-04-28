from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emoji.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Emojies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intro = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Emojies %r>' % self.id


@app.route('/')
def index():
    return render_template("base.html")


@app.route('/your-favorites')
def favorites():
    emojies = Emojies.query.order_by(Emojies.title).all()
    return render_template("your-favorites.html", emojies=emojies)


@app.route('/', methods=['POST', 'GET'])
def go_back():
    return render_template('about.html')


@app.route('/create-emoji', methods=['POST', 'GET'])
def create_emoji():
    title = intro = text = category = ''

    if request.method == 'POST':

        title = request.form.get('title', '')
        intro = request.form.get('intro', '')
        text = request.form.get('text', '')

        if not all([title, intro, text]):
            return 'mistake', 400

        emoji = Emojies(title=title, intro=intro, text=text)

        try:
            db.session.add(emoji)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Mistake: {e}", 500
    else:
        return render_template('create-emoji.html')



@app.route('/your-favorites/<int:id>/del')
def group_delete(id):
    emojies = Emojies.query.get_or_404(id)
    try:
        db.session.delete(emojies)
        db.session.commit()
        return redirect('/your-favorites')
    except:
        return "Error in deletion"


@app.route('/filter', methods=['GET'])
def filter_data():
    text = request.args.get('text', '')
    category = request.args.get('category', '')


    filtered_emojies = Emojies.query.filter(
        (Emojies.title.ilike(f"%{text}%") if text else True) &
        (Emojies.category.ilike(f"%{category}%") if category else True)
    ).all()


    result = [{"title": emoji.title, "intro": emoji.intro, "text": emoji.text, "category": emoji.category}
              for emoji in filtered_emojies]

    return jsonify(result)


@app.route('/about', methods=['POST', 'GET'])
def back_home():
    return render_template("about.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
