# sr-GUI
created by Joy (Yun-Hsuan) Jen

Flask Front End and python back end application for analyzing speech errors.
- First Version : Term Project for UIUC CS410 Fall 2018 Text Information Systems

### Requirements: 
- flask
- pyyaml
- nltk
- numpy
- SpeechRecognition
- metaphone

Make sure you have all the requirements listed above. You can install the packages using > pip install
You should have **Python** 3 installed as well

### Installing: 
- git clone https://github.com/joyyyjen/sr-GUI/

### Execute:
In sr-GUI directory, run python3 ./run.py. 
It will start serving Flask app "flask_site", and a localhost link will be given. 
Open the link and now you can use the Front End WebUI Error Analyzer. 

### How does it Work?
- This program accept a recognition zipfile. 
- In the backend, speech recognition will first recognize the audios and output recognition.txt.
- Giving this recognition.txt and a provided trans.txt, the analyzer will start word error rate alignment.
- Using the word error rate alignment, the SR error analyzer categorize errors.
- In the frontend, it prints a pie chart showing the coverage of each error, a table which listed the count, frequency and subclasses of the error type, and a txt reference of all errors. 

### Recognition Zipfile:
- If you are using your own recognition zipfile, please make sure all the audio file is record at a sample rate of 16 KHz
- Include a fileid file and a transcription file
- The file structure should look like this:
  - 84-121123-0000.wav
  - 84-121123-0001.wav
  - ...
  - fileid.txt
  - trans.txt

### Note: 
- It might takes around 2 mins to recognize 30 audios and output the analysis. Please be patient. 
- A test set is provided. It's called 'test-set.zip'. 


