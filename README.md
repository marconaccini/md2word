# md2word

Convert Markdown documents into a Microsoft Word document using Pandoc.

![md2word](./md2word_window.png)

If you are not familiar with Markdown, I recommend visiting the website [Markdown Guide](https://www.markdownguide.org). 

If you are not familiar with Pandoc, I recommend visiting the website [Pandoc](https://pandoc.org).

# Installation

If you like **Git**, use the following command in your preferred folder: 

	git clone https://github.com/marconaccini/md2word.git
	
Otherwise, download the ZIP file and extract its contents in your preferred folder.

If you like, create a **venv** environment like this:

	python -m venv env
	
and then activate the environment with:

Linux:

	source env/bin/activate
	
Windows: 

	env\Scripts\activate.bat

**Then**, in that folder, run this command:

	pip install -r requirements.txt	

# Other requirements  

md2word needs to run with **Python 3** and Pandoc.

# How to run  

**On Windows:**

	py md2word2.py
	
**On Linux:**	

	python3 ./md2word2.py
