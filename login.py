#import library
from flask import Flask, request, make_response, jsonify, render_template
from flask_restful import Resource, Api
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

#Library pendukung
import jwt
import os
import datetime

from sqlalchemy import delete, outerjoin

#inisalisasi objek flask
login = Flask(__name__)
fancy = Api(login)
db = SQLAlchemy(login)
CORS(login)

# konfigurasi database ==> create file db.sqlite
filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db.sqlite')
login.config['SQLALCHEMY_DATABASE_URI'] = database

#SECRET KEY
login.config['SECRET_KEY'] = "inirahasianegara"
# schema model database auth
class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))

# model schema article
class EdukasiModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100))
    konten = db.Column(db.Text)
    penulis = db.Column(db.String(50))

class GambarModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.BLOB)


#create model database ke file db.sqlite
db.create_all()

#decorator
def butuh_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('datatoken') 
        if not token:
            return make_response(jsonify({"msg":"No tokens!"}))
        try:
            jwt.decode(token, login.config['SECRET_KEY'], algorithms="HS256")
        except:
            return make_response(jsonify({"msg":"Invalid Token Entered!"}), 401)          
        return f(*args, **kwargs)
    return decorator

#routing endpoint
#routing auth 
@login.route('/', methods=['GET'])
def hello_World():
    return "This is FancyBin"

class RegisterUser(Resource):
    #posting data daru front end untuk disimpan dalam database
   
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        #cek
        if dataUsername and dataPassword:
            #
            dataModel = AuthModel(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"Register berhasil"}), 200)
        return jsonify({"msg":"Username and Password data cannot be empty"})    


# routing untuk login
class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        #query kecocokan data
        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword  :
            # login sukses & generate token auth
            token = jwt.encode(
               {
                   "username":queryUsername, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
           },      login.config['SECRET_KEY'], algorithm="HS256"
         )
            return make_response(jsonify({"msg":"Login Success!", "token":token}), 200)

           #login gagal
        return jsonify({"msg":"Login failed, Please try again!"})

class UpdateUser(Resource): 
    @butuh_token  
    def delete(self,id):
        # query db berdasarkan id
        query = AuthModel.query.get(id)

        if not query:
         return jsonify({'message' : 'User Data Could Not Be Found!'})

        db.session.delete(query)
        db.session.commit()
        return make_response(jsonify({"msg":"User Data Deleted Successfully!"}), 200)


class GambarModel(Resource):
    #menambah gambar
    def post(self):
            file = request.files['file']
            if not file:
              return jsonify({'message' : 'Upload Failed!'})
            

            file.save(os.path.join('./gambar', file.filename))
            return({"msg":'Successfully uploading files'}), 200
      
#endpoint artikel baru untuk user yang sudah ter-integrasi
#endpoint protected 
class TambahArtikel(Resource):
    #akan diproteksi
    @butuh_token
    def post(self):
        #menambah artikel baru kedalam database
        dataJudul = request.form.get('jenis')
        dataKonten = request.form.get('konten')
        dataPenulis = request.form.get('poin')

        data = EdukasiModel(judul=dataJudul, konten=dataKonten, penulis=dataPenulis)
        db.session.add(data)
        db.session.commit()
        return{"msg":"Result Data Added Successfully!"}, 200

 

#Routing untuk menghapus/mengedit data
class UpdateDataById(Resource):
    #e dit data dan butuh id
    @butuh_token
    def put(self, id):
        query = EdukasiModel.query.get(id)

        #get data dari form / multipart form(frontend)
        dataJudul = request.form.get('jenis')   
        dataKonten = request.form.get('konten')
        dataPenulis = request.form.get('poin')
      
        query.judul = dataJudul 
        query.konten = dataKonten
        query.penulis = dataPenulis
        db.session.commit()
        return make_response(jsonify({"msg":"Data Successfully Update!"}), 200)

        #delete 1 data berdasarkan id
    @butuh_token   
    def delete(self,id):
        # query db berdasarkan id
        query = EdukasiModel.query.get(id)

        if not query:
         return jsonify({'message' : 'Data not found!'})

        db.session.delete(query)
        db.session.commit()
        return make_response(jsonify({"msg":"Data Successfully Delete"}), 200)

# view data berdasarkan id(menampilkan 1 buah data)
    @butuh_token
    def get(self,id):
        query = EdukasiModel.query.get(id)
        output = {
            "id":query.id,
            "jenis":query.judul,
            "konten":query.konten,
            "poin":query.penulis
        } 
        return make_response(jsonify(output), 200)

        

#inisiasi resource api

fancy.add_resource(RegisterUser, "/fancy/register", methods=["POST"])
fancy.add_resource(LoginUser, "/fancy/login", methods=["POST"])
fancy.add_resource(UpdateUser, "/fancy/login/<id>", methods=["DELETE"])
fancy.add_resource(GambarModel, "/fancy/menu", methods=["POST", "GET"])
fancy.add_resource(TambahArtikel, "/fancy/result", methods=["POST"])
fancy.add_resource(UpdateDataById, "/fancy/result/<id>", methods=["PUT", "DELETE", "GET"])




#menjalankan aplikasi
if __name__ == "__main__":
    login.run(debug=True, port=80)
          



            

    
    