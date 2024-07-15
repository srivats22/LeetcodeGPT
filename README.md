# LeetcodeGPT

# Disclaimer

LeetcodeGPT is not affiliated with Leetcode. This is just a side project that I developed on my own

# About The Project

If you are doing leetcode problems and stuck you might go to ChatGPT or Gemini and ask for help.
But you would also need to add more to the prompt to ensure it doesn't share code till you ask etc. And it may or may not have all the data points about the question.

This is where LeetcodeGPT comes in.

# How does it work

LeetcodeGPT was build using Streamlit. It starts by showing a simple form asking you to enter the problem URL, choose and programming language and then choose a model (Gemini, ChatGPT).

Once the form is submitted it then makes an API call to leetcodes api to get the content of the question which is kept in the current sessions memory so you can ask questions related to it.

# Get Started

LeetcodeGPT was build to run locally and won't be deployed anytime soon. Here is how you can run it on your own

1. Clone this repository:
   ```git clone https://github.com/srivats22/LeetcodeGPT.git```
2. Open the repository in you prefered code editor
3. run the following command: ```pip install -r requirements.txt```
4. open common.py and add either ChatGPT or Gemini API Key
5. run the following command to start the application: ```streamlit run app.py```
