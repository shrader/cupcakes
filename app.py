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


@app.route("/api/cupcakes", methods=["GET", "POST"])
def show_and_create_cupcakes():
    """Return a list of cupcakes."""
    if request.method == "GET":
        cupcakes = Cupcake.query.all()
        serialized_cupcakes = [cupcake.serialize() for cupcake in cupcakes]

        return jsonify(cupcakes = serialized_cupcakes)
    

    json = request.json
    new_cupcake = Cupcake(flavor=json["flavor"], size=json["size"], rating =json["rating"], image=json.get("image"))
    db.session.add(new_cupcake)
    db.session.commit()
    
    return (jsonify(cupcake = new_cupcake.serialize()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["GET", "PATCH", "DELETE"])
def manipulate_cupcake(cupcake_id):
    """Show detail on specific cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    if request.method == "PATCH":
        data = request.json
        cupcake.flavor = data.get("flavor") or cupcake.flavor
        cupcake.size = data.get("size") or cupcake.size 
        cupcake.rating = data.get("rating") or cupcake.rating 
        cupcake.image = data.get("image") or cupcake.image 
        db.session.commit()
        return jsonify(cupcake = cupcake.serialize())

    if request.method == "DELETE":
        db.session.delete(cupcake)
        db.session.commit()
        return jsonify({"message": "Deleted"})

    return jsonify(cupcake = cupcake.serialize())