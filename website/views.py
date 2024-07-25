from flask import Blueprint, render_template, request, redirect, url_for, json, flash, session
from .models import TransformerModel, Admin
#from flask_login import login_required, current_user
#from .models import Note
from . import db
import os
from werkzeug.utils import secure_filename
from .models import Benchmark

views = Blueprint('views', __name__)

comet_rerank = False
BERTScore_rerank = False
TER_rerank = False
ChrF_rerank = False
bleu_rerank = False

@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():
    # if request.method == 'POST': 
    #     note = request.form.get('note')#Gets the note from the HTML 

    #     if len(note) < 1:
    #         flash('Note is too short!', category='error') 
    #     else:C:\Users\SOHAM\Desktop\Leaderboard_website\datasets\uploaded_files
    #         new_note = Note(data=note, user_id=123)  #providing the schema for the note 
    #         db.session.add(new_note) #adding the note to the database 
    #         db.session.commit()
    #         flash('Note added!', category='success')
    # Fetch Transformer models ordered by BLEU score in descending order    
    # return render_template("index.html", models=models)
    # models = TransformerModel.query.all()    
    #print(models)
    global comet_rerank, BERTScore_rerank, ChrF_rerank, TER_rerank, bleu_rerank
    # print("before post", comet_rerank)
    if request.method == "POST":
        bleu_rerank = request.form.get("bleu_rerank")
        TER_rerank = request.form.get("ter_rerank")
        comet_rerank = request.form.get("COMET_rerank")
        ChrF_rerank = request.form.get("ChrF_rerank")
        BERTScore_rerank = request.form.get("BERTScore_rerank")
        print(bleu_rerank)
        if bleu_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.bleu.desc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            return render_template("index.html", models = models, upload_times=upload_times, bleu_scores=bleu_scores)
        if TER_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.ter.asc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            return render_template("index.html", models = models, upload_times=upload_times, bleu_scores=bleu_scores)
        if comet_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.COMET.desc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            return render_template("index.html", models = models, upload_times=upload_times, bleu_scores=bleu_scores)
        if ChrF_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.chrF.desc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            return render_template("index.html", models = models, upload_times=upload_times, bleu_scores=bleu_scores) 
        if BERTScore_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.BERTScore.desc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            return render_template("index.html", models = models, upload_times=upload_times, bleu_scores=bleu_scores)
    models = TransformerModel.query.order_by(TransformerModel.bleu.desc()).all()
    # Prepare data for the graph (x-axis: upload time, y-axis: BLEU scores)
    upload_times = [model.year for model in models if model.year is not None]
    bleu_scores = [model.bleu for model in models if model.bleu is not None]    
    sorted_data = sorted(zip(upload_times, bleu_scores))
    # Unpack the sorted data into separate lists
    upload_times = [data[0] for data in sorted_data]
    bleu_scores = [data[1] for data in sorted_data]  
    # print(upload_times)
    # print(bleu_scores)  
    # Pass data to the template
    return render_template("index.html", models=models, upload_times=upload_times, bleu_scores=bleu_scores)
    # return render_template('index.html', models = models)

@views.route('/add', methods=['GET', 'POST'])
def add_model():  
    if request.method == "POST":
        #rank = request.form.get("rank")
        model_name = request.form.get("model_name")
        n_parameters = request.form.get("n_parameters")
        model_output = request.files["model_output"]
        open(fr"/Data/kamal/Leaderboard_website/datasets/uploaded_files/{model_name}_output", "w").close()
        model_output.save(fr"/Data/kamal/Leaderboard_website/datasets/uploaded_files/{model_name}_output")
        with open(fr"/Data/kamal/Leaderboard_website/datasets/uploaded_files/{model_name}_output", "r", encoding = "utf-8") as f:
            hypothesis = f.read()
        bleu = calculate_bleu(hypothesis)
        ter = calculate_TER(hypothesis)
        chrF = calculate_chrF(hypothesis)
        COMET = round(calculate_COMET(hypothesis), 2)
        BERTScore = round(calculate_BERTScore(hypothesis), 2)

        print("number of parameters", n_parameters)
        print("model name:", model_name)
        new_model = TransformerModel(model_name=model_name, n_parameters = n_parameters, bleu = bleu, ter = ter, chrF = chrF, COMET = COMET, BERTScore = BERTScore )  # Populate model attributes
        db.session.add(new_model)
        db.session.commit()
        return redirect(url_for(".home"))  # Redirect back to the index page
    return render_template("dev_add_model.html")




def calculate_bleu(hypothesis):
    # import pandas as pd
    # import numpy as np
    # import nltk
    # from nltk.translate.bleu_score import sentence_bleu

    # with open(r"/Data/kamal/Leaderboard_website/datasets/benchmarks/flores200_dataset/devtest/ben_Beng.devtest", 'r', encoding = "utf-8") as f:
    #     reference_text = f.read()

    # print("1")    
    # return sentence_bleu([reference_text], hypothesis)
    return 1.0

def calculate_TER(hypothesis):
    # from torchmetrics.text import TranslationEditRate
    # with open(r"/Data/kamal/Leaderboard_website/datasets/benchmarks/flores200_dataset/devtest/ben_Beng.devtest", 'r', encoding = "utf-8") as f:
    #     reference_text = f.read()
    # print("2")
    # ter = TranslationEditRate(normalize = True)
    # return ter([hypothesis],[[reference_text]])
    return 0

def calculate_chrF(hypothesis):
    # from torchmetrics.text import CHRFScore
    # with open(r"/Data/kamal/Leaderboard_website/datasets/benchmarks/flores200_dataset/devtest/ben_Beng.devtest", 'r', encoding = "utf-8") as f:
    #     reference_text = f.read()
    # print("3")
    # chrF = CHRFScore()
    # return chrF([hypothesis], [[reference_text]])
    return 1.0

def calculate_COMET(hypothesis):
    # from evaluate import load
    # with open(r"/Data/kamal/Leaderboard_website/datasets/benchmarks/flores200_dataset/devtest/ben_Beng.devtest", 'r', encoding = "utf-8") as f:
    #     reference_text = f.read()
    # with open(r"/Data/kamal/Leaderboard_website/datasets/benchmarks/flores200_dataset/devtest/eng_Latn.devtest", 'r', encoding = "utf-8") as g:
    #     source_text = g.read()
    # print("4")    
    # comet_metric = load('comet')
    # comet_score = comet_metric.compute(sources = [source_text], predictions = [hypothesis], references = [reference_text])
    # return comet_score["mean_score"]

    # from evaluate import load
    # comet_metric = load('comet')
    # source = ["Dem Feuer konnte Einhalt geboten werden", "Schulen und Kindergärten wurden eröffnet."]
    # hypothesis = ["The fire could be stopped", "Schools and kindergartens were open"]
    # reference = ["They were able to control the fire.", "Schools and kindergartens opened"]
    # comet_score = comet_metric.compute(predictions=hypothesis, references=reference, sources=source)    
    return 0.9234

def calculate_BERTScore(hypothesis):
    # from evaluate import load
    # bertscore = load("bertscore")
    # with open(r"/Data/kamal/Leaderboard_website/datasets/benchmarks/flores200_dataset/devtest/ben_Beng.devtest", 'r', encoding = "utf-8") as f:
    #     reference_text = f.read()    
    # print("5")
    # results = bertscore.compute(predictions=[hypothesis], references=[reference_text], lang="beng")
    # return results["f1"][0]
    return 1.0


#NEW


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')

        # Fetch the user from the database
        admin = Admin.query.filter_by(username = username).first()
        if admin and admin.check_password(password):
            session['admin'] = admin.id
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.admin_add_benchmark'))  # Redirect to a dashboard or home page
        else:
            flash('Login failed. Check your username and/or password', category='error')

    return render_template("login.html")


@views.route('/admin_add_benchmark', methods=['GET', 'POST'])
def admin_add_benchmark():
    if 'admin' not in session:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_benchmark':
            benchmark_name = request.form.get('benchmark_name')
            description = request.form.get('description')
            # Your logic to add benchmarking datasets
            benchmark_file = request.files['file']

            if not benchmark_name or not benchmark_file:
                flash('Benchmark name and dataset file are required!', category='error')
            else:
                # Save the file
                filename = secure_filename(benchmark_file.filename)
                file_path = os.path.join('/Data/kamal/Leaderboard_website/datasets/benchmarks', f"{benchmark_name}_benchmark")
                open(file_path,"w").close() #Creating the file
                benchmark_file.save(file_path)

                # Add benchmark to the database
                new_benchmark = Benchmark(name=benchmark_name, description=description, file_path=file_path)
                db.session.add(new_benchmark)
                db.session.commit()

                flash('Benchmark added successfully!', category='success')

# Clear the session and redirect to the home page
        session.pop('admin', None)
        session.pop('last_activity', None)
        return redirect(url_for('views.home'))

    return render_template("admin_add_benchmark.html")


# @views.route('/signup', methods=['GET', 'POST'])
# def sign_up():
    
#     return render_template("signup.html")
