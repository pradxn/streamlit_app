#import required libraries
from pyexpat import model
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

#load pickle file
pickle_in=open("chrome_reviews.pkl","rb")
model=pickle.load(pickle_in)

#load csv file
data = pd.read_csv('chrome_reviews.csv')

# create PorterStemmer
ps=PorterStemmer()

#classify data into dependent & independent variables
def Review_classification(dataframe):
	df=cleaning_data(dataframe)
	X=df['Text'].values
	y_pred=model.predict(X)
	return y_pred
    
#cleaning data
def cleaning_data(data_set):
	corpus=[]
	for i in range(0,len(data_set)):
		#remove all non-words characters
		review=re.sub("[^a-zA-Z]"," ",str(data_set['Text'][i]))

		#convert into lowercase
		review=review.lower()

		#split review into words
		review=review.split()

		#stemming
		review = [ps.stem(word) for word in review if not word in stopwords.words('english')]

		#join words back to make sentences
		review=' '.join(review)

		# list of reviews
		corpus.append(review)
      
	for i in range(len(corpus)):
		data_set['Text'][i]=corpus[i]

	return data_set
    
#main app
def main():
	st.title('App rating & review classifier')
	st.write('Identify the reviews where the semantics of review text does not match rating.')
	st.write('Upload a csv file of following format for using the app and click on Classify')
	st.write(data.head())
	
	html_temp="""
    <div style="background-color:tomato;padding:10px;">
    <h2 style="color:white;text-align:center;">App rating & review classifier</h2>
    </div>
    """
	st.markdown(html_temp,unsafe_allow_html=True)
	
	st.subheader("Upload CSV file to classify reviews")
	filename = st.file_uploader("Upload a file", type=("csv"))
	if filename is not None:
		try:
			if st.button('Classify'):
				test_data=pd.read_csv(filename)
				ref_data=test_data.copy(deep=True)
				y_pred=Review_classification(test_data)
				review_ID=[]
				for i in range(len(y_pred)):
					if ( (y_pred[i]==1)and (ref_data['Star'][i]<2)):
						review_ID.append(ref_data['ID'][i])
				result=ref_data[ref_data['ID'].isin(review_ID)]
				result.reset_index(inplace=True)
				result=result.iloc[:,1:]
				st.subheader('Classified Reviews')
				st.write('Reviews where the semantics of review text does not match rating.')				
				st.write(result)
		except:
			st.error('Please choose a file')
			
if __name__=='__main__':
	main()