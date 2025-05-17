# 🔍 Search Engine Project

## Authors: Serena Nguyen
This project was developed as a team effort for UCI's CS121: Information Retrieval course.

- **Serena Nguyen** – Backend development, document indexing, and retrieval logic  
- **Enrique Bar-Or** – Backend development, document indexing, and retrieval logic  
- **Francoise Morada** – Frontend UI development and result visualization

Team Number: 2024  
UCI NET IDs: `serenaan`, `ebaror`, `fmorada`

## 📖 Overview

Developed a lightweight document search engine that indexes a corpus of ~37,000 files, processes queries, and returns ranked results via a simple web interface. Built core indexing and retrieval logic from scratch, using Python and Flask.

---

## 💡 Key Features

- Inverted index construction across large corpus
- Tokenization and normalization of input queries
- Simple scoring/ranking of relevant documents
- Web-based UI for entering search queries
- Fast document lookup using optimized data structures

---

## 🛠️ Tech Stack

- Python 3
- Flask (UI + API)
- Jinja2 (HTML templates)
- Custom-built token parsing + index logic

---

## 🧪 How to Run

```bash
pip install -r requirements.txt
python searchengineui.py

then go to local host.
