from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from datetime import datetime






#my db connectin
local_server=True
app= Flask(__name__)
app.secret_key='sachin'




#this is for user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






#app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@loalhost/database_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root123@localhost/fms'
db=SQLAlchemy(app)





#here we will create db models that is tables
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    cats=db.relationship('Category', backref='cat')
    transact=db.relationship('Transaction', backref='tranact')
    pays=db.relationship('Payments', backref='pay')
    
class Payments(db.Model):
    paymentid=db.Column(db.Integer,primary_key=True)
    paymenttype=db.Column(db.String(50))
    paymentmode=db.Column(db.String(50))
    paymentdescription=db.Column(db.String(50))
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))
    tra=db.relationship('Transaction', backref='tran')

class Category(db.Model):
    catid=db.Column(db.Integer,primary_key=True)
    catname=db.Column(db.String(50))
    catdesc=db.Column(db.String(100))
    cattype=db.Column(db.String(50))
    catparentid=db.Column(db.Integer,db.ForeignKey('category.catid'))
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))
    trans=db.relationship('Transaction', backref='tr')

class Vendor(db.Model):
    venid=db.Column(db.Integer,primary_key=True)
    venname=db.Column(db.String(50))
    venloc=db.Column(db.String(50))
    createdon=db.Column(db.DateTime)
    modifiedon=db.Column(db.DateTime)
    userid=db.Column(db.Integer,db.ForeignKey('user.id')) 
    transac=db.relationship('Transaction', backref='trn')  

class Transaction(db.Model):
    transid=db.Column(db.Integer,primary_key=True)
    catid=db.Column(db.Integer,db.ForeignKey('category.catid'))
    venid=db.Column(db.Integer,db.ForeignKey('vendor.venid'))
    paymentid=db.Column(db.Integer,db.ForeignKey('payments.paymentid'))
    amount=db.Column(db.Integer)
    transdate=db.Column(db.String(50))
    transdetails=db.Column(db.String(100))
    particulars=db.Column(db.String(100))
    remarks=db.Column(db.String(100))
    createdon=db.Column(db.DateTime)
    modifiedon=db.Column(db.DateTime)
    userid=db.Column(db.Integer,db.ForeignKey('user.id')) 



   



#here we will pass endpoints and run the functions    
@app.route('/')
@login_required
def index():
    return render_template('index.html')





#endpoints of category page
@app.route('/category',methods=['POST','GET'])
@login_required
def category():  
    uid=current_user.id
    plist= db.engine.execute(f"SELECT catid,catname FROM `category` WHERE `catparentid` IS null AND `userid`={uid}")
    query=db.engine.execute(f"SELECT a.catid,a.catname,a.catdesc,a.cattype, COALESCE( (SELECT b.catname FROM category b WHERE b.catid = a.catparentid),'') 'pcat'  FROM category a where a.userid = {uid}")  
    return render_template('category.html',query=query,plist=plist) 

#insert function of category
@app.route('/select', methods = ['POST'])
@login_required
def select():
    if request.method=="POST":
        catname=request.form.get('category name')
        catdesc=request.form.get('category description')
        cattype=request.form.get('category type')
        catparentid=request.form.get('parent category')
        if catparentid == -1 or catparentid == "":
            catparentid = "NULL"
        userid=request.form.get('userid')
        query=db.engine.execute(f"INSERT INTO `category` (`catname`, `catdesc`, `cattype`, `catparentid`, `userid`) VALUES ('{catname}','{catdesc}','{cattype}', {catparentid}, {userid})")   
    return redirect(url_for('category')) 

#update function of cateogry
@app.route("/update/<string:catid>", methods= ['POST', 'GET'])
@login_required
def update(catid):
    posts=Category.query.filter_by(catid=catid).first()
    uid=current_user.id
    plist= db.engine.execute(f"SELECT catid,catname FROM `category` WHERE `catparentid` IS null AND `userid`={uid}")
    if request.method=='POST':
        catname=request.form.get('category name')
        catdesc=request.form.get('category description')
        cattype=request.form.get('category type')
        catparentid=request.form.get('parent category')
        if catparentid == -1 or catparentid == "":
            catparentid = "NULL"
        userid=request.form.get('userid')
        db.engine.execute(f"UPDATE `category` SET `catname`='{catname}', `catdesc` = '{catdesc}', `cattype` = '{cattype}', `catparentid` = {catparentid}, `userid` = {userid}  WHERE `category`.`catid` = '{catid}'")       
        return redirect('/category')       
    return render_template('update.html',posts=posts,plist=plist) 

#delete function of category
@app.route("/cdelete/<string:catid>",methods=['POST','GET'])
@login_required
def cdelete(catid):
    db.engine.execute(f"DELETE FROM `category` WHERE `category`.`catid`={catid}") 
    return redirect('/category') 


 



#ENDPOINTS OF  VENDOR PAGE
@app.route('/vendor')
@login_required
def vendor():
    uid=current_user.id
    query=db.engine.execute(f"SELECT * FROM `vendor` WHERE userid='{uid}'")
    return render_template('vendor.html',query=query)

#INSERT FUNCTION OF VENDOR
@app.route('/add', methods = ['POST'])
@login_required
def add():
    if request.method=="POST":
        venname=request.form.get('vendor name')
        venloc=request.form.get('vendor location')
        createdon=datetime.now()
        userid=request.form.get('userid')
        query=db.engine.execute(f"INSERT INTO `vendor` (`venname`, `venloc`,`createdon`,`userid`) VALUES ('{venname}','{venloc}','{createdon}',{userid})")   
    return redirect(url_for('vendor')) 

#UPDATE FUNCTION OF VENDOR
@app.route("/vedit/<string:venid>", methods= ['POST', 'GET'])
@login_required
def vedit(venid):
    posts=Vendor.query.filter_by(venid=venid).first()
    if request.method=='POST':
        venname=request.form.get('vendor name')
        venloc=request.form.get('vendor location')
        modifiedon=datetime.now()
        userid=request.form.get('userid')
        db.engine.execute(f"UPDATE `vendor` SET `venname`='{venname}', `venloc` = '{venloc}', `modifiedon`= '{modifiedon}', `userid`={userid}  WHERE `vendor`.`venid` = '{venid}'")       
        return redirect('/vendor')       
    return render_template('vedit.html',posts=posts)   

#DELETE FUNCTION OF VENDOR
@app.route("/vdelete/<string:venid>",methods=['POST','GET'])
@login_required
def vdelete(venid):
    db.engine.execute(f"DELETE FROM `vendor` WHERE `vendor`.`venid`={venid}") 
    return redirect('/vendor') 







#END POINTS OF PAYMENT PAGE
@app.route('/payment',methods=['POST','GET'])
@login_required
def payment(): 
    uid=current_user.id
    query=db.engine.execute(f"SELECT * FROM `payments` WHERE userid={uid}")
    return render_template('payment.html',query=query)  

#INSERT FUNCTION OF PAYMENTS
@app.route('/insert', methods = ['POST'])
@login_required
def insert():
    if request.method=="POST":
        paymenttype=request.form.get('payment type')
        paymentmode=request.form.get('payment mode')
        paymentdescription=request.form.get('payment description')
        userid=request.form.get('userid')
        query=db.engine.execute(f"INSERT INTO `payments` (`paymenttype`,`paymentmode`,`paymentdescription`,`userid`) VALUES ('{paymenttype}','{paymentmode}','{paymentdescription}', {userid})")   
    return redirect(url_for('payment')) 

#UPDATE FUNCTION OF PAYMENTS
@app.route("/edit/<string:paymentid>", methods= ['POST', 'GET'])
@login_required
def edit(paymentid):
    posts=Payments.query.filter_by(paymentid=paymentid).first()
    if request.method=='POST':
        paymenttype=request.form.get('payment type')
        paymentmode=request.form.get('payment mode')
        paymentdescription=request.form.get('payment description')
        userid=request.form.get('userid')
        db.engine.execute(f"UPDATE `payments` SET `paymenttype` = '{paymenttype}', `paymentmode` = '{paymentmode}', `paymentdescription` = '{paymentdescription}' , `userid`={userid} WHERE `payments`.`paymentid` = '{paymentid}'")       
        return redirect('/payment')       
    return render_template('edit.html',posts=posts)

#DELETE FUNCTION OF PAYMENTS
@app.route("/delete/<string:paymentid>",methods=['POST','GET'])
@login_required
def delete(paymentid):
    db.engine.execute(f"DELETE FROM `payments` WHERE `payments`.`paymentid`={paymentid}") 
    return redirect('/payment') 








#ENDPOINTS FOR TRANSACTION PAGE
@app.route('/transaction')
@login_required
def transaction():
    uid=current_user.id
    clist=db.engine.execute(f"SELECT * FROM `category` WHERE userid={uid}")
    vlist= db.engine.execute(f"SELECT * FROM `vendor`  WHERE userid={uid}")
    mlist= db.engine.execute(f"SELECT * FROM `payments` WHERE userid={uid}")
    query=db.engine.execute(f"SELECT `transid`,t.`catid`,c.catname,`amount`,`transdate`,`particulars`,t.`createdon`,t.`modifiedon`, transdetails, remarks, c.cattype FROM `transaction` t INNER JOIN category c ON t.catid=c.catid WHERE t.userid={uid}")
    return render_template('transaction.html',query=query,vlist=vlist,mlist=mlist,clist=clist)


#INSERT FUNCTION OF TRANSACTION 
@app.route('/tselect', methods = ['POST'])
@login_required
def tselect():
    if request.method=="POST":
        catid=request.form.get('catname')
        venid=request.form.get('vendor id')
        paymentid=request.form.get('payment id')
        amount=request.form.get('amount')
        transdate=request.form.get('transaction date')
        transdetails=request.form.get('transaction details')
        particulars=request.form.get('particulars')
        remarks=request.form.get('particulars')
        createdon=datetime.now()
        userid=request.form.get('userid')
        query=db.engine.execute(f"INSERT INTO `transaction` (`catid`, `venid`, `paymentid`, `amount`, `transdate`, `transdetails`, `particulars`, `remarks`, `createdon`, `userid`) VALUES ({catid},{venid},{paymentid},{amount},'{transdate}','{transdetails}','{particulars}','{remarks}', '{createdon}',{userid})")   
    return redirect(url_for('transaction')) 
        

#UPDATE FUNCTION OF TRANSACTION
@app.route("/tedit/<string:transid>", methods= ['POST', 'GET'])
@login_required
def tedit(transid):
    posts=Transaction.query.filter_by(transid=transid).first()
    uid=current_user.id
    clist=db.engine.execute(f"SELECT * FROM `category` WHERE userid={uid}")
    vlist= db.engine.execute(f"SELECT * FROM `vendor`  WHERE userid={uid}")
    mlist= db.engine.execute(f"SELECT * FROM `payments` WHERE userid={uid}")
    if request.method=='POST':
        catid=request.form.get('catname')    
        venid=request.form.get('vendor id')
        paymentid=request.form.get('payment id')
        amount=request.form.get('amount')
        transdate=request.form.get('transaction date')
        transdetails=request.form.get('transaction details')
        particulars=request.form.get('particulars')
        remarks=request.form.get('remarks')        
        modifiedon=datetime.now()
        userid=request.form.get('userid')
        db.engine.execute(f"UPDATE `transaction` SET `catid`={catid}, `venid`={venid}, `paymentid`={paymentid}, `amount`='{amount}', `transdate` = '{transdate}', `transdetails` = '{transdetails}', `particulars` = '{particulars}', `remarks` = '{remarks}', `modifiedon`= '{modifiedon}', `userid`={userid}  WHERE `transaction`.`transid` = '{transid}'")       
        return redirect('/transaction')       
    return render_template('tedit.html',posts=posts,vlist=vlist,mlist=mlist,clist=clist) 


#DELETE FUNCTION OF TRANSACTION
@app.route("/tdelete/<string:transid>",methods=['POST','GET'])
@login_required
def tdelete(transid):
    db.engine.execute(f"DELETE FROM `transaction` WHERE `transaction`.`transid`={transid}") 
    return redirect('/transaction') 










#ENDPOINTS OF REPORT PAGE
@app.route('/report', methods=["GET","POST"] )
@login_required
def report():
    uid=current_user.id
    if request.method=='POST':
        fromdt = request.form.get('fdate')
        todt  = request.form.get('tdate')        
        query=db.engine.execute(f"SELECT  c.cattype, c.`catname`, SUM(t.`amount`) AS `amount` FROM  `transaction` t LEFT JOIN `category` c ON t.`catid` = c.`catid` WHERE t.userid= {uid} and	t.`transdate` BETWEEN '" + fromdt + "' AND '" + todt + "' GROUP BY c.`catname` ")
        return render_template('report.html',query=query,fromdt=fromdt,todt=todt )
    else:
        query=db.engine.execute(f"SELECT  c.cattype, c.`catname`, SUM(t.`amount`) AS `amount` FROM  `transaction` t LEFT JOIN `category` c ON t.`catid` = c.`catid` WHERE t.userid= {uid}  GROUP BY c.`catname`")
        return render_template('report.html',query=query)









#ENDPOINTS FOR SIGNUP
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)
        new_user=db.engine.execute(f"INSERT  INTO  `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")        
        return render_template('login.html') 
    return render_template('signup.html') 







#ENDPOINTS FOR LOGIN PAGE
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":       
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html')        
    return render_template('login.html')






#ENDPOINTS FOR LOGOUT PAGE
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




#RUN THE FLASK
app.run(debug=True)    
