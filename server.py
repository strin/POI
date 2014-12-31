from flask import *
import rtree
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
data = rtree.load_data('data/POI_jiaotong.txt')
category = rtree.load_category('data/category.csv')

@app.route("/")
def hello():
  try:
    return render_template('main.html', centerx=rtree.get_center_x(data), 
                                        centery=rtree.get_center_y(data),
                                        centers=[(float(d['X_COORD']),float(d['Y_COORD']), d['KEY_NAME']) for d in data], 
                                        main_category=category.keys())
  except Exception as e:
    print 'error: ', e

@app.route("/category1", methods=['POST'])
def category1():
  try:
    input = request.form['cat'].decode('utf-8')
    return jsonify(cat=category[input].keys());
  except Exception as e:
    print 'error: ', e

@app.route("/category2", methods=['POST'])
def category2():
  try:
    cat1 = request.form['cat1'].decode('utf-8')
    cat2 = request.form['cat2'].decode('utf-8')
    return jsonify(cat=category[cat1][cat2].keys());
  except Exception as e:
    print 'error: ', e

@app.route("/category3", methods=['POST'])
def category3():
  try:
    cat1 = request.form['cat1'].decode('utf-8')
    cat2 = request.form['cat2'].decode('utf-8')
    cat3 = request.form['cat3'].decode('utf-8')
    return jsonify(id=category[cat1][cat2][cat3]);
  except Exception as e:
    print 'error: ', e

@app.route("/poi", methods=['POST'])
def poi():
  try:
    cat = int(request.form['cat'].decode('utf-8'))
    pinx = float(request.form['pinx'])
    piny = float(request.form['piny'])
    range = int(request.form['range'])
    print 'cat', cat, 'point', (piny, pinx), 'range', range
    if range == 0:
      dt = rtree.nearest_neighbor(data, (piny, pinx), cat)
    else:
      dt = rtree.range_search(data, (piny, pinx), range, cat)
    print 'dt', dt
    if dt == None:
      return jsonify(data=[])
    if range == 0:
      return jsonify(data=[dt])
    else:
      return jsonify(data=dt)

  except Exception as e:
    print 'error: ', e


if __name__ == "__main__":
  app.run(port=8080)
