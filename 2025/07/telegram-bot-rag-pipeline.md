---
author: "Bimal Gharti Magar"
title: "Build a Smarter Telegram Bot: Integrating a RAG Pipeline for FAQ Answering"
description: How to create a telegram bot and integrate a RAG Pipeline for FAQ Answering.
date: 2025-11-04
tags:
- python
- telegram
- llm
- rag
- langchain
- programming
---

![A top-down view of flowers with light pink petals and black centers.](/blog/2025/07/invoice-generator-api-c-sharp/black-and-pink-flowers.webp)

<!-- Photo by Seth Jensen, 2025. -->

In this post, we will show you how to build an intelligent FAQ bot using Python and the **Telegram Bot API**. We'll go beyond simple commands by integrating a **Retrieval-Augmented Generation** (RAG) pipeline with LangChain.

This RAG pipeline lets our bot pull information from a custom knowledge base (in our case, a simple `faqs.json` file) and use a **local** Large Language Model (LLM) through **Ollama** to generate accurate answers. The best part? This approach, which works great with interfaces like **Open Web UI**, gives you full control over your models and data with zero API costs.

### What is Telegram?

You've probably heard of [Telegram](https://telegram.org/)—it's a popular, cloud-based instant messaging app. It’s fast, works everywhere (mobile, web, and desktop), and has powerful features like huge group chats and easy file sharing.

One of its most powerful features for developers is the **Telegram Bot API**, an open platform that allows anyone to build and integrate automated applications (like ours!) directly into the chat interface.

### A Warning on Privacy and Encryption

Before we build our bot, it is critical to understand how Telegram handles encryption, as it directly impacts user privacy.

- **Cloud Chats (The Default)**: All standard chats, group chats, and **all bot interactions** are "Cloud Chats." These use server-client encryption. This means your messages are encrypted between your device and Telegram's servers, and then stored (encrypted) on their servers. This is what allows you to access your chat history from any device. However, **Telegram itself holds the encryption keys** and can access this data.

- **Secret Chats (Manual)**: Telegram also offers "Secret Chats," which are end-to-end encrypted (E2EE). In this mode, only you and the recipient can read the messages. Telegram has no access. However, **bots cannot operate in Secret Chats**.

**What this means for our bot**: Any message a user sends to our bot is a "Cloud Chat" and is **not end-to-end encrypted**. The data is accessible to Telegram and will be processed in plain text by our bot.py script on our server.
 
For this reason, you should never build a bot that asks for, or encourage users to send, highly sensitive private data such as passwords, financial information, or social security numbers. Always treat bot conversations as non-private.

### What is Retrieval-Augmented Generation (RAG)?

At its core, Retrieval-Augmented Generation (RAG) is a technique that makes Large Language Models (LLMs) smarter by connecting them to external, private knowledge.

- The Problem: An LLM like llama3 only knows the information it was trained on. It has no access to your company's internal FAQs, new documents, or any private data.
 
- The Solution (RAG): RAG solves this in two steps:
 
    - 1. Retrieve: When you ask a question, the system first retrieves relevant information from your own knowledge base (for us, our faqs.json file).
 
    - 2. Augment: It then augments the LLM's prompt by pasting that retrieved information in as context, along with your original question.
 
In short, instead of just asking the bot "What's the shipping policy?", we're effectively asking, "Based on this specific text: '...We offer standard shipping...' — what is the shipping policy?" This forces the LLM to base its answer on our facts, not its own general knowledge, making the response accurate and reliable.

### What you’ll build
- Telegram bot
- faqs.json knowledge base
- RAG pipeline with local embeddings (FAISS) + LLM (OpenWebUI)
 
### Prerequisites
You’ll need: Python 3.12+, a Telegram bot token (from BotFather), and access to an LLM via a locally hosted OpenWebUI instance (OpenAI-compatible API).
### Setting up the Project for Telegram Bot
 
`uv` is a high-performance Python package manager, so we'll use it to set up our project. If you don't have it installed, you can get it with or visit the [site](https://docs.astral.sh/uv/getting-started/installation/) for installation steps
```bash
pip install uv
```

Create a new project directory and navigate into it:
```bash
mkdir telegram-rag-bot
cd telegram-rag-bot
```

Initialize a new Python project.
```bash
uv init --bare
```
This command creates a minimal pyproject.toml file. This file will track our project's metadata and, most importantly, its dependencies.

Create a virtual environment using uv:
```bash
uv venv
```
This will create a .venv directory. Activate it with the following:
```bash
source .venv/bin/activate  

# On Windows, use 
#.venv\Scripts\activate
```

Install the necessary Python packages using uv:
```bash
uv add python-telegram-bot python-dotenv langchain langchain-openai langchain-community faiss-cpu jq sentence-transformers
```

The key libraries are:

- `python-telegram-bot`: For handling all Telegram communication.

- `langchain`: The primary framework for building the RAG pipeline.

- `langchain-openai`: Connector to OpenWebUI’s OpenAI-compatible API.

- `faiss-cpu`: An efficient library for similarity search, used as a local vector store to quickly find relevant chunks of your FAQ data.

#### Environment and configuration

The bot reads the Telegram token from the environment variable BOT_TOKEN. We can store it in a .env file as BOT_TOKEN=your-token-here.
```bash
# .env (OpenWebUI)
# OPENWEBUI_URL must end with /v1 (e.g., http://localhost:3000/v1).
BOT_TOKEN=123456:abcdefg
OPENWEBUI_URL=http://localhost:3000/v1
OPENWEBUI_API_KEY=your_key_here
```
[Inline mode](https://core.telegram.org/bots/features#inline-requests) requires enabling inline for the bot via BotFather.


Create a new file named `bot.py` and add the following code to set up and add message handlers for the Telegram bot.

```python
import logging
import os
from uuid import uuid4
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
from dotenv import load_dotenv

# load .env variables
load_dotenv()
bot_token = os.getenv("BOT_TOKEN", "")

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    
async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document:
        file = await update.message.document.get_file()
        file_name = update.message.document.file_name
        await file.download_to_drive(file_name)
    elif update.message.photo:
        # Get the largest photo size
        file = await update.message.photo[-1].get_file()
        file_name = f"photo_{file.file_unique_id}.jpg" # Create a unique name for photos
        await file.download_to_drive(file_name)
    elif update.message.video:
        file = await update.message.video.get_file()
        file_name = update.message.video.file_name
        await file.download_to_drive(file_name)
    else:
        await update.message.reply_text("Please send a document, photo, or video.")
        return
    
def main() -> None:
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    document_handler = MessageHandler(filters.PHOTO | filters.Document.PDF | filters.VIDEO, document)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(document_handler)
    application.add_handler(unknown_handler)

    # Run the bot
    logger.info("Starting bot polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
    
```

#### Try it out
To run the application, simply run
```bash
uv run bot.py
```
Search for your bot name in Telegram and send the bot a message or command like `/start` or `/caps`.

#### What this bot does
- Responds to /start with a greeting.
- Echoes back any plain text message (that isn’t a command).
- Converts text to uppercase via /caps or inline mode.
- Downloads files users send (photos, PDFs, and videos) to local storage.
- Politely handles unknown commands.

#### Core structure

- `start()`: Sends a simple welcome message when the user runs /start.
- `echo()`: Replies with the exact same text the user sent (only for non-commands).
- `caps()`: Turns the arguments after /caps into uppercase and sends them back.
- `inline_caps()`: Provides an inline result that uppercases whatever users type after @YourBotName in any chat.
- `document()`: Saves received media to disk:
    - Photos: Downloads the largest size, naming it photo_<unique_id>.jpg.
    - PDFs: Downloads using the document’s file name. Note: The filter only accepts PDFs as documents.
    - Videos: Downloads using the video’s file name.
    - If none of these are present, it prompts the user to send a supported file.
- `unknown()`: Catches any unrecognized commands and replies with a friendly error.

#### Handlers and filters

- `CommandHandler('start', start)` and `CommandHandler('caps', caps)` handle [commands](https://core.telegram.org/bots/features#commands).
- `MessageHandler(filters.TEXT & (~filters.COMMAND), echo)` ensures normal text (not commands) is echoed.
- `InlineQueryHandler(inline_caps)` answers [inline queries](https://core.telegram.org/bots/features#inline-requests).
- `MessageHandler(filters.PHOTO | filters.Document.PDF | filters.VIDEO, document)` restricts downloads to photos, PDFs, and videos.
- `MessageHandler(filters.COMMAND, unknown)` is added last to catch all other commands.

#### Running the bot

`main()` wires up the handlers, builds the Application with the token, logs a startup message, and starts long polling via `application.run_polling()`.

This script is a clean, async-first Telegram bot scaffold that demonstrates commands, inline mode, message filtering, and media downloads—ready to extend for more sophisticated behaviors.

Now that we have our bot ready, we will extend the code to add a RAG pipeline to the bot. 

### Setting up the knowledge base
Let’s set up a knowledge base by creating a file named `faqs.json` to hold our data. The RAG pipeline will load and search this content. An example structure is shown below.

```json
[
 {
    "category": "General",
    "question": "What are your operating hours?",
    "answer": "Monday to Friday, 9:00 AM–5:00 PM (local time)."
  },
  {
    "category": "Accounts",
    "question": "How do I reset my password?",
    "answer": "Go to our website, click Login, then Forgot Password. Check your email for the reset link."
  }
]
```

### Setting up the RAG Pipeline
The RAG pipeline is the engine that converts our static JSON file into a searchable brain for our bot. This part initializes once and creates a vector database. In simple steps,
- Load faqs.json
- Create embeddings
- Store them in FAISS
- When a user asks a question, find similar answers and ask the LLM to write a reply based only on those.

##### Data Ingestion (Indexing the FAQs) handled by `setup_rag_chain()` method
This part happens once when the bot starts. We load the `faqs.json` file, create vector embeddings, and store them in a searchable database (FAISS).

- Load Data: Read the faqs.json file.

- Embeddings: Use an embedding model [`HuggingFace (Sentence-Transformers) all‑MiniLM‑L6‑v2.`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) to convert the text into numerical vectors.

- Vector Store: Store these vectors in a FAISS index for fast retrieval.

##### The RAG Retrieval Logic handled by `handle_message()` method

When a user asks a question:

- Embed Query: The user's question is converted into an embedding vector.

- Retrieve Context: The query vector is used to perform a similarity search against the FAISS index. This returns the top K most relevant FAQs (question and answer pairs).

- Construct Prompt: A final prompt is built, containing the user's question and the retrieved relevant context.

- Example Prompt Template: "You are an expert FAQ assistant. Use the following context to answer the user's question. If the context does not contain the answer, state that you cannot help with this specific question. Context: [Retrieved FAQs] Question: [User's message]"

- Generate Response: The complete prompt is sent to our OpenWebUI model via the OpenAI-compatible API, e.g. gpt-5 or another model exposed by OpenWebUI, which generates a coherent, context-grounded final answer.

- Send to Telegram: The bot sends the LLM's final response back to the user.

##### New capabilities added to `bot.py`

- RAG pipeline: Loads FAQs from a local JSON file, embeds them with HuggingFace, retrieves the most relevant entries via FAISS, and drafts answers with an LLM served by OpenWebUI.
- Inline UX polish: Sends a “typing…” chat action while the model thinks.
- Persisted chain: The RAG chain is built once at startup and stored in bot_data for reuse across messages.

The core logic of our bot will revolve around an update to the standard message handler. When a user sends a question, the bot no longer looks for a simple command; instead, it passes the question to the RAG pipeline.

#### Try it out
To run the application, simply run
```bash
uv run bot.py
```
Search for your bot name in telegram and send the bot a message like `What are your operating hours?`.


Changes to the RAG pipeline setup are available [here](https://github.com/bimalghartimagar/telegram-rag-bot/commit/4afac21e085c2782f98fffc66bb2cca27e6c7f50)

Source code is available [here](https://github.com/bimalghartimagar/telegram-rag-bot)

### Conclusion

By integrating a RAG pipeline, we've leveled up our Telegram bot from a simple command processor to a knowledge-aware assistant. This approach ensures our bot's answers are accurate, grounded in our provided faqs.json data, and remain consistent, dramatically reducing the chance of "hallucinations" from the underlying LLM.

This architecture is powerful and scalable. To expand its capabilities, we only need to update the faqs.json file and re-run the indexing step—no need to retrain or modify the core LLM!