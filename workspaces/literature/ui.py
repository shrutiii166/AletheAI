import streamlit as st

from rag.document_loader import load_pdf_pages
from rag.chunker import split_documents
from rag.vector_store import (
    create_vector_store,
    add_chunks,
    search_chunks,
)

from workspaces.literature.novel_tools import (
    NOVEL_FEATURES,
    analyze_novel,
    recommend_literature,
)

from workspaces.literature.poetry_tools import (
    POETRY_FEATURES,
    analyze_poetry,
)


def render_literature_workspace():

    st.subheader("Your Literature Companion")

    mode = st.radio(
        "What would you like to explore?",
        [
            "Novels & Literary Works",
            "Poems & Lyrics",
            "Literary Recommendations",
        ],
        horizontal=True,
        key="literature_mode",
    )

    # -----------------------------------------
    # Literary recommendations - no upload
    # -----------------------------------------

    if mode == "Literary Recommendations":

        personality = st.text_area(
            "Tell me about yourself, your interests, or your current mood.",
            placeholder="Describe your personality, thoughts, interests...",
            key="literature_personality",
        )

        if st.button("Find my literary match"):

            if not personality.strip():
                st.warning("Tell me a little about yourself first.")

            else:
                with st.spinner("Exploring the literary world..."):
                    response = recommend_literature(personality)

                st.markdown(response)

        return

    # -----------------------------------------
    # Upload one literary work
    # -----------------------------------------

    uploaded_file = st.file_uploader(
        "Upload one book, poem, or literary work (PDF)",
        type=["pdf"],
        max_upload_size=10,
        key="literature_pdf",
    )

    if uploaded_file:

        document_key = (
            f"{uploaded_file.name}_{uploaded_file.size}"
        )

        if st.session_state.get("literature_document_key") != document_key:

            try:
                with st.spinner("Processing your literary work..."):

                    pages = load_pdf_pages(
                        uploaded_file.getvalue(),
                        uploaded_file.name,
                    )

                    chunks = split_documents(pages)

                    client, collection = create_vector_store()

                    stored_count = add_chunks(collection, chunks)

                    st.session_state.literature_vector_client = client
                    st.session_state.literature_vector_collection = collection
                    st.session_state.literature_document_key = document_key

                    st.session_state.literature_document = {
                        "name": uploaded_file.name,
                        "pages": pages,
                        "chunk_count": stored_count,
                    }

                st.success(
                    f"Ready! {len(pages)} pages and "
                    f"{stored_count} text chunks indexed."
                )

            except Exception as error:
                st.error(f"Could not process this file: {error}")
                return

    else:
    # Clear the previous document when the upload is removed.
     st.session_state.pop("literature_document", None)
     st.session_state.pop("literature_document_key", None)
     st.session_state.pop("literature_vector_client", None)
     st.session_state.pop("literature_vector_collection", None)
     st.session_state.pop("literature_response", None)        

    document = st.session_state.get("literature_document")

    if not document:
        st.info("Upload a literary work to begin exploring it.")
        return

    st.caption(f"Currently exploring: **{document['name']}**")

    # -----------------------------------------
    # Feature selection
    # -----------------------------------------

    features = (
        NOVEL_FEATURES
        if mode == "Novels & Literary Works"
        else POETRY_FEATURES
    )

    feature = st.selectbox(
        "Choose an experience",
        features,
        key="literature_feature",
    )

    question = st.text_area(
        "What would you like to explore?",
        placeholder="Ask a question or describe what you'd like analysed...",
        key="literature_analysis_question",
    )

    if st.button("Explore", key="literature_explore"):

      if not question.strip():
        st.warning("Enter a question or request first.")

      else:
        collection = st.session_state.literature_vector_collection

        with st.spinner("Exploring your literary work..."):

            results = search_chunks(
                collection,
                question,
                top_k=8,
            )

            if not results:
                st.session_state.pop("literature_response", None)
                st.warning(
                    "I couldn't find relevant passages. "
                    "Try rephrasing your request."
                )

            else:
                context = "\n\n".join(
                    f"Page {item['metadata'].get('page', 'Unknown')}:\n"
                    f"{item['content']}"
                    for item in results
                )

                if mode == "Novels & Literary Works":
                    response = analyze_novel(
                        feature,
                        question,
                        context,
                    )
                else:
                    response = analyze_poetry(
                        feature,
                        question,
                        context,
                    )

                st.session_state.literature_response = response


# Display the response outside the button block
    if st.session_state.get("literature_response"):
      st.markdown(st.session_state.literature_response)