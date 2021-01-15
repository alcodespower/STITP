from flask import Flask,request,render_template,json
import time
import utils
import json
import string
from flask import jsonify
import decimal
from jieba.analyse import extract_tags


app = Flask(__name__)


class MyJSONEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, decimal.Decimal):
      # Convert decimal instances to strings.
      return str(obj)
    return super(MyJSONEncoder, self).default(obj)

@app.route('/')
def welcome():
  return  render_template("main.html")

@app.route('/login')
def form():
  id = request.values.get("id")
  return f"""
  <form>
    账号：<input value="{id}"><br />
    密码：<input>
    
  </form>
  """




@app.route('/time')
def get_time():
  return utils.get_time()

@app.route('/c2')
def get_c2_data():
  res = []
  # print(utils.get_c2_data())
  for tup in utils.get_c2_data():
    # print(tup)
    res.append({"name":tup[0],"value":int(tup[1])})
  return jsonify({"data":res})

@app.route('/c1')
def get_c1_data():
  data = utils.get_c1_data()
  return jsonify({"confirm":int(data[0]),"suspect":int(data[1]),"heal":int(data[2]),"dead":int(data[3])})

@app.route('/l1')
def get_l1_data():
  data = utils.get_l1_data()
  day,confirm,suspect,heal,dead = [],[],[],[],[]
  for a,b,c,d,e in data[7:]:
    day.append(a.strftime("%m-%d"))  #a是datatime类型
    confirm.append(b)
    suspect.append(c)
    heal.append(d)
    dead.append(e)
  return jsonify({"day":day,"confirm":confirm,"suspect":suspect,"heal":heal,"dead":dead})


@app.route("/l2")
def get_12_data():
  data = utils.get_l2_data()
  day,confirm_add,suspect_add = [],[],[]
  for a,b,c in data[7:]:
    day.append(a.strftime("%m-%d"))
    confirm_add.append(b)
    suspect_add.append(c)
  return jsonify({"day":day,"confirm_add":confirm_add,"suspect_add":suspect_add})

@app.route('/r1')
def get_r1_data():
  data = utils.get_r1_data()
  city = []
  confirm = []
  for k,v in data:
    city.append(k)
    confirm.append(int(v))
  return jsonify({"city":city,"confirm":confirm})

@app.route('/r2')
def get_r2_data():
  data = utils.get_r2_data()
  d = []
  for i in data:
    k = i[0].rstrip(string.digits) #去除热搜数字
    v = i[0][len(k) :] # 获取热搜数字
    ks = extract_tags(k) #使用jieba提取关键词
    for j in ks:
      if not j.isdigit():
        d.append({"name":j,"value":v})
  return jsonify({"kws": d})

# 修复TypeError: Object of type 'Decimal' is not JSON serializable
# decimal类型的对象不可JSON序列化
####以下代码未测试####################
# 重写flask.json.JSONEncoder里面默认方法
# class MyJSONEncoder(flask.json.JSONEncoder):
#
#     def default(self, obj):
#         if isinstance(obj, decimal.Decimal):
#             # Convert decimal instances to strings.
#             return str(obj)
#         return super(MyJSONEncoder, self).default(obj)
# app.json_encoder = MyJSONEncoder
# #################################
# class DecimalEncoder(json.JSONEncoder):
#   def default(self, o):
#     if isinstance(o, decimal.Decimal):
#       return float(o)
#     super(DecimalEncoder, self).default(o)



if __name__ == '__main__':

  app.json_encoder = MyJSONEncoder
  app.run(debug=True)