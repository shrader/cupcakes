"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

"""data = {
        "id" : self.id,
        "flavor" : self.flavor,
        "size" : self.size,
        "rating" : self.rating,
        "image" : self.image
        } """


@app.route("/api/cupcakes", methods=["GET","POST"])
def show_and_create_cupcakes():
    """Return a list of cupcakes."""
    if request.method == "GET":
        cupcakes = Cupcake.query.all()
        serialized_cupcakes = [cupcake.serialize() for cupcake in cupcakes]

        return jsonify(cupcakes = serialized_cupcakes)
    

    json = request.json
    new_cupcake = Cupcake(flavor=json["flavor"], size=json["size"], rating = json["rating"], image=json.get("image"))
    db.session.add(new_cupcake)
    db.session.commit()
    
    return jsonify(cupcake = new_cupcake.serialize())




@app.route("/api/cupcakes/<int:cupcake_id>")
def show_playlist(cupcake_id):
    """Show detail on specific cupcake."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake = cupcake.serialize())


@app.route("/playlists/add", methods=["POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    form = PlaylistForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        new_playlist = Playlist(name=name, description=description)
        db.session.add(new_playlist)
        db.session.commit()

        return redirect("/playlists")
    
    return render_template("new_playlist.html", form = form)

""" GET /api/cupcakes
Get data about all cupcakes.

Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.

The values should come from each cupcake instance.

GET /api/cupcakes/[cupcake-id]
Get data about a single cupcake.

Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

This should raise a 404 if the cupcake cannot be found.

POST /api/cupcakes
Create a cupcake with flavor, size, rating and image data from the body of the request.

Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}. """