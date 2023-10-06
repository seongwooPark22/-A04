import pandas as pd
from utility import *

class FileManager:

    def __init__(self):
        self.file_path = "./resource/TodoList_Datas.csv"
        try:
            self.df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            self.df = pd.DataFrame({
                "작업 이름": [], "마감 날짜": [], "반복": []
            })
            self.df.to_csv(self.file_path, index=False)

    def sort_todolist(self):
        self.df = self.df.sort_values(by='마감 날짜')
        self.df.to_csv(self.file_path, index=False)

    def get_data_by_index(self, index):
        list=self.df.loc[index].to_list()
        list[1]=change_date_to_this_week(list[1],list[2])
        return list

    def filter_todolist(self):
        years_df = self.df[(self.df['반복'] == "매년") & self.df['마감 날짜'].apply(filter_by_year)].copy()
        years_df['마감 날짜']=years_df['마감 날짜'].apply(change_date_to_this_week_year)
        month_df = self.df[(self.df['반복'] == "매달") & self.df['마감 날짜'].apply(filter_by_month)].copy()
        month_df['마감 날짜']=month_df['마감 날짜'].apply(change_date_to_this_week_month)
        week_df = self.df[(self.df['반복'] == "매주") & self.df['마감 날짜'].apply(filter_by_week)].copy()
        week_df['마감 날짜']=week_df['마감 날짜'].apply(change_date_to_this_week_weekday)
        none_df = self.df[(self.df['반복'] == "없음") & self.df['마감 날짜'].apply(filter_by_none)].copy()
        filter_df = pd.concat([years_df, month_df, week_df, none_df])
        filter_df['Index']=filter_df.index
        filter_df=filter_df.sort_values(by='마감 날짜')
        return filter_df

    def is_valid_file(self):
        for index, row in self.df.iterrows():
            row_data = {'index': index, 'data': row.to_dict()}
            if (is_valid_title(row_data['data']['작업 이름'])
                    and is_valid_date(row_data['data']['마감 날짜'])
                    and is_valid_repeat(row_data['data']['반복'])):
                continue
            else:
                print(f'오류: 데이터 파일 TodoList_Datas.csv에 문법 규칙과 의미 규칙에 위배되는 행이 {index + 2}행에 존재합니다.')
                return False
        return True

    def delete_todo(self, index):
        self.df.drop(index, inplace=True)
        self.df.to_csv(self.file_path, index=False)

    def edit_todo(self, index, col_name, data):##col name:'작업 이름'
        self.df.loc[index,col_name]=data
        self.df.to_csv(self.file_path, index=False)

    def add_todo(self, data):## data: [배열임]
        new_row=pd.DataFrame({'작업 이름':[data[0]],'마감 날짜':[data[1]],'반복':[data[2]]})
        self.df=pd.concat([self.df,new_row],ignore_index=True)##index 초기화
        self.df.to_csv(self.file_path, index=False)
