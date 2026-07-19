# AI Projects
List of AI projects:

1) **Calendar Booking Assistant**
   - An Agentic AI app which books appointments according to the user's instructions. It access the calendar by connecting
     through the Google Calendar API.\
     Tech stack used:\
     Programming language: Python\
     Tools: Google Calendar API\
     LLM: Ollama\
     UI: Gradio\
     > **[!IMPORTANT]**\
     _**Please setup Google Calendar API beforehand to run the code or it will throw an error**_\
     _**Follow the instructions in the link below:**_\
     _**https://developers.google.com/workspace/calendar/api/quickstart/python**_

2) **SQL Assistant**
   - An Agentic AI app which generates SQL queries according to the user's instructions based on a predefined SQL database
     schema. It revises and improves it's own query before generating a response to the user.\
     Tech stack used:\
     Programming language: Python\
     Frameworks: LangChain, LangGraph\
     LLM: Ollama\
     UI: Gradio

3) **Code Generating Assistant**
   - An Agentic AI app which generates Python code according to the user's instructions. It revises and improves it's own
     code before generating a response to the user, and is also able to search the web if it does not know the code.\
     Tech stack used:\
     Programming language: Python\
     Frameworks: LangChain, LangGraph\
     Tools: Tavily API\
     LLM: Ollama\
     UI: Gradio

4) **Math Assistant**
   - An Agentic AI app which solve the user's math problems. It searches the web if it does not know how to solve a problem.\
     Tech stack used:\
     Programming language: Python\
     Frameworks: LangChain\
     Tools: Tavily API\
     LLM: Ollama\
     UI: Gradio

5) **RAG Chatbot**
   - A Chatbot which is able to search the web to answer the user's questions.\
     Tech stack used:\
     Programming language: Python\
     Frameworks: LangChain\
     Tools: Tavily API\
     LLM: Ollama\
     UI: Gradio

6) **Research Assistant**
   - An Agentic AI app which writes a research report according to the user's topic. It is able to search the web or connect
     to the ArXiv API to find relevant information, and also revise and improve it's own research before generating a
     response to the user.\
     Tech stack used:\
     Programming language: Python\
     Frameworks: LangChain, LangGraph\
     Tools: Tavily API, ArXiv API\
     LLM: Ollama\
     UI: Gradio

7) **Self-Learning Tic-Tac-Toe**
   - A Tic-Tac-Toe game which the opponent bot is able to learn from it's mistakes in the previous games and improves it's
     strategy by playing with human players. It starts dumb and easy to beat in the beginning, and gradually becomes smarter
     and harder to beat through the game rounds. It has 2 modes: Playing mode and Training mode. Playing mode is the
     original mode, while Training mode trains the opponent bot by competing it with another bot which takes random moves in
     order to accelerate it's training process so that users can immediately feel the difference in smartness of the
     opponent bot without manually playing against it for lots of rounds. There is also a feature for users to reset the
     opponent bot's training process.\
     Learning algorithm used: Q-Learning\
     Tech stack used:\
     Programming language: Python\
     Libraries: PyGame
