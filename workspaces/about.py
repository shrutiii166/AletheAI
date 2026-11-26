import streamlit as st


def render_about_page():

    st.markdown(
        """
        <style>
        .about-page {
            max-width: 850px;
            margin: auto;
        }

        .about-intro {
            font-size: 1.08rem;
            line-height: 1.85;
        }

        .about-note {
            padding: 18px 22px;
            border-left: 3px solid #9b8ac4;
            background: rgba(155, 138, 196, 0.08);
            border-radius: 5px;
            margin: 18px 0;
            line-height: 1.7;
        }

        .about-small {
            opacity: 0.75;
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="about-page">', unsafe_allow_html=True)

    # -----------------------------------------
    # 1. Introduction
    # -----------------------------------------

    st.title("✦ Hello there!")

    st.markdown(
        """
        <div class="about-intro">

        I'm AletheAI. You can call me Alethea, if we're going to be friends.

        I started as an idea. A big, slightly ambitious one: a companion
        you could talk to about the things you read, study and work with.

        A place to ramble about a poem that stuck with you at 2 a.m.
        To argue about what a character really meant. To dig one stubborn
        answer out of a 200-page document, or to ask a spreadsheet what
        it's been hiding all this time.

        I didn't appear fully formed, though. I got built through a lot
        of experiments. Some worked. Some didn't. A few were extremely
        confident and extremely wrong (we don't talk about those).

        But every one taught me something, and look at me now. Still
        learning, still curious, and slightly too excited to meet you.

        My name comes from the Greek word <i>alētheia</i>, which means
        truth, or literally "un-hidden" (and more, but we dont have the full day now, do we?). Finding what's already in your
        books, notes and data is my whole job. And when I can't find it,
        I'll tell you instead of making something up.

        But I promise to do my best. Fair deal?

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # -----------------------------------------
    # 2. Origin story
    # -----------------------------------------

    st.header("✧ So... why do I exist?")

    st.markdown(
        """
        The creator wanted everything. And I mean everything.

        She's a reader, a curious mind, someone who loves exploring
        ideas but prefers smart work over unnecessarily hard work.

        But like everyone, she has her struggles, too.

        Visualising data wasn't always easy. Making sense of lengthy
        documents could be tedious. Studying sometimes meant spending
        more time organising information than actually understanding it.

        And when she read a book, she didn't always want a summary.
        Sometimes she wanted to question a character, argue about an
        interpretation, or understand why a particular sentence stayed
        with her.

        So with all these things to discuss, argue and talk about, she just did what AI engineers do best.
        "CREATE" 
        And somewhere while all that learning, experimenting, breaking things, fixing them and exhaustingly trying again, I happened.

        I'm not quite everything(obviously). Not yet, anyway.
        But every little corner of mine has a reason for being here.

        """
    )

    st.divider()

    # -----------------------------------------
    # 3. Workspaces
    # -----------------------------------------

    st.header("✧ Come explore")

    st.markdown(
        "I've made a few little corners for the different things "
        "your curious mind might get up to."
    )

    with st.container(border=True):
        st.subheader("📚 Bookish Corner")

        st.markdown(
            "**Ever finished a book and wanted to keep talking about it?**"
        )

        st.write(
            "Excellent. We're going to get along. Bring me your novels, "
            "poems or lyrics. We can wander through characters, symbolism, "
            "themes and passages, or disagree about what a writer might "
            "have meant. I can even imagine a conversation with the author. "
            "And don't worry, I won't spoil the ending unless you ask."
        )

        st.caption(
            "How to begin: Upload a literary PDF, choose an experience, "
            "and tell me what's on your mind."
        )

    with st.container(border=True):
        st.subheader("🎓 Study Nook")

        st.markdown(
            "**Ever wished your study material would explain itself "
            "a little better?**"
        )

        st.write(
            "I've got a few tricks for that. Give me your study material "
            "and I can turn it into revision notes, flashcards and quizzes, "
            "break difficult topics into simpler explanations, and help "
            "you check what you've understood."
        )

        st.caption(
            "How to begin: Upload your study PDF and choose what you'd "
            "like help with."
        )

    with st.container(border=True):
        st.subheader("🔎 Document Detective")

        st.markdown(
            "**Ever looked at a long document and wondered where "
            "to even begin?**"
        )

        st.write(
            "Hand it over. I'll help you find relevant information, "
            "answer questions and make sense of what's inside. And when "
            "I find an answer, I'll point to the page where I found it."
        )

        st.caption(
            "How to begin: Upload a PDF and ask me a question in the chat."
        )

    with st.container(border=True):
        st.subheader("📊 Numbers Playground")

        st.markdown(
            "**Ever stared at a spreadsheet and wondered what "
            "it's trying to tell you?**"
        )

        st.write(
            "Don't worry. I don't judge spreadsheets. Even the messy ones. "
            "Bring me your CSV or Excel data and we can explore patterns, "
            "look at statistics, create charts and ask questions about "
            "what the numbers are hiding."
        )

        st.caption(
            "How to begin: Upload your dataset, explore the tabs, "
            "and ask me questions in the chat."
        )

    st.divider()

    # -----------------------------------------
    # 4. Technical explanation
    # -----------------------------------------

    st.header("✧ A peek under my hood")

    st.markdown(
        """
        - **Language model:** My brain, which reads and writes.
        - **Embeddings:** How I turn sentences into numbers, so I can
          find passages with similar meaning.
        - **RAG:** I look things up in your document first, then answer.
        - **Python and pandas:** How I count, compare and draw your data.
        """
    )

    st.divider()

    # -----------------------------------------
    # 5. Privacy and accuracy
    # -----------------------------------------

    st.header("✧ A little promise")

    st.markdown(
        """
        I can make mistakes, so please double-check anything important.

        Your files and processed document data are handled temporarily,
        not stored in a permanent document database. AletheAI is designed
        to clear session data after one hour.

        Still, please don't upload sensitive or confidential information.
        Better safe than sorry, yes?
        """
    )

    st.divider()

    # -----------------------------------------
    # 6. Closing
    # -----------------------------------------

    st.header("✧ Before you go...")

    st.markdown(
        """
        I'm still growing. If you find something I could do better,
        tell my creator.

        She gets very excited about improvements.
        """
    )

    st.markdown(
        '<p class="about-small">Made with curiosity, experiments, '
        'and quite a bit of persistence. ✦</p>',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
