import streamlit as st 
import pandas as pd 
import spacy 
from spacy import displacy
import streamlit.components.v1 as stc 
nlp = spacy.load("en_core_web_sm")
import neattext as nt 
import neattext.functions as nfx 
from collections import Counter
from textblob import TextBlob 
import seaborn as sns 
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud
import base64
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import docx2txt
import pdfplumber 
from PyPDF2 import PdfFileReader 



def text_analyzer(my_text):
	docx = nlp(my_text) 
	allData = [(token.text,token.shape_,token.pos_,token.tag_,token.lemma_,token.is_alpha,token.is_stop) for token in docx]
	df = pd.DataFrame(allData,columns = ['Token','Shape','PoS','Tag','Lemma','IsAlpha','Is_Stopword'])
	return df

def get_entities(my_text):
	docx = nlp(my_text)
	entities = [(entity.text, entity.label_) for entity in docx.ents]
	return entities

HTML_WRAPPER = """<div style ="overflow-x: auto ; border :1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div> """
def render_entites(raw_text):
	docx = nlp(raw_text)
	html = displacy.render(docx , style = "ent")
	html = html.replace("\n\n","\n")
	result = HTML_WRAPPER.format(html)
	return result

def get_most_common_tokens(my_text, num = 5):
	word_tokens = Counter(my_text.split())
	most_common_tokens = dict(word_tokens.most_common(num))
	return most_common_tokens

def get_sentiment(my_text):
	blob = TextBlob(my_text)
	sentiment = blob.sentiment
	return sentiment

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

def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text+=page.extractText()
	return all_page_text

def read_pdf2(file):
	with pdfplumber.open(file) as pdf:
		page = pdf.pages[0]
		return page.extract_text()

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

