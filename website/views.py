
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory

# from main import app
from .models import TransformerModel, Model, Environment
from . import db
import os
from werkzeug.utils import secure_filename
from .models import Dataset, Users
import zipfile
import subprocess
import sys

views = Blueprint('views', __name__)

comet_rerank = False
BERTScore_rerank = False
TER_rerank = False
ChrF_rerank = False
bleu_rerank = False

@views.route('/home', methods=['GET', 'POST'])
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
    datasets = Dataset.query.all()
    lang_pairs = list(set([dataset.lang_pairs for dataset in datasets]))
    print([dataset.name for dataset in datasets])
    if request.method == "POST":
        bleu_rerank = request.form.get("bleu_rerank")
        TER_rerank = request.form.get("ter_rerank")
        comet_rerank = request.form.get("COMET_rerank")
        ChrF_rerank = request.form.get("ChrF_rerank")
        BERTScore_rerank = request.form.get("BERTScore_rerank")
        if bleu_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.bleu.desc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            zipfilepaths = [model.zip_file_path for model in models if model.zip_file_path is not None]
            return render_template("index.html", lang_pairs = lang_pairs,  datasets = datasets, models = models, upload_times=upload_times, bleu_scores=bleu_scores, zip_file_path = zipfilepaths)
        if TER_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.ter.asc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            zipfilepaths = [model.zip_file_path for model in models if model.zip_file_path is not None]
            return render_template("index.html", lang_pairs = lang_pairs, datasets = datasets, models = models, upload_times=upload_times, bleu_scores=bleu_scores, zip_file_path = zipfilepaths)
        if comet_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.COMET.desc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            zipfilepaths = [model.zip_file_path for model in models if model.zip_file_path is not None]
            return render_template("index.html", lang_pairs = lang_pairs, datasets = datasets, models = models, upload_times=upload_times, bleu_scores=bleu_scores, zip_file_path = zipfilepaths)
        if ChrF_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.chrF.desc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            zipfilepaths = [model.zip_file_path for model in models if model.zip_file_path is not None]
            return render_template("index.html", lang_pairs = lang_pairs, datasets = datasets, models = models, upload_times=upload_times, bleu_scores=bleu_scores, zip_file_path = zipfilepaths)
        if BERTScore_rerank == "true":
            models = TransformerModel.query.order_by(TransformerModel.BERTScore.desc()).all()
            upload_times = [model.year for model in models if model.year is not None]
            bleu_scores = [model.bleu for model in models if model.bleu is not None]    
            sorted_data = sorted(zip(upload_times, bleu_scores))
            upload_times = [data[0] for data in sorted_data]
            bleu_scores = [data[1] for data in sorted_data]
            zipfilepaths = [model.zip_file_path for model in models if model.zip_file_path is not None]
            return render_template("index.html", lang_pairs = lang_pairs, datasets = datasets, models = models, upload_times=upload_times, bleu_scores=bleu_scores, zip_file_path = zipfilepaths)
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
    zipfilepaths = [model.zip_file_path for model in models if model.zip_file_path is not None]
    return render_template("index.html", lang_pairs = lang_pairs, datasets = datasets, models = models, upload_times=upload_times, bleu_scores=bleu_scores, zip_file_path = zipfilepaths)
    # return render_template('index.html', models = models)


@views.route('/<path:filename>')
def serve_file(filename):
        return send_from_directory("..", filename)

def zip_files(zip_name, file_paths):
    with zipfile.ZipFile(zip_name, 'w') as zip_file:
        for file in file_paths:
            zip_file.write(file, os.path.basename(file))
    print(f'Created zip file: {zip_name}')

@views.route('/upload_model', methods = ['POST'])
def upload_model():
    benchmark = request.form.get('benchmark')
    model_name = request.form.get("model_name")
    n_parameters = request.form.get("n_parameters")
    model_output = request.files["model_output"]
    model_output.seek(0)
    modelText = model_output.read()
    modelText = str(modelText, 'utf-8').splitlines()
    with open(
            fr"datasets/uploaded_files/{benchmark}_output.txt",
            'w+', encoding='utf-8') as f:
        for items in modelText:
            f.write('%s\n' % items)
    f.close()
    print(benchmark)
    bleu = calculate_bleu(benchmark, modelText)
    ter = calculate_TER(benchmark, modelText)
    chrF = calculate_chrF(benchmark, modelText)
    COMET = round(calculate_COMET(benchmark, fr"datasets/uploaded_files/{benchmark}_output.txt"), 2)
    BERTScore = round(calculate_BERTScore(benchmark, modelText), 2)
    paper_name = request.form.get("paperName")
    publicationYear = request.form.get("publicationYear")
    code = request.form.get("codeLink")
    zipfilename = fr"datasets/benchmarks/{benchmark}.zip"
    dataset = Dataset.query.filter_by(name = benchmark).all()
    new_model = TransformerModel(model_name=model_name, benchmark = benchmark, n_parameters=n_parameters, bleu=bleu, ter=ter, chrF=chrF,
                                 COMET=COMET, BERTScore=BERTScore, paper = paper_name, year = publicationYear, code = code, zip_file_path = zipfilename, lang_pairs = dataset[0].lang_pairs)  # Populate model attributes
    db.session.add(new_model)
    db.session.commit()
    return redirect(url_for(".home"))


@views.route('/add_model', methods=['GET'])
def add_model():
    if 'user' in session:
        datasets = Dataset.query.all()
        print([dataset.name for dataset in datasets])
        return render_template("dev_add_model.html", datasets = datasets)
    else:
        return redirect(url_for('views.home'))

@views.route('/dataset_upload', methods = ['GET'])
def add_dataset():
    return render_template('modal.html')

@views.route('/upload', methods = ["POST"])
def upload_dataset():
    datasetfieldname = request.form.get("datasetFieldName")
    source_lang_code = request.form.get("sourceLang")
    target_lang_code = request.form.get("targetLang")
    source_file = request.files["sourceText"]
    target_file = request.files["targetText"]
    datasets = Dataset.query.all()
    datasets_name = [dataset.name for dataset in datasets]
    if datasetfieldname not in datasets_name:
        source_file.seek(0)
        target_file.seek(0)
        sourceText = source_file.read()
        targetText = target_file.read()
        sourceText = str(sourceText, 'utf-8').splitlines()
        targetText = str(targetText, 'utf-8').splitlines()
        sourceTextlen = len(sourceText)
        targetTextlen = len(targetText)
        if sourceTextlen == targetTextlen:
            with open(fr"datasets/benchmarks/{datasetfieldname}_sourceText.txt", 'w+') as f:
                for items in sourceText:
                    f.write('%s\n' % items)
            f.close()
            source_file_path = fr"datasets/benchmarks/{datasetfieldname}_sourceText.txt"
            with open(fr"datasets/benchmarks/{datasetfieldname}_targetText.txt", 'w', encoding='utf-8') as file:
                for item in targetText:
                    file.write(f"{item}\n")
            file.close()
            target_file_path = fr"datasets/benchmarks/{datasetfieldname}_targetText.txt"
            zipfilename = fr"datasets/benchmarks/{datasetfieldname}.zip"
            zip_files(zipfilename, [source_file_path, target_file_path])
            lang_pairs = source_lang_code + "-" + target_lang_code
            if sourceText or targetText:
                new_dataset =Dataset(name=datasetfieldname,  source_file_path=source_file_path, target_file_path = target_file_path, zip_file_path = zipfilename, lang_pairs = lang_pairs )
                print(new_dataset.source_file_path)
                print(new_dataset.target_file_path)
                print(new_dataset.name)
                db.session.add(new_dataset)
                db.session.commit()  # Populate model attributes
                return render_template('modal.html', message='Upload Successful')
            # Save files directly without creating empty files first
            # sourceText.save(
            #     fr"C:/Users/rochitranjan/PycharmProjects/Evaluation_leaderboard/datasets/benchmarks/{datasetfieldname}_sourceText.txt")
            # targetText.save(
            #     fr"C:/Users/rochitranjan/PycharmProjects/Evaluation_leaderboard/datasets/benchmarks/{datasetfieldname}_targetText.txt")
            # return render_template('modal.html', message='Upload Successful')
        else:
            return render_template('modal.html', message='Upload Failed')
    else:
        return render_template('modal.html', message='Upload Failed')

def calculate_bleu(benchmark, hypothesis_text):
    from sacrebleu.metrics import BLEU
    with open(fr"datasets/benchmarks/{benchmark}_targetText.txt", 'r', encoding = "utf-8") as f:
        reference_text = f.readlines()
    reference_text = list(map(lambda x:[x], reference_text))
    bleu = BLEU()
    bleu =  bleu.corpus_score(hypothesis_text, reference_text)
    return bleu.score

def calculate_TER(benchmark, hypothesis):
    from sacrebleu.metrics import TER

    # from torchmetrics.text import TranslationEditRate
    with open(fr"datasets/benchmarks/{benchmark}_targetText.txt", 'r', encoding = "utf-8") as f:
        reference_text = f.readlines()
    #
    ter = TER()
    ter = ter.corpus_score(hypothesis,[reference_text])
    #print(ter.score)
    return ter.score
    #return 0

def calculate_chrF(benchmark, hypothesis):
    #from torchmetrics.text import CHRFScore
    from sacrebleu.metrics import CHRF
    with open(fr"datasets/benchmarks/{benchmark}_targetText.txt", 'r', encoding = "utf-8") as f:
        reference_text = f.readlines()
    # print("3")
    #chrF = CHRFScore()
    # Instantiate the CHRF object
    chrf = CHRF()
    score = chrf.corpus_score(hypothesis,[reference_text])
    #print(score.score)
    return score.score
    #return chrF([hypothesis], [[reference_text]])
    #return 1.0

def calculate_COMET(benchmark, translation_outputs):
    #from evaluate import load
    import chardet
    import pandas as pd
    from comet import download_model, load_from_checkpoint
    # with open(fr"C:/Users/rochitranjan/PycharmProjects/Evaluation_leaderboard/datasets/benchmarks/{benchmark}_targetText.txt", 'r', encoding='utf-8') as f:
    #     reference_text = [line.strip() for line in f.readlines()]
    # with open(fr"C:/Users/rochitranjan/PycharmProjects/Evaluation_leaderboard/datasets/benchmarks/{benchmark}_sourceText.txt", 'r') as g:
    #     source_text = [line.strip() for line in g.readlines()]
    reference_path = fr"datasets/benchmarks/{benchmark}_targetText.txt"
    source_path = fr"datasets/benchmarks/{benchmark}_sourceText.txt"
    ref_rawdata = open(reference_path, 'rb').read()
    source_rawdata = open(source_path, 'rb').read()
    translation_rawdata = open(translation_outputs, 'rb').read() 

    ref_result = chardet.detect(ref_rawdata)
    src_result = chardet.detect(source_rawdata)
    trans_result = chardet.detect(translation_rawdata)
    ref_encoding = ref_result['encoding']
    src_encoding = src_result['encoding']
    trans_encoding = trans_result['encoding']
    ref_data = pd.read_table(reference_path, encoding=ref_encoding, header=None, names = ['ref'])
    src_data = pd.read_table(source_path, encoding=src_encoding, header=None, names = ['src'])
    trans_data = pd.read_table(translation_outputs, encoding=trans_encoding, header=None, names = ['mt'])
    data = pd.concat([ref_data, src_data, trans_data], axis = 1)
    data['src'] = data['src'].astype('str')
    data['ref'] = data['ref'].astype('str')
    data['mt'] = data['mt'].astype('str')
    list_of_data = data.to_dict(orient='records')
    
    model_path = download_model("Unbabel/wmt22-comet-da")
    model = load_from_checkpoint(model_path)
    model_output = model.predict(list_of_data, batch_size=8, gpus=0)
    # print("4")
    return model_output['system_score']

    # comet_metric = load('comet')
    # comet_score = comet_metric.compute(sources = source_text, predictions = hypothesis, references = reference_text)
    # return comet_score['mean_score']

    # from evaluate import load
    # comet_metric = load('comet')
    # source = ["Dem Feuer konnte Einhalt geboten werden", "Schulen und Kindergärten wurden eröffnet."]
    # hypothesis = ["The fire could be stopped", "Schools and kindergartens were open"]
    # reference = ["They were able to control the fire.", "Schools and kindergartens opened"]
    # comet_score = comet_metric.compute(predictions=hypothesis, references=reference, sources=source)
    #return 0.9234

def calculate_BERTScore(benchmark, hypothesis):
    from evaluate import load
    bertscore = load("bertscore")
    with open(fr"datasets/benchmarks/{benchmark}_targetText.txt", 'r', encoding = "utf-8") as f:
        reference_text = [line.strip() for line in f.readlines()]
    # # print("5")
    results = bertscore.compute(predictions=hypothesis, references=reference_text, lang="hi")
    print(results)
    return results["f1"][0]
    #return 1.0


#NEW

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = request.form.get('user_role')
        # Fetch the user from the database
        user = Users.query.filter_by(username = username).first()
        print(user.username)
        print(user.check_password(password))
        if user and user.check_password(password) and user_role == user.user_role:
            #session['admin'] = user.id
            #flash('Logged in successfully!', category='success')
            user.isLoggedIn = True
            db.session.add(user)
            db.session.commit()
            if 'user' not in session:
                session['user'] = username  # Store the username in the session
                session['role'] = user.user_role
            return render_template("login.html", message = "Login Successful")  # Redirect to a dashboard or home page
        else:
            return render_template("login.html", message = "Login Unsuccessful")

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


@views.route('/signup', methods=['GET'])
def sign_up():
    return render_template("signup.html")


@views.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password1')
    confirm_password = request.form.get('password2')
    firstname = request.form.get('firstName')
    if password == confirm_password:
        user = Users(username = username, email = email, password = password, first_name = firstname, user_role = "dev", isLoggedIn = True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session['dev'] = user.id
        flash('Sign Up successful!', category='success')
        return render_template("signup.html", message = "Sign Up Successful!")  # Redirect to a dashboard or home page
    else:
        print('Sign Up Failed')
        flash('Sign Up failed!', category='error')
        return render_template("signup.html",  message = "Sign Up Unsuccessful!")


@views.route('/logout', methods=['GET'])
def logout():
    username = session['user']
    # Fetch the user from the database
    user = Users.query.filter_by(username=username).first()
    if user:
        user.isLoggedIn = False
        db.session.add(user)
        db.session.commit()
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('views.home'))  # Redirect to home page


@views.route('/filter', methods=['POST'])
def filter():
    dataset = request.form.get('benchmark')
    selected_option = dataset
    datasets = Dataset.query.all()
    models = TransformerModel.query.filter_by(benchmark = dataset).all()
    print([model.model_name for model in models])
    upload_times = [model.year for model in models if model.year is not None]
    bleu_scores = [model.bleu for model in models if model.bleu is not None]
    sorted_data = sorted(zip(upload_times, bleu_scores))
    upload_times = [data[0] for data in sorted_data]
    bleu_scores = [data[1] for data in sorted_data]
    return render_template("index.html", selected_option = selected_option, datasets = datasets, models = models, upload_times=upload_times, bleu_scores=bleu_scores)


@views.route('/lang_filter', methods=['POST'])
def lang_filter():
    langpair = request.form.get('lang_filter')
    datasets = Dataset.query.all()
    lang_pairs = list(set([dataset.lang_pairs for dataset in datasets]))
    models = TransformerModel.query.filter_by(lang_pairs = langpair).all()
    print([model.model_name for model in models])
    upload_times = [model.year for model in models if model.year is not None]
    bleu_scores = [model.bleu for model in models if model.bleu is not None]
    sorted_data = sorted(zip(upload_times, bleu_scores))
    upload_times = [data[0] for data in sorted_data]
    bleu_scores = [data[1] for data in sorted_data]
    return render_template("index.html", lang_pairs = lang_pairs, lang_pair = langpair,  datasets = datasets, models = models, upload_times=upload_times, bleu_scores=bleu_scores)


@views.route('/model_upload', methods=['GET'])
def model_upload():
    return render_template("model_upload.html")

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Function to dynamically import the uploaded Python file
# def import_user_file(file_path: str):
#     spec = importlib.util.spec_from_file_location("model_inference", file_path)
#     model_inference = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(model_inference)
#     return model_inference


@views.route('/create_project', methods=['POST'])
def create_project():
    BASE_DIR =  os.path.join(os.getcwd(), "model_repository")
    model_name = request.form.get('model_name')
    model_folder = os.path.join(BASE_DIR, model_name)
    os.makedirs(model_folder, exist_ok=True)
    weights_file = request.files['model_weights']
    requirements_file = request.files['requirements_file']
    model_inference = request.files['model_inference']
    inference_script_files = request.files.getlist('model_scripts[]')
    weights_path = os.path.join(model_folder, weights_file.filename)
    requirements_path = os.path.join(model_folder, requirements_file.filename)
    model_inference_path = os.path.join(model_folder, model_inference.filename)
    weights_file.save(weights_path)
    requirements_file.save(requirements_path)
    model_inference.save(model_inference_path)
    inference_script_paths = []
    for inference_script_file in enumerate(inference_script_files):
        inference_script_path = os.path.join(model_folder, f'{inference_script_file[1].filename}')
        inference_script_file[1].save(inference_script_path)
        inference_script_paths.append(inference_script_path)
    inference_script_paths_string = ";".join(inference_script_paths)
    inference_model = Model(projectname=model_name, model_weights_path = weights_path, requirements_path=requirements_path, 
                            model_inference_path = model_inference_path, inference_script_paths = inference_script_paths_string) 
    db.session.add(inference_model)
    db.session.commit()
    return render_template("model_upload.html",  message = "Model Upload Successful!")

@views.route('/create_environment', methods=['GET'])
def create_environment():
    models = Model.query.all()
    return render_template("create_environment.html",  models = models)

# Function to read dependencies from requirements.txt
def read_requirements(requirements_path):
    dependencies = []
    try:
        with open(requirements_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    if '==' in line:
                        name, version = line.split('==')
                    else:
                        name, version = line, 'latest'
                    dependencies.append({'name': name, 'version': version})
    except FileNotFoundError:
        print("requirements.txt not found!")
    return dependencies

def custom_install(command, env_name, dependency):
    try:
        # Example: Create a virtual environment (make sure virtualenv is installed)
        command_to_run = f"conda run -n {env_name} {command}"
        print("command_to_run : ", command_to_run)
        # Run the command using subprocess
        subprocess.check_call(command_to_run, shell=True)
        print(f"{dependency} Dependency installed in the '{env_name}' environment!")
    except subprocess.CalledProcessError as e:
        print(f"Error during environment setup: {e}")


@views.route('/model_filter', methods=['POST'])
def model_filter():
    modelfilter = request.form.get('model_filter')
    env_name = request.form.get('env_name')
    python_version = request.form.get('python_version')
    models = Model.query.all()
    model_requirementpath = Model.query.filter_by(projectname = modelfilter).first()
    dependencies = read_requirements(model_requirementpath.requirements_path)
    return render_template("create_environment.html", models = models, modelfilter = modelfilter, dependencies=dependencies, env_name = env_name, python_version = python_version)

@views.route('/create_env', methods=['POST'])
def create_env():
    modelfilter = request.form.get('model_filter')
    env_name = request.form.get('env_name')
    python_version = request.form.get('python_version')
    create_conda_environment(env_name, python_version)
    commands = request.form.getlist('commands')
    dependency_name = request.form.getlist('dependency_name')
    dependency_dict = dict(zip(dependency_name, commands))
    print(dependency_dict)
    for dependency, command in dependency_dict.items():
        if command.strip() != '':  
            command = command + " --yes"
            custom_install(command, env_name, dependency)
        else:
            install_library(dependency, env_name)
    environment = Environment(modelname = modelfilter, environment_name = env_name) 
    db.session.add(environment)
    db.session.commit()
    return render_template("create_environment.html",  message = "Environment Created Successfully!")


# Function to install a library
def install_library(library_name, env_name):
    try:
        # Run the pip install command
        command_to_run = f"conda run -n {env_name} pip install {library_name}"
        print("command_to_run :", command_to_run)
        subprocess.check_call(command_to_run, shell = True)
        print(f"{library_name} Dependency installed in the '{env_name}' environment!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing {library_name}: {e}")

def create_conda_environment(env_name, python_version):
    try:
        # Command to create the conda environment
        print(python_version)
        print(env_name)
        command = [
            "conda", "create", "--name", env_name, f"python={python_version}", "--yes"
        ]
        # Run the command to create the environment
        subprocess.check_call(command)
        conda_int = [
            "conda", "init"
        ]
        subprocess.check_call(conda_int, shell = True)
        command = f"conda activate {env_name} && echo 'Environment {env_name} activated'"
    
    # Run the command to activate the environment and execute a simple echo command
        subprocess.run(command, shell=True, executable='/bin/bash')
        print(f"Conda environment '{env_name}' with Python {python_version} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the environment: {e}")


@views.route('/model_inference', methods=['GET'])
def model_inference():
    models = Model.query.all()
    return render_template("model_inference.html",  models = models)

def call_function_in_conda_env(conda_env, script_path, model_name, source_text):
    try:
        # Construct the command to activate the Conda environment and run the Python script
        command = f"""
        conda run -n {conda_env} && python {script_path} "{model_name}" "{source_text}"
        """
        # Use subprocess to execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        return result.stdout.strip()
    except Exception as e:
        print(f"An error occurred: {e}")


@views.route('/infer_model', methods=['POST'])
def infer_model():
    source_text = request.form.get('source_text')
    model_name = request.form.get('model_name')
    models = Model.query.all()
    model_requirementpath = Model.query.filter_by(projectname = model_name).first()
    env = Environment.query.filter_by( modelname = model_name).first()
    inference_file = model_requirementpath.model_inference_path
    conda_env = env.environment_name
    BASE_DIR =  os.path.join(os.getcwd(), "model_repository")
    model_folder = os.path.join(BASE_DIR, model_name)
    translation = call_function_in_conda_env(conda_env, inference_file, model_folder , source_text)
    return render_template("model_inference.html", source_sent = source_text, model_name = model_name,  models = models, translation = translation)


