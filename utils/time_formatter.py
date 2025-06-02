
def get_progress_bar(current: int, total: int) -> str:
    """
    Return progress bar as string: 00:34 ━━━⬤───── 03:45
    """
    def format_time(seconds: int):
        minutes = seconds // 60
        sec = seconds % 60
        return f"{minutes:02d}:{sec:02d}"

    bar_length = 20
    filled = int(bar_length * current / total)
    empty = bar_length - filled
    bar = "━" * filled + "⬤" + "─" * (empty - 1)
    
    return f"{format_time(current)} {bar} {format_time(total)}"
