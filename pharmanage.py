import csv
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tkinter import font as tkFont
import pandas as pd
import datetime

# Original Code from by JW.Seo pharmacist
'''
Minor update added by ssrihappy
V_0.1

-입력 칸을 단순화 하고 신규환자 입력 시 환자번호 및 최초내방일을 자동 입력하도록 개선하였습니다.
-신규환자 등록 및 기존환자 업데이트를 분리하여 중복 및 잠재적 오류를 개선하였습니다.
-exe file로 build하여 Window 운영체제에서 일반 사용자가 사용할 수 있도록 하였습니다.
-아이콘을 신규로 적용하였습니다.

'''


today = str(datetime.datetime.now().strftime('%Y-%m-%d'))


# 설정 파일 경로
config_file = 'config.txt'

def save_config(path):
    """ 설정 파일에 파일 경로 저장 """
    with open(config_file, 'w') as f:
        f.write(path)

def load_config():
    """ 설정 파일에서 파일 경로 불러오기 """
    try:
        with open(config_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
        


root = Tk()
root.title("팜매니지(Pharmanage) 약국 고객 관리 프로그램 V_0.1")
root.geometry("1200x1000")
style = ttk.Style()
style.theme_use('winnative')


# 변수 선언 부분
cust_num = StringVar()
cust_name = StringVar()
birthdate = StringVar()
contact = StringVar()
consult_date = StringVar()
search_var = StringVar()
selected_row_index = None  # 선택된 행의 인덱스를 저장하는 전역 변수
file_name = None  # 파일 이름을 저장하는 전역 변수
file_name = load_config()  # 프로그램 시작 시 파일 경로 불러오기


content_frame = Frame(root)
content = Text(content_frame, width=int(30*1.5), height=35)
content_scroll = Scrollbar(content_frame, command=content.yview)
content['yscrollcommand'] = content_scroll.set
content.pack(side='left')
content_scroll.pack(side='right', fill='y')

disease_frame = Frame(root)
disease = Text(disease_frame, width=int(30*1.5), height=10)
disease_scroll = Scrollbar(disease_frame, command=disease.yview)
disease['yscrollcommand'] = disease_scroll.set
disease.pack(side='left')
disease_scroll.pack(side='right', fill='y')

prescription_frame = Frame(root)
prescription = Text(prescription_frame, width=int(30*1.5), height=10)
prescription_scroll = Scrollbar(prescription_frame, command=prescription.yview)
prescription['yscrollcommand'] = prescription_scroll.set
prescription.pack(side='left')
prescription_scroll.pack(side='right', fill='y')

prescription_content_frame = Frame(root)
prescription_content = Text(prescription_content_frame, width=int(30*1.5), height=10)
prescription_content_scroll = Scrollbar(prescription_content_frame, command=prescription_content.yview)
prescription_content['yscrollcommand'] = prescription_content_scroll.set
prescription_content.pack(side='left')
prescription_content_scroll.pack(side='right', fill='y')

notes_frame = Frame(root)
notes = Text(notes_frame, width=int(30*1.5), height=7)
notes_scroll = Scrollbar(notes_frame, command=notes.yview)
notes['yscrollcommand'] = notes_scroll.set
notes.pack(side='left')
notes_scroll.pack(side='right', fill='y')



def load_csv():
    if file_name:
        df = pd.read_csv(file_name, encoding='cp949')
        df = df.fillna('')  # NaN 값을 공백으로 대체
        return df
    else:
        return pd.DataFrame()  # 파일 이름이 없는 경우 빈 데이터프레임 반환


# 이벤트 바인딩
def on_right_click(event):
    # 우클릭 이벤트를 처리하는 함수
    pass
    
# 모든 관련 위젯에 대해 우클릭 이벤트 바인딩
content.bind("<Button-3>", on_right_click)
disease.bind("<Button-3>", on_right_click)
prescription.bind("<Button-3>", on_right_click)
prescription_content.bind("<Button-3>", on_right_click)
notes.bind("<Button-3>", on_right_click)



def search():
    df = load_csv()
    search_results.delete(0, END)
    search_text = search_var.get()
    results = df[df.applymap(lambda x: search_text in str(x)).any(axis=1)]
    result_dict = {}
    for idx, row in results.iterrows():
        for col in results.columns:
            if search_text in str(row[col]):
                key = row['고객명 (김마음)'] + ' ' + str(row['최초방문일 (자동입력)'])  # 고객명과 최초방문일를 연결하여 고유한 키 생성
                if key not in result_dict:
                    result_dict[key] = []
                result_dict[key].append(col)
    for name_date, cols in result_dict.items():
        search_results.insert(END, f"{name_date} ({', '.join(cols)})")

def show_info(event):
    global selected_row_index
    df = load_csv()
    selected = search_results.curselection()
    if not selected:
        return
    selected_name_date = search_results.get(selected).split(' (열:')[0]
    selected_name, selected_date = selected_name_date.split(' ')[:2]
    selected_df = df[(df['고객명 (김마음)'] == selected_name) & (df['최초방문일 (자동입력)'] == selected_date)]
    if selected_df.empty:
        print(f"{selected_name_date}에 해당하는 고객명과 최초방문일가 데이터에 없습니다.")
        return
    selected_row_index = selected_df.index[0]
    info = selected_df.iloc[0]

    # 기존의 텍스트 필드에 정보 표시
    cust_num.set(info['고객번호 (자동입력)'])
    cust_name.set(info['고객명 (김마음)'])
    birthdate.set(info['생년월일 (930117-1)'])
    contact.set(info['연락처 (01012342345)'])
    consult_date.set(info['최초방문일 (자동입력)'])
    content.delete("1.0", "end")
    content.insert("1.0", info['상담내용'])
    disease.delete("1.0", "end")
    disease.insert("1.0", info['질환/질병 정보'])
    prescription.delete("1.0", "end")
    prescription.insert("1.0", info['의약품/영양제 정보'])
    prescription_content.delete("1.0", "end")
    prescription_content.insert("1.0", info['임상증상'])
    notes.delete("1.0", "end")
    notes.insert("1.0", info['기타 참고사항'])

def update_csv():
    global selected_row_index
    df = load_csv()
    if selected_row_index is None:
        print("선택된 고객 정보가 없습니다.")
        return

    # 입력된 정보로 데이터 프레임 업데이트
    df.at[selected_row_index, '고객번호 (자동입력)'] = cust_num.get()
    df.at[selected_row_index, '고객명 (김마음)'] = cust_name.get()
    df.at[selected_row_index, '생년월일 (930117-1)'] = birthdate.get()
    df.at[selected_row_index, '연락처 (01012342345)'] = contact.get()
    df.at[selected_row_index, '최초방문일 (자동입력)'] = consult_date.get()
    df.at[selected_row_index, '상담내용'] = content.get("1.0", "end-1c")
    df.at[selected_row_index, '질환/질병 정보'] = disease.get("1.0", "end-1c")
    df.at[selected_row_index, '의약품/영양제 정보'] = prescription.get("1.0", "end-1c")
    df.at[selected_row_index, '임상증상'] = prescription_content.get("1.0", "end-1c")
    df.at[selected_row_index, '기타 참고사항'] = notes.get("1.0", "end-1c")

    # 변경된 내용을 CSV 파일에 저장
    df.to_csv('customer_data.csv', index=False, encoding='cp949')

def read_No():
    df = load_csv()
    new_num = (len(df)+1)
    return new_num

# 검색어 입력 칸 생성
search_entry = ttk.Entry(root, textvariable=search_var, width=40)
search_entry.grid(row=0, column=1, padx=10)
ttk.Button(root, text="기존고객 검색(2-1)", command=search).grid(row=0, column=2, padx=(5, 10), pady=1)

# 엔터 키 이벤트 바인딩
search_entry.bind('<Return>', lambda event: search())

# 검색 결과 리스트
search_results = Listbox(root, width=80)
search_results.grid(row=1, column=1, padx=10, pady=(1, 50), columnspan=2)
search_results.bind('<Double-1>', show_info)

fields = [('고객번호 (자동입력)', cust_num), ('고객명 (김마음)', cust_name), ('생년월일 (930117-1)', birthdate), ('연락처 (01012342345)', contact), ('최초방문일 (자동입력)', consult_date)]
for i, (text, var) in enumerate(fields):
    ttk.Label(root, text=text).grid(row=i+2, column=0, padx=10, pady=1)
    ttk.Entry(root, textvariable=var, width=60).grid(row=i+2, column=1, padx=10, pady=1)

ttk.Label(root, text="상담내용").grid(row=len(fields)+2, column=0, padx=10, pady=1)
content_frame.grid(row=len(fields)+2, column=1, rowspan=4, padx=10, pady=1)

ttk.Label(root, text="질환/질병 정보").grid(row=len(fields)+2, column=2, padx=10, pady=1)
disease_frame.grid(row=len(fields)+2, column=3, padx=10, pady=1)

ttk.Label(root, text="의약품/영양제 정보").grid(row=len(fields)+3, column=2, padx=10, pady=1)
prescription_frame.grid(row=len(fields)+3, column=3, padx=10, pady=1)

ttk.Label(root, text="임상증상").grid(row=len(fields)+4, column=2, padx=10, pady=1)
prescription_content_frame.grid(row=len(fields)+4, column=3, padx=10, pady=1)

ttk.Label(root, text="기타 참고사항").grid(row=len(fields)+5, column=2, padx=10, pady=1)
notes_frame.grid(row=len(fields)+5, column=3, padx=10, pady=1)

def clear_all():
    num = read_No()
    cust_num.set(str(num))
    cust_name.set('')
    birthdate.set('')
    contact.set('')
    consult_date.set(today)
    content.delete("1.0", "end")
    disease.delete("1.0", "end")
    prescription.delete("1.0", "end")
    prescription_content.delete("1.0", "end")
    notes.delete("1.0", "end")
    
def open_file():
    global file_name
    file_path = filedialog.askopenfilename(filetypes=[("CSV 파일", "*.csv")])
    if file_path:
        file_name = file_path
        file_path_label.config(text="DB 파일: " + file_name)
        save_config(file_name)  # 설정 파일에 파일 경로 저장

# 파일 경로 라벨 및 파일 열기 버튼
file_path_label = ttk.Label(root, text="DB 파일: " + (file_name if file_name else ""))
file_path_label.grid(row=0, column=3, padx=10)
ttk.Button(root, text="DB 파일 열기", command=open_file).grid(row=0, column=4, padx=(5, 10), pady=1)

def save_new_customer():
    # 입력된 정보 가져오기
    
    new_cust_num = cust_num.get()
    new_cust_name = cust_name.get()
    new_birthdate = birthdate.get()
    new_contact = contact.get()
    new_consult_date = consult_date.get()
    new_content = content.get("1.0", "end-1c")
    new_disease = disease.get("1.0", "end-1c")
    new_prescription = prescription.get("1.0", "end-1c")
    new_prescription_content = prescription_content.get("1.0", "end-1c")
    new_notes = notes.get("1.0", "end-1c")

    # CSV 파일에 새로운 고객 정보 추가
    with open('customer_data.csv', 'a', newline='', encoding='cp949') as file:
        writer = csv.writer(file)
        writer.writerow([new_cust_num, new_cust_name, new_birthdate, new_contact,
                         new_consult_date, new_content, new_disease, new_prescription,
                         new_prescription_content, new_notes])

# 신규 고객 저장 버튼 생성
ttk.Button(root, text="신규 고객 저장(1-2)", command=save_new_customer).grid(row=len(fields)+6, column=1, padx=10, pady=1)



# 업데이트 버튼 생성
ttk.Button(root, text="기존고객 업데이트(2-2)", command=update_csv).grid(row=len(fields)+6, column=2, padx=10, pady=1)

# 모든 필드 비우기 버튼 생성
ttk.Button(root, text="신규등록 - 초기화(1-1)", command=clear_all).grid(row=len(fields)+6, column=0, padx=10, pady=1)




root.mainloop()

