# Planning/Brainstorming

I want to make the following application:

Purpose: I am learning to sew and want to start making clothing for my friends to use. However I need their body measurements in order to make sure the clothes fit them. I also source almost all of my fabric and materials secomd hand (i.e. Thrift Stores, Facebook Marketplace, Estate Sales), so the fabrics come in random lengths. I also have a varity of clothing patterns that required different quantity of materials based on the size of the garment that you want to make. So I would like to create an application that allows my friends to sign up, and enter in their measurements for the garments that I am going to make. I also want to be able to enter the sizing requirements for a pattern and the amount/dimensions of fabric that I have and the application cross reference the requirements of the sewing patter, the amount of fabric I have, and the measurements of my friends to provide a list of who I can make a garment for and what size.

I would like to make a product requirement document based on the information above, please ask any follow up questions that would help make the document more detailed as we prepare to make a Minimum viable product.

1. The Measurement Profile
-Standard vs. Custom: Do you want friends to fill out a "Universal Profile" (e.g., Bust, Waist, Hips, Inseam) once, or do you want to send them specific measurement requests based on the pattern you're currently looking at?
A: I want my friends to start by filing out a form with the universal profile that has all of the standard measurements. If custom measusurements are required, after they are narrowed down I can contant them myself over the phone when needed.
-Visual Aids: Since many people don't know exactly where their "natural waist" is, would you like the app to include diagrams or instructions for them?
A: And yes, I think including a basic image (that I am sure I can find on the internet) next to the form that describes where the measurements are would be necessary.
2. The Fabric Inventory
-Fabric Characteristics: Beyond dimensions (Length x Width), do we need to track stretch percentage or fabric type (Woven vs. Knit)? This is huge for sizing—a Size M in a jersey knit might fit a friend that a Size M in a stiff denim won't.
A: I don't think we would need to track the fabric type yet. This should be based on the basic dimensions.
-Irregular Shapes: Since you buy second-hand, do you often deal with "remnants" (non-rectangular pieces)? Should the app account for that, or should we stick to standard rectangular dimensions for the MVP?
A:Yes I often am working with remnants, but I would say that I should have the option to enter in the square footage/yardage of the materials and maybe we can perform some simple translation that would convert it to the stardard sewing yardage dimensions. But also patterns often offer some sort of chart based on the dimensions of the fabric since yardage of fabric can be in several shapes and sizes. So I think it should allow for me to enter in the pattern sizing/fabric chart to aid in the decision.
3. The Pattern Requirements
-Inputting the Chart: Sewing patterns usually have a "Body Measurement" chart and a "Finished Garment" chart. Which one do you want the app to use for the matching logic?
A:I think the body measurement chart should be the default, with the option to use the finished garment if the default is not available.
-Layout Logic: Patterns usually specify yardage based on fabric width (e.g., "2 yards of 45-inch wide" vs "1.5 yards of 60-inch wide"). Do you want the app to handle those specific calculations?
A: Yes, especially considering that the remnant fabirc might end up varying based on how I cut it.
4. The "Matchmaker" Logic
T-he "Ease" Factor: In sewing, "ease" is the extra room in a garment. Do you want the app to simply say "The pattern says Size 10, Friend is Size 10," or do you want it to be more precise (e.g., "This fabric is enough for the Size 10, and Friend A's measurements fit within the Size 10 range")?
A: I like the latter option. It should show me all friends that the fabric + pattern can accompany and what size. So if there is a pattern and combo that can make a 10, everyone that can fit a 0-10 should be shown with the size that would be within their measurement range.
-Prioritization: If you have enough fabric to make a shirt for three different friends, do you want a way to "claim" fabric for a specific person so it's removed from your available inventory?
A: Yes, I think once a fabric has been used to make something there should be a way to mark that the fabric is no longer available.
5. Access & Privacy
-Visibility: Should friends only see their own measurements, or is this a "closed circle" where everyone is comfortable? (Usually, people are a bit sensitive about measurement data!)
A: Yes, the only access a user (my friends) should be able to see is their own measurements. I do not even want them to be able to see the garment or fabric since that is going to be a surprise from them as well.
6. For the MVP, do you want to enter each "View" as a separate pattern, or do you need the app to handle multiple versions/views within one pattern entry?
A: Each view should be a separate pattern. That would be much easier for me and for caclulations
7. When you enter a remnant, would it be safer to enter the "Largest Usable Rectangle" (Length x Width) of that piece, or do you want the app to actually try to calculate based on total square inches? (Note: The "Largest Rectangle" method is usually much more reliable for sewing.)
A: I think largest usable rectangle would be best and simplest.
8. Does the app need to check if you have both fabrics in stock to suggest a match, or should it just focus on the main fabric for now?
A: Currently I am only working with pieces that are sourced from a single fabric. So we only need to worry about one at a time for now
9. Are you planning to work exclusively in Imperial (inches/yards), Metric (cm/meters), or do you need the app to convert between them (e.g., you measure a thrifted piece in cm but the pattern is in yards)?
A: Ideally it would all be imperial, and since it's thirfted fabrics where I will be doing the measurements myself (using measuring tapes that are in inches), lets only worry about imperial for now
10. Should the app show you how old a friend's measurement data is? Would you like a feature that allows you to send a "Measurement Refresh" nudge to a friend?
A: Lets show a "Last Updated" date in the view, but we do not need to nudge, I can do that myself.
11. Since you want the fabrics and garments to be a surprise, I assume there is an "Admin" view (you) and a "User" view (friends). Do you want a "Project" status to track your progress (e.g., Planned, In Progress, Completed)?
A: Yes, there should be an admin (me) view, as well as a user (friends) view. Sure we can inlcude a project view that has the pattern, fabric, and status/progress indicator.
12. To make the matching logic work, you’ll need to input this grid for every pattern. Are you comfortable entering multiple "Fabric Width vs. Yardage" rows for each size, or should we just have a single "Required Yardage" field for the most common width (e.g., 45")?
A: I think because the patterns I have all have variable sizes, that I would need to manually enter in the width vs yardage for each.
13. How do you want the "Matchmaker" to handle this? Should it only suggest a size if all of the friend's measurements fit within that size's range, or should it flag the friend if even one measurement fits (knowing you might "grade" between sizes manually)?
A: I think the measurements that matter most are the shoulders and chest/bust for tops and the waist/hips for bottoms. So if those measurements are within range then that should count as a match. And there are cases where the inseam matters (like a full lenght pant), but for something like a skirt the inseam doesn't. So maybe a flag for whether something is full length or not could be useful.
14. Would you like the app to automatically convert your "Length (inches) x Width (inches)" into "Total Yards" to compare against the pattern, or should the app strictly look at whether the rectangle you have is wider/longer than what the pattern specifies?
A: I think that it should do the width vs length as that seems to be important for things like dresses which have singular long pattern pieces where the length or width matters greatly.  
15. When you mark a project as "Completed," should that fabric be deleted from the database entirely, or moved to an "Archive/Scrap Pile" so you can see a history of what you've made?
A: Move to a scrap pile, not deleted
16. Since this involves personal measurements, do you want friends to create a password-protected account, or is a simple "Unique Link" (like a private Google Doc) enough for your needs?
A: I plan to use something like google/discord oauth for account creation/login.
17. Would you like to categorize patterns as "Top", "Bottom", or "Full Body" (e.g., a dress or jumpsuit that needs all measurements to match)?
A: Yes
18. Do you want the logic to be Strict (if they are $0.1''$ over, they are excluded) or Flexible (show them as a match but highlight the measurement that is slightly over in red/yellow)?
A: To start I would like to be strict since I am still learning and would like to follow the instructions as close as possible.
19. When you find a match and start a project, should the app notify the friend at all (e.g., "A new project has been started for you!"), or should the app stay completely silent so you can reveal the gift in person?
A: No
20. For the MVP, would you like a feature to upload a photo of the back of the pattern envelope? Even if the app doesn't "read" the text yet, having the photo there for your own reference while you enter the data could be a huge time-saver.
A: Yes, Uploading a picture of the back of the pattern envelope would be useful. Also for the fabric, uploading a photo of the fabric would be a nice touch.

## The Technical Stack

Framework: Django using Python
Frontend: HTML Templates that are built into Django with Tailwindcss and DaisyUI with django-tailwind | <https://pypi.org/project/django-tailwind/>
Backend: Django (built-in)
Database: SQLite for Development, PostgreSQL for Production
Auth: Python Social Auth - Django | <https://pypi.org/project/social-auth-app-django/>
