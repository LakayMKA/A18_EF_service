from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


DATABASE_URL = "sqlite:///./projet_BD.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



class Projet(Base):
    __tablename__ = "projets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Code_projet=Column(String, nullable=False)
    Nom = Column(String, nullable=False)
    Description = Column(String, nullable=False)


Base.metadata.create_all(engine)



@app.route('/projet', methods=['POST'])
def create_projet():
    data = request.json
    new_projet = Projet( Code_projet=data['Code_projet'],Nom=data['Nom'], Description=data['Description'])
    session.add(new_projet)
    session.commit()
    return jsonify({"message": "Projet créé!", "id": new_projet.id}), 201


@app.route('/projet/<int:projet_id>', methods=['GET'])
def get_projet(projet_id):
    projet = session.query(Projet).filter_by(id=projet_id).first()
    if projet:
        return jsonify({"id": projet.id,"Code_projet":projet.Code_projet, "Nom": projet.Nom, "Description": projet.Description})
    else:
        return jsonify({"message": "Projet non trouvé!"}), 404


if __name__ == '__main__':
    app.run(port=5005)
