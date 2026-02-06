from .models import MeasurementProfile, PatternSizeRequirement, Pattern, Fabric


def get_sewable_matches(pattern: Pattern, fabric: Fabric):
    """
    Returns the SMALLEST possible size for each friend that fits
    within the available fabric dimensions.
    """
    matches = []
    # Keep track of IDs of friends who have already found their 'Best Fit'
    matched_friend_ids = set()

    # 1. Get sizes that fit the fabric, ordered from smallest to largest.
    # We order by max_bust (for tops/full) or max_waist (for bottoms).
    sort_field = "max_waist" if pattern.category == "BOTTOM" else "max_bust"

    possible_sizes = PatternSizeRequirement.objects.filter(
        pattern=pattern,
        required_width__lte=fabric.width_inches,
        required_length__lte=fabric.length_inches,
    ).order_by(sort_field)

    # 2. Iterate through sizes (starting with the smallest)
    for size_req in possible_sizes:
        # Get friends who haven't been matched yet
        friends = MeasurementProfile.objects.exclude(user_id__in=matched_friend_ids)

        # 3. Apply the strict measurement filters
        if pattern.category == "TOP":
            if size_req.max_bust:
                friends = friends.filter(bust_chest__lte=size_req.max_bust)
            if size_req.max_shoulder:
                friends = friends.filter(shoulder_width__lte=size_req.max_shoulder)

        elif pattern.category == "BOTTOM":
            if size_req.max_waist:
                friends = friends.filter(waist__lte=size_req.max_waist)
            if size_req.max_hips:
                friends = friends.filter(hips__lte=size_req.max_hips)
            if pattern.is_full_length and size_req.max_inseam:
                friends = friends.filter(inseam__lte=size_req.max_inseam)

        elif pattern.category == "FULL":
            if size_req.max_bust:
                friends = friends.filter(bust_chest__lte=size_req.max_bust)
            if size_req.max_waist:
                friends = friends.filter(waist__lte=size_req.max_waist)
            if size_req.max_hips:
                friends = friends.filter(hips__lte=size_req.max_hips)
            if size_req.max_shoulder:
                friends = friends.filter(shoulder_width__lte=size_req.max_shoulder)

        # 4. Add the newly matched friends to the results and 'lock' them
        for profile in friends:
            matches.append(
                {
                    "friend": profile.user,
                    "size_label": size_req.size_label,
                    "last_updated": profile.last_updated,
                }
            )
            matched_friend_ids.add(profile.user_id)

    return matches
