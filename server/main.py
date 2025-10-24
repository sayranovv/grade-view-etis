from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pydantic import BaseModel
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO, StringIO

matplotlib.use('Agg')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class AnalyseRequest(BaseModel):
    username: str
    password: str
    term: str

user_data = {}

def get_available_terms(session):
    url = "https://student.psu.ru/pls/stu_cus_et/stu.signs?p_mode=current"
    response = session.get(url, varify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    submenu = soup.find_all("div", class_="submenu")

    terms = []

    for block in submenu:
        for item in block.find_all("span", class_="submenu-item"):
            link = item.find("a")
            if link and "p_term=" in link.get("href", ""):
                href = link["href"]
                term_number = href.split("p_term=")[-1]
                if term_number.isdigit():
                    terms.append(int(term_number))
            else:
                text = item.get_text(strip=True)
                if "семестр" in text:
                    term_number = ''.join(ch for ch in text if ch.isdigit())
                    if term_number.isdigit():
                        terms.append(int(term_number))

    return sorted(set(terms))

def scrape_etis(username, password, term_filter):
    session = requests.Session()
    login_url = 'https://student.psu.ru/pls/stu_cus_et/stu.login'
    login_data = {
        'p_username': username,
        'p_password': password,
        'p_redirect': ''
    }
    response = session.post(login_url, data=login_data, varify=False)

    if 'Вход' in response.text:
        raise HTTPException(status_code=401, detail="Неверные данные")

    if term_filter is not None:
        terms = [term_filter]
    else:
        terms = get_available_terms(session)

    all_data = []
    for term in terms:
        grades_url = f'https://student.psu.ru/pls/stu_cus_et/stu.signs?p_mode=current&p_term={term}'
        response = session.get(grades_url, varify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        subjects = soup.find_all('h3')
        for subject in subjects:
            subject_name = subject.text.strip()
            table = subject.find_next('table', class_='common')
            if table:
                rows = table.find_all('tr')
                data = []
                for row in rows[2:]:
                    cols = row.find_all('td')
                    if len(cols) >= 9:
                        data.append([col.text.strip() for col in cols])

                if data:
                    df = pd.DataFrame(data, columns=[
                        'Тема', 'Тип работы', 'Тип контроля', 'Оценка', 'Проходной балл',
                        'Текущий балл', 'Макс. балл', 'Дата', 'Преподаватель'
                    ])
                    df['Предмет'] = subject_name
                    df['Семестр'] = term
                    all_data.append(df)

    if all_data:
        full_df = pd.concat(all_data, ignore_index=True)
        full_df['Оценка'] = pd.to_numeric(full_df['Оценка'], errors='coerce')
        full_df['Текущий балл'] = pd.to_numeric(full_df['Текущий балл'], errors='coerce')
        full_df['Макс. балл'] = pd.to_numeric(full_df['Макс. балл'], errors='coerce')

        return full_df
    else:
        raise ValueError("Данные не найдены. Проверьте семестры или вход.")


def analyze_data(df, term_filter=None):
    if term_filter is not None:
        df = df[df['Семестр'] == term_filter]

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')

    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_bytes = excel_buffer.getvalue()

    subject_stats = (
        df.groupby('Предмет')
        .agg({'Оценка': ['mean', 'count']})
        .reset_index()
    )
    subject_stats.columns = ['Предмет', 'Средний балл', 'Количество КТ']

    subject_stats['Средний балл'] = subject_stats['Средний балл'].fillna(0)

    subject_stats['Предмет с КТ'] = subject_stats.apply(
        lambda row: f"{row['Предмет']} ({int(row['Количество КТ'])} КТ)", axis=1
    )

    subject_totals = (
        df.groupby(['Семестр', 'Предмет'])['Оценка']
        .sum()
        .reset_index(name='Суммарный балл')
    )
    term_dynamics = (
        subject_totals.groupby('Семестр')['Суммарный балл']
        .mean()
        .reset_index(name='Средний балл')
    )

    term_dynamics['Средний балл'] = term_dynamics['Средний балл'].fillna(0)

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(subject_stats['Предмет с КТ'], subject_stats['Средний балл'])
    ax1.set_title('Средний балл за КТ по предметам')
    ax1.set_xlabel('Предмет')
    ax1.set_ylabel('Средний балл за КТ')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    png1_buffer = BytesIO()
    fig1.savefig(png1_buffer, format='png')
    png1_bytes = png1_buffer.getvalue()
    plt.close(fig1)

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(term_dynamics['Семестр'], term_dynamics['Средний балл'], marker='o')
    ax2.set_title('Динамика по семестрам')
    ax2.set_xlabel('Семестр')
    ax2.set_ylabel('Средний балл')
    ax2.grid(True)
    png2_buffer = BytesIO()
    fig2.savefig(png2_buffer, format='png')
    png2_bytes = png2_buffer.getvalue()
    plt.close(fig2)

    bar_data = {
        "labels": subject_stats['Предмет с КТ'].tolist(),
        "values": subject_stats['Средний балл'].apply(lambda x: float(x) if pd.notna(x) else 0.0).tolist()
    }
    line_data = {
        "labels": [int(x) for x in term_dynamics['Семестр'].tolist()],
        "values": term_dynamics['Средний балл'].apply(lambda x: float(x) if pd.notna(x) else 0.0).tolist()
    }

    return {
        "csv": csv_bytes,
        "xlsx": excel_bytes,
        "avg_grades_png": png1_bytes,
        "term_dynamics_png": png2_bytes,
        "bar_data": bar_data,
        "line_data": line_data
    }

@app.post('/api/login')
def login(request: LoginRequest):
    session = requests.Session()
    login_url = 'https://student.psu.ru/pls/stu_cus_et/stu.login'
    login_data = {
        'p_username': request.username,
        'p_password': request.password,
        'p_redirect': ''
    }
    response = session.post(login_url, data=login_data, varify=False)

    if 'Вход' in response.text:
        raise HTTPException(status_code=401, detail="Неверные данные")

    terms = get_available_terms(session)

    return {"success": True, "terms": terms}

@app.post('/api/analyze')
def analyze(request: AnalyseRequest):
    term_filter = int(request.term) if request.term else None
    try:
        df = scrape_etis(request.username, request.password, term_filter)
        results = analyze_data(df, term_filter)
        key = f"{request.username}_{term_filter if term_filter else 'all'}"
        user_data[key] = {
            "csv": results["csv"],
            "xlsx": results["xlsx"],
            "avg_grades": results["avg_grades_png"],
            "term_dynamics": results["term_dynamics_png"],
        }
        return {
            "success": True,
            "bar_data": results["bar_data"],
            "line_data": results["line_data"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/download/{file_type}')
def download(file_type: str, username: str = Query(...), term: str = Query(default='')):
    term_filter = int(term) if term else None
    key = f"{username}_{term_filter if term_filter else 'all'}"
    if key not in user_data:
        raise HTTPException(status_code=404, detail="Data not found. Perform analysis first.")

    if file_type == 'csv':
        return Response(content=user_data[key]['csv'], media_type="text/csv", headers={"Content-Disposition": "attachment; filename=grades.csv"})
    elif file_type == 'xlsx':
        return Response(content=user_data[key]['xlsx'], media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=grades.xlsx"})
    elif file_type == 'avg_grades':
        return Response(content=user_data[key]['avg_grades'], media_type="image/png", headers={"Content-Disposition": "attachment; filename=avg_grades.png"})
    elif file_type == 'term_dynamics':
        return Response(content=user_data[key]['term_dynamics'], media_type="image/png", headers={"Content-Disposition": "attachment; filename=term_dynamics.png"})
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")