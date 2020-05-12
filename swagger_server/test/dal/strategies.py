from hypothesis import strategies as st


NEO4J_IDENTIFIER_ST = st.from_regex('[A-Za-z][A-Za-z0-9]*', fullmatch=True)

NEO4J_VALUE_ST = st.one_of(
    st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1),
    st.integers(max_value=2 ** 63 - 1, min_value=-2 ** 63),
    st.floats(allow_infinity=False, allow_nan=False),
    st.booleans()
)

NEO4J_LABELS_ST = st.lists(elements=NEO4J_IDENTIFIER_ST, unique=True, min_size=1)
NEO4J_PROPS_ST = st.dictionaries(
    keys=NEO4J_IDENTIFIER_ST,
    values=NEO4J_VALUE_ST
)

NEO4J_NODE_ST = st.tuples(
    NEO4J_LABELS_ST,
    NEO4J_PROPS_ST
)
