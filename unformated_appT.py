import streamlit as st 
import pandas as pd 

import streamlit.components.v1 as stc 

import neattext as nt 
import neattext.functions as nfx 


import seaborn as sns 
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud
import base64
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import docx2txt
from app_utils import *





def plot_wordcloud(my_text):
	my_wordcloud = WordCloud().generate(my_text)
	fig = plt.figure()
	plt.imshow(my_wordcloud, interpolation = 'bilinear')
	plt.axis('off')
	st.pyplot(fig)

def make_downloadable(data):
	csvfile = data.to_csv(index = False)
	b64=base64.b64encode(csvfile.encode()).decode()
	new_filename = "nlp_result_{}.csv".format(timestr)
	st.markdown("#### 📥 ⬇️ Download CSV File###")
	href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Clik here!!</a>'
	st.markdown(href,unsafe_allow_html = True)


def main():
	st.title("text analysis")
	menu = ["Home","NLP","About"]

	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Home":
		st.subheader("Home: Text Anakysis")
		raw_text = st.text_area("Enter your text here:")
		num_of_most_comm = st.sidebar.number_input("Most common tokens",5,15)
		if st.button("Analyze"):
			with st.beta_expander("Original Text"):
				st.write(raw_text)
			with st.beta_expander("Text Analysis"):
				toke_result_df = text_analyzer(raw_text)
				st.dataframe(toke_result_df)

			with st.beta_expander("Entities"):
				#entity_result = get_entities(raw_text)
				entity_result = render_entites(raw_text)
				stc.html(entity_result,height = 200, scrolling = True)

			col1,col2 = st.beta_columns(2)
			with col1:
				with st.beta_expander("Word stats"):
					st.info("Word Statistics")
					docx = nt.TextFrame(raw_text)
					st.write(docx.word_stats())

				with st.beta_expander("Top keywords"):
					st.info("Top Keywords")
					prcessed_text = nfx.remove_stopwords(raw_text.lower())
					keywords = get_most_common_tokens(prcessed_text, num_of_most_comm)
					st.write(keywords)

				with st.beta_expander("Sentiment"):
					sentiment_result = get_sentiment(raw_text)
					st.write(sentiment_result)

			with col2:
				with st.beta_expander("Plot word frequency"):
					fig = plt.figure()
					top_keywords = get_most_common_tokens(prcessed_text, num_of_most_comm)
					plt.bar(keywords.keys(),top_keywords.values())
					plt.xticks(rotation = 45)
					st.pyplot(fig)

				with st.beta_expander("Plot POS"):
					fig = plt.figure()
					sns.countplot(toke_result_df['PoS'])
					plt.xticks(rotation = 45)
					st.pyplot(fig)

				with st.beta_expander("Plot wordcloud"):
					plot_wordcloud(raw_text)

			with st.beta_expander("Download Text Analysis Results"):
				make_downloadable(toke_result_df)


	elif choice == "NLP":
		st.subheader("NLP Task")
		text_file = st.file_uploader("Upload Files", type = ['pdf','docx','txt'])#, accept_multiple_files=True
		num_of_most_comm = st.sidebar.number_input("Most common tokens",5,15)
		if text_file is not None:
			if text_file.type == 'application/pdf':
				raw_text = read_pdf(text_file)
				#st.write(raw_text)
			elif text_file.type == 'text/plain':
				raw_text = str(text_file.read(),'utf-8')
				#st.write(raw_text)
			else:
				raw_text = docx2txt.process(text_file)
				#st.write(raw_text)

			with st.beta_expander("Original Text"):
				st.write(raw_text)

			with st.beta_expander("Text Analysis"):
				toke_result_df = text_analyzer(raw_text)
				st.dataframe(toke_result_df)

			with st.beta_expander("Entities"):
					#entity_result = get_entities(raw_text)
				entity_result = render_entites(raw_text)
				stc.html(entity_result,height = 200, scrolling = True)

			col1,col2 = st.beta_columns(2)
			with col1:
				with st.beta_expander("Word stats"):
						st.info("Word Statistics")
						docx = nt.TextFrame(raw_text)
						st.write(docx.word_stats())

				with st.beta_expander("Top keywords"):
						st.info("Top Keywords")
						prcessed_text = nfx.remove_stopwords(raw_text.lower())
						keywords = get_most_common_tokens(prcessed_text, num_of_most_comm)
						st.write(keywords)

				with st.beta_expander("Sentiment"):
						sentiment_result = get_sentiment(raw_text)
						st.write(sentiment_result)

			with col2:
				with st.beta_expander("Plot word frequency"):
					try:
						fig = plt.figure()
						top_keywords = get_most_common_tokens(prcessed_text, num_of_most_comm)
						plt.bar(keywords.keys(),top_keywords.values())
						plt.xticks(rotation = 45)
						st.pyplot(fig)
					except:
						st.warning("Insufficient Data")

				with st.beta_expander("Plot POS"):
					try:
						fig = plt.figure()
						sns.countplot(toke_result_df['PoS'])
						plt.xticks(rotation = 45)
						st.pyplot(fig)
					except:
						st.warning("Insufficient Data")

				with st.beta_expander("Plot wordcloud"):
					try:
						plot_wordcloud(raw_text)
					except:
						st.warning("Insufficient Data")

			with st.beta_expander("Download Text Analysis Results"):
					make_downloadable(toke_result_df)

				


	else:
		st.subheader("About")



if __name__=="__main__":
	main()

