from flask import Flask, render_template, request, Response
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def handle_index():
    return render_template('index.html')
    
@app.route('/process', methods=["POST"])
def handle_process():
    if request.method == 'GET':
        return 'Method not allowed', 405

    if 'file' not in request.files:
        return 'Invalid Arguments', 400 

    sells_file = request.files['file']

    if sells_file.filename == "":
        return 'Invalid Arguments', 400
    
    df = pd.read_excel(sells_file)
    
    min_deal_cost = int(request.form.get("number"))

    manager_bonus = []
    
    filtered = df[df['Сумма сделки'] >= min_deal_cost]
    
    deals_sums = filtered['Сумма сделки']
    for d in deals_sums:
        manager_bonus.append(int(d) * 0.1)
    
    filtered['Бонус менеджера'] = manager_bonus

    filtered.add
    
    return "", 200

if __name__ == '__main__':
    app.run()