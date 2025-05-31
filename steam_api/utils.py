def get_unlocked_and_locked_achievements(achievements):
    unlocked = [a for a in achievements if a.get('achieved', 0) == 1]
    locked = [a for a in achievements if a.get('achieved', 0) == 0]
    return unlocked, locked
