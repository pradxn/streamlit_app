from python:3.8.9
CMD mkdir /chrome_reviews
copy . /chrome_reviews
WORKDIR /chrome_reviews
expose 8051
run pip install -r requirements.txt
CMD streamlit run predict_reviews.py
