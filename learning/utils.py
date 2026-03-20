from .models import Badge, UserAchievement

def award_badge(user, badge_name):
    """Award a badge to a user safely — no crashes on duplicate calls."""
    
    # Find the badge by name
    badge = Badge.objects.filter(name=badge_name).first()
    
    if not badge:
        # Badge doesn't exist in DB — skip silently
        return False
    
    # Add to profile's ManyToMany (safe, ignores duplicates automatically)
    profile = user.learning_profile
    profile.badges.add(badge)
    
    # Save to UserAchievement history using get_or_create to prevent crash
    obj, created = UserAchievement.objects.get_or_create(
        user=user,
        badge=badge,
        achievement=None   # explicit None required for unique_together to work
    )
    
    return created  # True if newly awarded, False if already had it