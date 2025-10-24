from getpass import getpass
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from http.client import HTTPException

def get_available_terms(session):
    url = "https://student.psu.ru/pls/stu_cus_et/stu.signs?p_mode=current"
    response = session.get(url)
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
    response = session.post(login_url, data=login_data)

    if 'Вход' in response.text:
        raise HTTPException(status_code=401, detail="Неверные данные")

    if term_filter is not None:
        terms = [term_filter]
    else:
        terms = get_available_terms(session)
        print(f"Найдены семестры: {terms}")

    all_data = []
    for term in terms:
        grades_url = f'https://student.psu.ru/pls/stu_cus_et/stu.signs?p_mode=current&p_term={term}'
        response = session.get(grades_url)
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

        print(full_df)

        return full_df
    else:
        raise ValueError("Данные не найдены. Проверьте семестры или вход.")


def analyze_data(df, term_filter=None, output_csv='grades.csv', output_excel='grades.xlsx'):
    if term_filter is not None:
        df = df[df['Семестр'] == term_filter]
        print(f"Анализ только для семестра {term_filter}")
    else:
        print("Анализ для всех семестров")

    df.to_csv(output_csv, index=False)
    df.to_excel(output_excel, index=False)
    print(f"Данные сохранены в {output_csv} и {output_excel}")

    subject_stats = (
        df.groupby('Предмет')
        .agg({'Оценка': ['mean', 'count']})
        .reset_index()
    )

    subject_stats.columns = ['Предмет', 'Средний балл', 'Количество КТ']

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

    print("\nСредний балл по предметам:")
    print(subject_stats)
    print("\nДинамика по семестрам (средний балл):")
    print(term_dynamics)

    plt.figure(figsize=(10, 6))
    plt.bar(subject_stats['Предмет с КТ'], subject_stats['Средний балл'])
    plt.title('Средний балл за КТ по предметам')
    plt.xlabel('Предмет')
    plt.ylabel('Средний балл за КТ')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('avg_grades.png')

    plt.figure(figsize=(8, 5))
    plt.plot(term_dynamics['Семестр'], term_dynamics['Средний балл'], marker='o')
    plt.title('Динамика по семестрам')
    plt.xlabel('Семестр')
    plt.ylabel('Средний балл')
    plt.grid(True)
    plt.savefig('term_dynamics.png')

    print("Графики сохранены как avg_grades.png и term_dynamics.png")

if __name__ == "__main__":
    username = input('Введите email ETIS: ')
    password = getpass('Введите пароль ETIS: ')

    term_choice = input("Введите номер семестра для анализа (или 'all' для всех): ")
    term_filter = int(term_choice) if term_choice != 'all' else None

    try:
        df = scrape_etis(username, password, term_filter)
        analyze_data(df, term_filter)
    except ValueError as e:
        print(e)