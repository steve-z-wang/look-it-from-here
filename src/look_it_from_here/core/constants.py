# Semantic constants for web page processing

# Semantic attributes to preserve (minimal set focused on meaning)
SEMANTIC_ATTRIBUTES = {
    # ARIA accessibility standards (minimal set)
    'role', 'aria-label',

    # HTML5 semantic attributes
    'title', 'alt',

    # Form semantics (essential only)
    'type', 'value', 'placeholder',
}

# Interactive HTML elements that should NEVER be collapsed
# These elements have inherent semantic meaning even without attributes
INTERACTIVE_ELEMENTS = {
    # Form controls
    'input', 'button', 'textarea', 'select', 'option',

    # Navigation
    'a', 'nav',

    # Interactive content
    'details', 'summary',

    # Media with controls
    'audio', 'video',

    # Form structure
    'form', 'fieldset', 'legend', 'label',
}

# Non-semantic role values that indicate elements should be skipped
NON_SEMANTIC_ROLES = {'none', 'presentation'}