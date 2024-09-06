# What the Food
- User gives food image that he/she will eat.
- Then our program then recommends food intake based on optimal nutrient intake.

## Task 1 - Detect foods from image

### Backbone model
- YOLO v8을 이용해서 fine-tuning 진행

### Dataset
- [AI Hub 한국 이미지(음식)](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=79)의 10개의 class, 10000장의 image

<center><img src = "./img/classes.png" width="50%" height = "50%"></center>

### Annotation
<center><img src = "./img/annotation.jpg" width="50%" height = "50%"></center>

- Dataset의 bounding box의 상태가 좋지 않아 human annotation 진행


## Task 2 - Propose food intake
### Get daily nutrient intake

- 이용자의 키, 몸무게, 나이, 성별,활동계수를 이용해서 하루 칼로리 권장 섭취량 측정
- 총 칼로리=기초 칼로리*활동계수
- 아래는 키, 몸무게, 나이, 성별을 이용한 기초칼로리 계산공식
```
male Basic_Kcal=88.362+(13.397*User_Input_Weight)+(4.799*User_Input_Height)-(5.677*User_Input_Age)
female Basic_Kcal=447.593+(9.247*User_Input_Weight)+(3.098*User_Input_Height)-(4.330*User_Input_Age)
```
- 한국인 기준 단백질, 지방, 탄수화물, 당류, 나트륨 권장 섭취량 반영
- 칼로리에 비례하여 탄/단/지 비율을 5:3:2로 통일, 당류는 성별에 따라 차등 나트륨은 2400mg으로 통일 


### Get nutrient of foods
- [전국통합식품영양성분정보(음식)표준데이터](https://www.data.go.kr/data/15100070/standard.do)

### Propose food intake
- 음식별 영양소 데이터와 개인별 영양소 권장 섭취량을 이용해서 음식별 섭취량을 추천
- 개인별 영양소 권장 섭취량은, 칼로리별 권장 섭취량을 측정결과를 그대로 반영
- 권장 섭취 영양소에 대한 최적화 알고리즘을 이용하여 개인별 음식 추천 섭취량을 계산


## 실행 방법
- 필요한 패키지를 설치
- 디렉토리 안에 먹은 이미지 파일 올리기

- 터미널에 다음을 입력하세요.

        python main.py

