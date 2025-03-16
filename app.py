from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    """ Página principal para upload """
    arquivos = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", arquivos=arquivos)


@app.route("/upload", methods=["POST"])
def upload_file():
    """ Lida com o envio de arquivos """
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo encontrado!"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado!"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    return jsonify({"message": f"Arquivo {file.filename} enviado com sucesso!", "filename": file.filename})


@app.route("/listar_arquivos")
def listar_arquivos():
    """ Retorna a lista de arquivos no diretório de upload """
    arquivos = os.listdir(UPLOAD_FOLDER)
    return jsonify(arquivos)


if __name__ == "__main__":
    app.run(debug=True)