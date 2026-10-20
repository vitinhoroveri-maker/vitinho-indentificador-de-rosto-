from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
detector = cv2.CascadeClassifier(CASCADE_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    if detector.empty():
        return jsonify({"error": "O detector facial não foi carregado."}), 500
    payload = request.get_json(silent=True) or {}
    image_data = payload.get("image", "")
    if not image_data or "," not in image_data:
        return jsonify({"error": "Imagem não recebida."}), 400
    try:
        encoded = image_data.split(",", 1)[1]
        raw = base64.b64decode(encoded)
        array = np.frombuffer(raw, dtype=np.uint8)
        frame = cv2.imdecode(array, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({"error": "Não foi possível ler a imagem."}), 400
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(45, 45)
        )
        h, w = frame.shape[:2]
        return jsonify({
            "count": len(faces),
            "width": w,
            "height": h,
            "faces": [
                {"x": int(x), "y": int(y), "width": int(fw), "height": int(fh)}
                for x, y, fw, fh in faces
            ]
        })
    except Exception as exc:
        return jsonify({"error": f"Erro ao analisar imagem: {exc}"}), 400

if __name__ == "__main__":
    print("\nIA Rostos Pro está iniciando.")
    print("Abra http://127.0.0.1:5000 no navegador.")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
