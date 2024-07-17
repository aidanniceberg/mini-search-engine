WEBSITE_MAPPING = {
    "mappings": {
        "properties": {
            "url": {"type": "keyword"},
            "title": {"type": "text"},
            "description": {"type": "text"},
            "content": {"type": "text"},
            "alts": {"type": "text"},
            "h1": {"type": "text"},
            "h2": {"type": "text"},
            "h3": {"type": "text"},
            "h4": {"type": "text"},
            "h5": {"type": "text"},
            "h6": {"type": "text"},
            "paragraphs": {"type": "text"},
            "linked_data": {
                "type": "object",
                "dynamic": False
            },
        }
    }
}
