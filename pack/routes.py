from flask import render_template, request, url_for, send_from_directory
from pack import app, Nonogram_Code
from pack import Divisibility_Rule_Generator as drg
import os


@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/nono', methods=['POST', 'GET'])
def non_page():
    if request.method == 'POST':
    #    size = int(request.form['dimension'])
    #    grid = Nonogram_Code.puzzle_gen(size)
        return render_template('nonogram.html')
    else:
        return render_template('nonogram.html')


@app.route('/div_rule', methods=['POST', 'GET'])
def div_rule():
    if request.method == 'POST':
        num = int(request.form['number'])
        rule = drg.better_gen(num)
        rule = rule.split('\n')
        return render_template('rule_page.html', str=rule)
    else:
        return render_template('div_rule.html')

@app.route('/factor', methods=['POST', 'GET'])
def factor():
    if request.method == 'POST':
        num = int(request.form['number'])
        factorization =  drg.nice_latex(drg.prime_fac(num, drg.plist))
        return render_template('factorization.html', num=num, fac=factorization)
    else:
        return render_template('factor.html')


@app.route('/cv')
def cv():
    workingdir = os.path.abspath(os.getcwd())
    return send_from_directory(workingdir, 'CV (1).pdf')