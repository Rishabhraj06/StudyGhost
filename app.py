"""StudyGhost Streamlit Interactive Web Application."""

import streamlit as st
from studyghost.cheatsheet import CheatSheetEngine
from studyghost.mcq_gen import MCQGenerator
from studyghost.flashcards import FlashcardEngine

st.set_page_config(page_title="StudyGhost - 1-Page Cheatsheet & Exam Copilot", page_icon="👻", layout="wide")

st.markdown("""
# 👻 StudyGhost
### Stop reading 80-page slides the night before exams.
Condense bulky PDFs into **1-page high-yield cheat sheets**, instant **practice MCQs**, and **Anki-ready flashcard decks**.
""")

st.sidebar.header("📁 Input Study Materials")
upload_file = st.sidebar.file_uploader("Upload Notes (TXT, MD)", type=["txt", "md"])
subject = st.sidebar.text_input("Course / Subject Name", value="Distributed Systems")

default_sample = """Distributed Systems: A distributed system is a collection of autonomous computing elements that appears to its users as a single coherent system.
CAP Theorem: The CAP theorem states that a distributed data store can simultaneously provide at most two of three guarantees: Consistency, Availability, and Partition Tolerance.
Consensus is defined as the process of agreeing on a single data value among distributed processes.
Raft Consensus: Raft achieves consensus via an elected leader who manages replicated logs.
Paxos Protocol: Paxos is a family of consensus protocols operating under crash-fault tolerant networks.
Two-Phase Commit (2PC): 2PC is a distributed algorithm that coordinates all processes in a distributed atomic transaction.
Throughput is the rate at which successful transactions are committed.
Latency is defined as the time delay experienced in system communications.
Redundancy is the duplication of critical components to increase system reliability.
Network partitions occur when communication between nodes in different subnetworks fails.
Eventual consistency guarantees that if no new updates are made to a given data item, all accesses will eventually return the last updated value.
"""

raw_text = ""
if upload_file is not None:
    raw_text = upload_file.read().decode("utf-8", errors="ignore")
else:
    raw_text = st.text_area("Or paste lecture notes / textbook snippets here:", value=default_sample, height=180)

tab1, tab2, tab3 = st.tabs(["📄 1-Page Cheatsheet", "🎯 Exam MCQ Simulator", "🗂️ Anki Flashcards"])

if raw_text.strip():
    with tab1:
        st.subheader("⚡ 1-Page High-Yield Cram Sheet")
        sheet = CheatSheetEngine.generate(raw_text, subject_title=subject)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📖 Core Definitions")
            for d in sheet["definitions"]:
                st.info(d)
        with col2:
            st.markdown("#### 📐 Laws & Formulas")
            for r in sheet["rules_and_formulas"]:
                st.warning(r)
                
        st.markdown("#### 🎯 Must-Know Exam Highlights")
        for k in sheet["key_takeaways"]:
            st.markdown(f"- **{k}**")
            
        md_content = f"# {subject} - 1-Page Cheatsheet\n\n## Core Definitions\n" + "\n".join(f"- {d}" for d in sheet["definitions"]) + "\n\n## Key Highlights\n" + "\n".join(f"- {k}" for k in sheet["key_takeaways"])
        st.download_button("📥 Download Cheatsheet (.md)", data=md_content, file_name=f"{subject.lower()}_cheatsheet.md", mime="text/markdown")

    with tab2:
        st.subheader("🎯 Active Recall Practice Quiz")
        questions = MCQGenerator.generate_questions(raw_text, count=5)
        score = 0
        for i, q in enumerate(questions):
            st.markdown(f"**{q.prompt}**")
            user_choice = st.radio(f"Select option for #{i+1}:", q.options, key=f"q_{i}", index=None)
            if user_choice:
                user_opt_idx = q.options.index(user_choice)
                if user_opt_idx == q.correct_idx:
                    st.success("✅ Correct! " + q.explanation)
                    score += 1
                else:
                    st.error("❌ Incorrect. " + q.explanation)
            st.write("---")

    with tab3:
        st.subheader("🗂️ Spaced Repetition Flashcards")
        cards = FlashcardEngine.generate(raw_text, max_cards=8)
        tsv_data = FlashcardEngine.to_tsv(cards)
        
        st.write(f"Generated **{len(cards)}** high-yield flashcards:")
        for idx, card in enumerate(cards, 1):
            with st.expander(f"Card #{idx}: {card.front}"):
                st.markdown(f"**Answer:** {card.back}")
                st.caption(f"Tag: #{card.tag}")
                
        st.download_button(
            label="📥 Download for Anki (.tsv)",
            data=tsv_data,
            file_name=f"{subject.lower()}_anki_deck.tsv",
            mime="text/tab-separated-values"
        )
