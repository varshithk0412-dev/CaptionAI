from flask import Flask, render_template, redirect, url_for, request, flash, session,send_from_directory
import os
from register_user import add_user, user_exists
from werkzeug.utils import secure_filename
from generate_captions import create_captions
from attach_captions import attach_captions_to_video

app = Flask(__name__)
app.secret_key = os.urandom(24) 

UPLOAD_FOLDER = 'user_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
OUTPUT_FOLDER = 'outputs'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

VALID_EXT = {'mp3', 'mp4', 'webm', 'mov'} 

def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in VALID_EXT

@app.route("/")
def home(): 
    return render_template('home.html')

@app.route("/register", methods=["GET", "POST"])
def register(): 
    if request.method == "POST": 
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if user_exists(email): 
            flash("User with this email already exists.")
            return redirect(url_for('login'))
            
        if password != confirm_password: 
            flash("Passwords do not match.")
            return render_template('register.html')

        add_user(name, email, password)
        flash("Account created successfully! Please log in.")
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login(): 
    if request.method == "POST": 
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = user_exists(email)
        
        if user is None: 
            flash("No user registered with this email.")
            return redirect(url_for('register'))

        if user['password'] != password:
            flash("Incorrect password. Please try again.")
            return render_template('login.html')
            
        session['user_id'] = user['id']
        return redirect(url_for('upload')) 

    return render_template('login.html')

@app.route("/upload", methods=["GET", "POST"])
def upload(): 
    if 'user_id' not in session:
        flash("Please log in to access the upload page.")
        return redirect(url_for('login'))

    if request.method == "POST": 
        if 'file' not in request.files:
            flash("No file part detected in the request.")
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '':
            flash("No file selected.")
            return redirect(request.url)
            
        if file and allowed(file.filename):
            filename = secure_filename(file.filename)
            
            user_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(session['user_id']))
            
            os.makedirs(user_dir, exist_ok=True)
            

            save_path = os.path.join(user_dir, filename)
            


            if os.path.exists(save_path):
                flash(f"A file named '{filename}' already exists! Please rename your file or delete the old one.")
                return redirect(request.url)
            file.save(save_path)
            flash(f"File '{filename}' successfully uploaded!")
            captions = create_captions(save_path)
            attach_captions_to_video(save_path,captions,session['user_id'])
            return redirect(url_for('upload'))
        else:
            flash("Invalid file type. Please upload a valid media file.")
            return redirect(request.url) 

    return render_template('upload.html')

@app.route("/history")
def history():
   
    if 'user_id' not in session:
        flash("Please log in to view your history.")
        return redirect(url_for('login'))

    user_id = str(session['user_id'])
    user_output_dir = os.path.join(app.config['OUTPUT_FOLDER'], user_id)
    
    videos = []
    
  
    if os.path.exists(user_output_dir):

        for filename in os.listdir(user_output_dir):
            if filename.endswith(('.mp4', '.mov', '.webm')):
                videos.append(filename)

    return render_template('history.html', videos=videos)

@app.route("/view_video/<user_id>/<filename>")
def view_video(user_id, filename):
    
    if 'user_id' not in session or str(session['user_id']) != str(user_id):
        flash("Unauthorized access.")
        return redirect(url_for('login'))
        
    user_output_dir = os.path.join(app.config['OUTPUT_FOLDER'], str(user_id))
    return send_from_directory(user_output_dir, filename)
if __name__ == "__main__":
    app.run(debug=True)