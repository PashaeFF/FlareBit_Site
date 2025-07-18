def get_page_range(paginator, page, show_pages):
    current_page = page.number
    total_pages = paginator.num_pages
    
    start_page = max(current_page - show_pages // 2, 1)
    end_page = min(start_page + show_pages - 1, total_pages)
    
    if end_page - start_page + 1 < show_pages:
        start_page = max(end_page - show_pages + 1, 1)
    
    return range(start_page, end_page + 1)


ALLOWED_MIME_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'video/mp4',
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
]

ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.webp', '.png', '.gif', '.mp4', '.pdf', '.docx', '.doc', '.xlsx']
