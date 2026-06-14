"""Link-formatting helpers.

Each transform is its own small function so they can be tested and
troubleshot in isolation. The display text gets cleaned up; the link
*target* is always left untouched so it stays a working URL.
"""

import re


def strip_scheme(url: str) -> str:
    """Drop a leading http:// or https:// from the front of a URL.

    >>> strip_scheme("https://pushpopswap.com/nat64.html")
    'pushpopswap.com/nat64.html'
    """
    return re.sub(r"^https?://", "", url)


def strip_html_ext(text: str) -> str:
    """Drop a .html / .htm extension off the path.

    Matches the extension at the very end *or* right before a ?query or
    #fragment, so the trailing #anchor / query string is preserved.

    >>> strip_html_ext("pushpopswap.com/nat64.html")
    'pushpopswap.com/nat64'
    >>> strip_html_ext("pushpopswap.com/nat64.html#config")
    'pushpopswap.com/nat64#config'
    >>> strip_html_ext("pushpopswap.com/nat64.html?ref=x")
    'pushpopswap.com/nat64?ref=x'
    """
    return re.sub(r"\.html?(?=[?#]|$)", "", text, flags=re.IGNORECASE)


def display_text(url: str) -> str:
    """Build the human-friendly link text: no scheme, no .html extension.

    >>> display_text("https://pushpopswap.com/nat64.html")
    'pushpopswap.com/nat64'
    """
    return strip_html_ext(strip_scheme(url))


def clean_link(url: str) -> str:
    """Markdown link with cleaned display text and a preview-suppressed target.

    The target keeps the full, working URL (scheme + .html) and is wrapped in
    <...> so Discord won't unfurl a preview.

    >>> clean_link("https://pushpopswap.com/nat64.html")
    '[pushpopswap.com/nat64](<https://pushpopswap.com/nat64.html>)'
    """
    return f"[{display_text(url)}](<{url}>)"
