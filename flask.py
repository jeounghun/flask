from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
CORS(app)  # CORS 설정 적용

# MySQL 연결 설정
app.config['MYSQL_HOST'] = 'localhost'  # MySQL 호스트
app.config['MYSQL_USER'] = 'root'  # MySQL 사용자명
app.config['MYSQL_PASSWORD'] = ''  # MySQL 비밀번호
app.config['MYSQL_DB'] = 'results'  # 생성한 데이터베이스명
mysql = MySQL(app)

@app.route('/data', methods=['POST'])
def receive_data():
    # 이미지 데이터 추출
    image = request.files['image']

    # 이미지 처리 (이미지를 서버에 저장)
    image.save(os.path.join(app.root_path, 'img', image.filename))

    # JSON 데이터 추출
    data = request.get_json()

    # 변수 추출
    damA = data.get('damA')
    damB = data.get('damB')
    damD = data.get('damD')
    damE = data.get('damE')

    # MySQL에 데이터 삽입
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO measurements (damA, damB, damD, damE) VALUES (%s, %s, %s, %s)",
                (damA, damB, damD, damE))
    mysql.connection.commit()
    cur.close()

    # 결과값 포맷팅
    formatted_data = {}
    if damA is not None:
        formatted_data['damA'] = "{:.1f}".format(float(damA))
    if damB is not None:
        formatted_data['damB'] = "{:.1f}".format(float(damB))
    if damD is not None:
        formatted_data['damD'] = "{:.1f}".format(float(damD))
    if damE is not None:
        formatted_data['damE'] = "{:.1f}".format(float(damE))

    # 원하는 값을 출력
    selected_data = {}
    if 'print_damA' in request.args and 'damA' in formatted_data:
        selected_data['damA'] = formatted_data['damA']
    if 'print_damB' in request.args and 'damB' in formatted_data:
        selected_data['damB'] = formatted_data['damB']
    if 'print_damD' in request.args and 'damD' in formatted_data:
        selected_data['damD'] = formatted_data['damD']
    if 'print_damE' in request.args and 'damE' in formatted_data:
        selected_data['damE'] = formatted_data['damE']

    # 선택된 데이터 반환
    return jsonify(selected_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)