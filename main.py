from flask import Flask, render_template, request, Response, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def handle_index():
    return render_template('index.html')
    
@app.route('/process', methods=["POST"])
def handle_process():
    if 'file' not in request.files:
        return 'Invalid Arguments', 400 

    sells_file = request.files['file']

    if sells_file.filename == "":
        return 'Invalid Arguments', 400
    
    df = pd.read_excel(sells_file)
    
    min_deal_cost = int(request.form.get("number"))

    filtered = df[df['Сумма сделки'] >= min_deal_cost].copy()

    filtered['Бонус менеджера'] = filtered['Сумма сделки'] * 0.10

    summary = (
        df.groupby('Менеджер')['Сумма сделки']
        .sum()
        .reset_index()
        .rename(columns={'Сумма сделки': 'Сумма продаж'})
    )

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered.to_excel(writer, sheet_name='Детализация', index=False)
        summary.to_excel(writer, sheet_name='Сводка', index=False)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='result.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if __name__ == '__main__':
    app.run()
