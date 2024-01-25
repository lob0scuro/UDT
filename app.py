from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from config import *



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/udt"
db = SQLAlchemy(app)
app.app_context().push()


# site master table
    

class SiteMaster(db.Model):
    site_id = db.Column(db.String(25), nullable=False, unique=True, primary_key=True)
    site_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(125))
    coordinates = db.Column(db.String(50))
    type_of = db.Column(db.String(50))
    tower = db.Column(db.String(50))
    unit_make = db.Column(db.String(50))
    unit_model = db.Column(db.String(50))
    unit_serial = db.Column(db.String(50))
    freon = db.Column(db.String(50))
    controller = db.Column(db.String(50))
    filters = db.Column(db.String(50))










# parts order table
# class Parts_Order(db.Model):
#     id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
#     part_name = db.Column(db.String(50), nullable=False)
#     part_model = db.Column(db.String(50))
#     quantity_ordered = db.Column(db.Integer)
#     job_no = db.Column(db.String(10))
#     date_ordered = db.Column(db.DateTime, nullable=False)
#     po = db.Column(db.String(10))
#     siteAssoc = db.Column(db.String(50), db.ForeignKey('SiteMaster.site_id'), nullable=False)
    
#     def __repr__(self):
#         return f"Order: {self.id}/ for site({self.siteAssoc})"
    



@app.route("/", methods=['GET', 'POST'])
def index():
    status = 1
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

        siteEntry = SiteMaster(site_id=site_id, site_name=site_name, coordinates=coordinates, owner=owner, manufacturer=manufacturer, model=model, serial=serial, refrigerant=refrigerant, controller=controller, filters=filters)
        
        try:
            db.session.add(siteEntry)
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
        finally:
            db.session.commit()

    if status:  
        return render_template('index.html')
    else:
        return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template('login.html')



@app.route("/search")
def search():
    contents = SiteMaster.query.all()
    return render_template('search.html', contents=contents)



@app.route("/results")
def results():
    criteria = request.args.get('criteria') 
    if criteria:
        contents = SiteMaster.query.filter(SiteMaster.site_id.icontains(criteria) | SiteMaster.site_name.icontains(criteria) | SiteMaster.coordinates.icontains(criteria) | SiteMaster.tower.icontains(criteria)).limit(25).all() 
    else:
        contents = SiteMaster.query.all()
    return render_template('search_results.html', contents=contents)
    




@app.route("/describe/<id>")
def describe(id):
    data = db.session.query(SiteMaster).get(id)
    return render_template('describe.html', data=data)


@app.route("/edit/<obj>", methods=['GET', 'POST'])
def edit(obj):
    data = db.session.query(SiteMaster).get(obj)
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        owner = request.form.get('owner')
        coordinates = request.form.get('coordinates')
        parish = request.form.get('parish')
        manufacturer = request.form.get('manufacturer')
        model = request.form.get('model')
        serial = request.form.get('serial')
        refrigerant = request.form.get('refrigerant')
        controller = request.form.get('controller')
        filter = request.form.get('filters')
               
        
        try:
            data.site_id = id
            data.site_name = name
            data.owner = owner
            data.coordinates = coordinates
            data.parish = parish
            data.manufacturer = manufacturer
            data.model = model
            data.serial = serial
            data.refrigerant = refrigerant
            data.controller = controller
            data.filters = filter
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
        finally:
            db.session.commit()
            return redirect(url_for("update_successful", id=data.site_id))
        
    return render_template('site-editor.html', data=data)


@app.route("/update_successful/<id>")
def update_successful(id):
    data = db.session.query(SiteMaster).get(id)
    return render_template("update_successful.html", data=data)



@app.route("/parts_order_form")
def parts_order_form():
    # not ready - state = 0
    # edit/ready = 1
    return render_template('parts.html', state=1)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
