import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
import re

# Download necessary NLTK resources (if not already downloaded)
nltk.download("punkt")

def extract_obligations_and_rights(text):
    sentences = sent_tokenize(text)

    obligations = []
    rights = []

    # Define regex patterns to match exact phrases and variations
    obligation_patterns = [
        r"\bmust\b",
        r"\bshall\b",
        r"\bis required to\b",
        r"\bhas to\b",
        r"\bneeds to\b",
        r"\bagree(?:s|d) to\b",
        r"\bobligated to\b",
        r"\bobligation to\b",
        r"\bpromise(?:s|d)? to\b",
        r"\bpay(?:s|ed)?\b",
        r"\bresponsible for\b",
        r"\bcommit(?:s|ted)? to\b",
        r"\bsupposed to\b",
        r"\bfail(?:s|ed)? to\b",
        r"\brepay\b",
        r"\bborrower is liable\b",
        r"\bgotta\b",  # Informal: "got to"
        r"\bneed(?:s|ed)? to\b",  # Variations of "need"
        r"\bshould\b",  # Informal obligation
        r"\bought to\b",  # Informal: "ought to"
        r"\bwill give\b",  # Added to capture "will give"
        r"\bdid not give\b",  # Added to capture "did not give"
        r"\btold\b",  # Added to capture "told"
        r"\bmake the payment\b",  # Added to capture "make the payment"
        r"\bmake payment\b",  # Added to capture "make payment"
        r"\bpay\b",  # Added to capture "pay"
        r"\brefused to repair\b",  # Added to capture "refused to repair"
        r"\brepair\b",  # Added to capture "repair"
        r"\breplace\b"  # Added to capture "replace"
    ]

    rights_patterns = [
        r"\bis entitled to\b",
        r"\bhas the right to\b",
        r"\bhave the right to\b",
        r"\bmay\b",
        r"\bcan\b",
        r"\bis allowed to\b",
        r"\bpermitted to\b",  # Variation of "allowed"
        r"\bable to\b",  # Informal: "able to"
        r"\ballowed to\b",  # Informal: "allowed to"
        r"\breceive\b",  # Added to capture implicit rights
        r"\bwarranty\b"  # Added to capture warranty-related rights
    ]

    # Compile the patterns with case-insensitive flag
    obligation_regex = re.compile("|".join(obligation_patterns), re.IGNORECASE)
    rights_regex = re.compile("|".join(rights_patterns), re.IGNORECASE)

    # Process each sentence
    for sentence in sentences:
        is_obligation = obligation_regex.search(sentence)
        is_right = rights_regex.search(sentence)

        # If both obligation and right are found in the same sentence, extract separately
        if is_obligation and is_right:
            obligation_match = obligation_regex.search(sentence)
            right_match = rights_regex.search(sentence)

            # Extract part of sentence related to obligation
            obligation_part = sentence[obligation_match.start():].split(".")[0]
            obligations.append(obligation_part.strip())

            # Extract part of sentence related to rights
            right_part = sentence[right_match.start():].split(".")[0]
            rights.append(right_part.strip())

        # If only an obligation exists, add it
        elif is_obligation:
            obligations.append(sentence.strip())

        # If only a right exists, add it
        elif is_right:
            rights.append(sentence.strip())
            # Check for implicit obligation
            if "warranty" in sentence.lower():
                obligations.append("Implicit obligation to repair or replace the phone under warranty terms.")

    return obligations, rights

# Streamlit UI
st.title("📜 Legal Contract Parser")
st.write("Extract obligations and rights from legal documents.")

# Input area for legal text
user_input = st.text_area("Enter legal text:", height=150)

if st.button("🔍 Extract Obligations & Rights"):
    if user_input:
        obligations, rights = extract_obligations_and_rights(user_input)

        st.subheader("🔍 Extracted Results")

        # Display obligations
        st.markdown("### ✅ Obligations")
        if obligations:
            for ob in obligations:
                st.write(f"- {ob}")
        else:
            st.warning("No obligations found.")

        # Display rights
        st.markdown("### 🔴 Rights")
        if rights:
            for rt in rights:
                st.write(f"- {rt}")
        else:
            st.warning("No rights found.")
    else:
        st.error("Please enter legal text to analyze.")
