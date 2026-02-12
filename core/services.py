from .models import MeasurementProfile, PatternSizeRequirement, Pattern, Fabric
import re
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from math import gcd


def convert_inches_to_yardage(total_inches):
    """Converts internal inch measurements back to a yardage string for the UI."""
    if not total_inches:
        return ""

    yards = float(total_inches) / 36
    whole_yards = int(yards)
    remainder = yards - whole_yards

    # Convert remainder to the nearest 8th of a yard (standard for sewing)
    eighths = int(round(remainder * 8))

    if eighths == 0:
        return str(whole_yards)
    if eighths == 8:
        return str(whole_yards + 1)

    # Simplify the fraction (e.g., 4/8 becomes 1/2)
    common = gcd(eighths, 8)
    num = eighths // common
    den = 8 // common

    frac_str = f"{num}/{den}"
    return f"{whole_yards} {frac_str}".strip() if whole_yards > 0 else frac_str


def validate_and_convert_yardage(value):
    if not value:
        return None

    value_str = str(value).strip()

    # NEW: Check if it's already a decimal (e.g., '2.375' or '85.50' from the DB)
    # We allow this now so the form doesn't break on re-save
    try:
        # If the user entered a decimal, treat it as Yards
        if "." in value_str:
            decimal_yards = Decimal(value_str)
            return (decimal_yards * 36).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
    except:
        pass

    # Existing fraction logic
    pattern = r"^(\d+)?\s?(\d+/\d+)?$"
    match = re.match(pattern, value_str)

    if not match or value_str == "":
        raise ValidationError("Invalid format. Use '2', '2.5', or '2 3/8'.")

    whole_str, frac_str = match.groups()
    whole = Decimal(whole_str) if whole_str else Decimal(0)
    fraction = Decimal(0)

    if frac_str:
        num, den = map(int, frac_str.split("/"))
        if num >= den:
            raise ValidationError(f"Invalid fraction '{frac_str}'.")
        fraction = Decimal(num) / Decimal(den)

    total_inches = (whole + fraction) * 36
    return total_inches.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


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
