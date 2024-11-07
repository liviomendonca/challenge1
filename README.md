# Python Challenge - Continuous Learning

Develop an interactive chatbot that not only answers questions but also learns and adapts based on user interactions. The chatbot should store relevant information on a specific topic only when the user provides accurate information (it should not accept false corrections) or when it relates to preferences, such as preferring a more formal tone.


# main.py

Groq chatbot using RAG. Run it with `streamlit run main.py`.
It also prints in the terminal some of the "chain of thought" of the agent.


# no_rag_chatbot.py

Simpler Groq chatbot. This version doesn't rely on RAG nor agents.
I keep this version for comparison reasons.


# rag.py

I included the vector database files ready to use to faster initialization but you can (re-)generate it for the same data (i.e. `shrek_script.md`) or any file you want. Keep in mind it accepts only `.md` files but it's configurable.
