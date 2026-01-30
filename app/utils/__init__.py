"""Module Utils - Utilitaires et helpers"""

from .session import (
    init_session_state,
    init_modules,
    reset_session_state,
    add_to_favorites,
    get_session_stats
)

from .cache_utils import (
    get_quote_hash,
    fetch_unique_quote,
    generate_image_cached,
    clear_image_cache,
    clear_quote_cache,
    get_cache_stats,
    translate_cached,
    analyze_sentiment_cached
)

from .quote_processor import (
    process_quote_generation,
    regenerate_with_new_style,
    validate_quote_data,
    format_quote_for_display
)

__all__ = [
    # Session
    'init_session_state',
    'init_modules',
    'reset_session_state',
    'add_to_favorites',
    'get_session_stats',
    
    # Cache
    'get_quote_hash',
    'fetch_unique_quote',
    'generate_image_cached',
    'clear_image_cache',
    'clear_quote_cache',
    'get_cache_stats',
    'translate_cached',
    'analyze_sentiment_cached',
    
    # Quote Processor
    'process_quote_generation',
    'regenerate_with_new_style',
    'validate_quote_data',
    'format_quote_for_display'
]