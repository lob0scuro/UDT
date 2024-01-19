from flask import Flask, render_template, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from config import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/udt"
db = SQLAlchemy(app)
app.app_context().push()

class Sites(db.Model):
    siteID = db.Column(db.String(25), nullable=False, unique=True, primary_key=True)
    siteName = db.Column(db.String(50), nullable=False)
    coordinates = db.Column(db.String(50))
    owner = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    model = db.Column(db.String(50))
    serial = db.Column(db.String(50))
    refrigerant = db.Column(db.String(50))
    controller = db.Column(db.String(50))
    filters = db.Column(db.String(50))
    
    def __repr__(self):
        return f"Site: {self.siteID} {self.siteName}"


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        site_name = request.form.get('site-name')
        site_id = request.form.get('site-id')
        coordinates = request.form.get('coordinates')
        owner = request.form.get('owner')

        manufacturer = request.form.get('make')
        model = request.form.get('model')
        serial = request.form.get('serial')
        refrigerant = request.form.get('freon')
        controller = request.form.get('controller')
        filters = request.form.get('filters')

        siteEntry = Sites(siteID=site_id, siteName=site_name, coordinates=coordinates, owner=owner, manufacturer=manufacturer, model=model, serial=serial, refrigerant=refrigerant, controller=controller, filters=filters)
        
        try:
            db.session.add(siteEntry)
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
        finally:
            db.session.commit()

                

    return render_template("index.html")

@app.route("/search")
def search():
    contents = Sites.query.all()
    return render_template('search.html', contents=contents)



@app.route("/results")
def results():
    criteria = request.args.get('criteria') 
    if criteria:
        contents = Sites.query.filter(Sites.siteID.icontains(criteria) | Sites.siteName.icontains(criteria) | Sites.coordinates.icontains(criteria) | Sites.owner.icontains(criteria)).limit(25).all() 
    else:
        contents = Sites.query.all()
    return render_template('search_results.html', contents=contents)
    

@app.route("/parts_order_form")
def parts_order_form():
    return render_template('parts.html')


@app.route("/describe")
def describe():
    q = request.form.get('identifiedBy')
    data = Sites.query.get(q)
    return render_template('describe.html', data=data)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
