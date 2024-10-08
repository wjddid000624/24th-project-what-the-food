from detection import detection
from Food_DB import get_personel_info, get_recommended_intake
import cvxpy as cp
import pandas as pd
import copy

# gets input from user and calculate BMR(Basal Metabolic Rate)
personal_total_kcal, personal_daily_nutrient = get_personel_info()

while True:
    total_kcal = personal_total_kcal
    daily_nutrient = personal_daily_nutrient.copy()

    print("_____________________________________")
    print("오늘 몇끼를 드실건가요?")
    meals = int(input())

    for meal in range(meals):
        # get image file name
        print(f"\n오늘의 {meal+1}번째 식사의 사진의 파일 이름을 입력하세요. (ex. lunch.jpg)")
        file_name = input()

        # todo: Show image to user

        # detect food from image
        detected_food = detection(file_name)

        # get recommended intake of each food
        input_list, x = get_recommended_intake(total_kcal, daily_nutrient, detected_food, meals-meal)

        # Read Food_DB to get nutrient information of each food
        df = pd.read_csv('Food_DB.csv', encoding='utf-8')

        df = df[[
            'Fd_Name', 
            'Fd_Kcal', 
            'Fd_Protein', 
            'Fd_fat', 
            'Fd_cbhyd', 
            'Fd_sugar', 
            'Fd_natrium' ]]

        nutrient_type = ['칼로리', '단백질', '지방', '탄수화물', '당류', '나트륨']

        nutrient_meal = {
            '칼로리': 0,  # 칼로리
            '단백질': 0,  # 단백질
            '탄수화물': 0,  # 탄수화물
            '지방': 0,  # 지방
            '당류': 0,  # 당류
            '나트륨': 0,  # 나트륨
        }

        # print recommended intake of each food        
        print(f'\n오늘 {meal+1}번째 끼의 권장 섭취량은 다음과 같습니다.')
        for i in range(len(input_list)):
            if x.value[i][0] < 0.01:
                x.value[i][0] = 0
            print('{0}의 권장 섭취량은 {1:0.0f}g 입니다.'.format(input_list[i], x.value[i][0] * 100))

            # calculate nutrient_meal
            nutrient_meal['칼로리'] += x.value[i][0] * df.loc[df['Fd_Name'] == input_list[i]]['Fd_Kcal'].values[0]
            nutrient_meal['단백질'] += x.value[i][0] * df.loc[df['Fd_Name'] == input_list[i]]['Fd_Protein'].values[0]
            nutrient_meal['탄수화물'] += x.value[i][0] * df.loc[df['Fd_Name'] == input_list[i]]['Fd_cbhyd'].values[0]
            nutrient_meal['지방'] += x.value[i][0] * df.loc[df['Fd_Name'] == input_list[i]]['Fd_fat'].values[0]
            nutrient_meal['당류'] += x.value[i][0] * df.loc[df['Fd_Name'] == input_list[i]]['Fd_sugar'].values[0]
            nutrient_meal['나트륨'] += x.value[i][0] * df.loc[df['Fd_Name'] == input_list[i]]['Fd_natrium'].values[0]

        # update total_kcal and daily_nutrient
        total_kcal -= nutrient_meal['칼로리']
        daily_nutrient['Fd_Protein(g)'] -= nutrient_meal['단백질']
        daily_nutrient['Fd_Cbhyd(g)'] -= nutrient_meal['탄수화물']
        daily_nutrient['Fd_Fat(g)'] -= nutrient_meal['지방']
        daily_nutrient['Fd_Sugar(g)'] -= nutrient_meal['당류']
        daily_nutrient['Fd_Natrium(mg)'] -= nutrient_meal['나트륨']
        
        print(f'\n오늘 {meal+1}번째 끼의 권장 섭취량을 지켰을 때 섭취 영양소량은 다음과 같습니다.')
        print(*[f'{key}: {value}' for key, value in nutrient_meal.items()], sep=', ')

        
        # # test print
        # print("after", total_kcal, daily_nutrient)

    print("프로그램을 종료하시겠습니까? (y/n)")
    end = input()
    if end == 'y':
        break