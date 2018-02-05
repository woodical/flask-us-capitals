import flask
import sqlite3
import contextlib

DB = 'app.db'
app = flask.Flask(__name__)

COLUMNS = """
    State, 
    Abbreviation, 
    Year_of_Statehood, 
    Capital, 
    Area, 
    Population
"""


@app.route('/us_states/api/v1.0/us_states', methods=['GET'])
def get_us_states():
    with contextlib.closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT %s
            FROM list_of_us_state_capitals 
            ORDER BY State""" % COLUMNS
                    )

        us_states = cur.fetchall()

    return flask.jsonify(us_states)


@app.route('/us_states/api/v1.0/us_states/<state>', methods=['GET'])
def get_us_state(state):
    with contextlib.closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT %s 
            FROM list_of_us_state_capitals 
            WHERE State = ?
            """ % COLUMNS,
                    (state,)
                    )

        us_state = cur.fetchone()

    return flask.jsonify(us_state)


@app.route('/us_states/api/v1.0/us_states', methods=['POST'])
def create_us_state():
    if not flask.request.json or 'State' not in flask.request.json:
        flask.abort(400)

    sql = '''INSERT INTO list_of_us_state_capitals VALUES(?,?,?,?,?,?) '''
    us_state = (
        flask.request.json['State'],
        flask.request.json['Abbreviation'],
        flask.request.json['Year_of_Statehood'],
        flask.request.json['Capital'],
        flask.request.json['Area'],
        flask.request.json['Population'],
    )
    with contextlib.closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        cur.execute(sql, us_state)
        conn.commit()

    return flask.jsonify(us_state), 201


@app.route('/us_states/api/v1.0/us_states/<state>', methods=['PUT'])
def update_us_state(state):
    app.logger.info(flask.request.json)
    us_state = (
        flask.request.json['Abbreviation'],
        flask.request.json['Year_of_Statehood'],
        flask.request.json['Capital'],
        flask.request.json['Area'],
        flask.request.json['Population'],
        state,
    )
    sql = '''
        UPDATE list_of_us_state_capitals
        SET 
            Abbreviation = ?,
            Year_of_Statehood = ?,
            Capital = ?,
            Area = ?,
            Population = ?
        WHERE State = ?
    '''
    with contextlib.closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        cur.execute(sql, us_state)
        conn.commit()
    return flask.jsonify(us_state), 201


@app.route('/us_states/api/v1.0/us_states/<state>', methods=['DELETE'])
def delete_us_state(state):
    sql = 'DELETE FROM list_of_us_state_capitals WHERE State=?'
    with contextlib.closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        cur.execute(sql, (state,))
        conn.commit()

    return '', 204


@app.route('/')
def main():
    return flask.render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
