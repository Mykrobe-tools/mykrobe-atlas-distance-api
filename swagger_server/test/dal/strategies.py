from hypothesis import strategies as st


NEO4J_IDENTIFIER_ST = st.from_regex('[A-Za-z][A-Za-z0-9]*', fullmatch=True)
NEO4J_VALUE_ST = st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1)