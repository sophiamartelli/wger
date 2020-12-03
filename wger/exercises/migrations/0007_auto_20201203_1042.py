# Generated by Django 3.1.3 on 2020-12-03 09:42

from django.db import migrations


exercise_variation_ids = [
    #
    # exercises in English
    #

    # Rows
    [106, 108, 109, 110, 142, 202, 214, 339, 340, 362, 412, 670],

    # Lat Pulldowns
    [187, 188, 204, 212, 213, 215, 216, 424],

    # Deadlifts
    [105, 161, 209, 328, 351, 381],

    # Shoulder Raises
    [148, 149, 233, 237, 306, 421],

    # "Shoulder Press"
    [119, 123, 152, 155, 190, 227, 228, 229, 329],

    # "Calf Raises"
    [102, 103, 104, 776],

    # "Bench Press"
    [100, 101, 163, 192, 210, 211, 270, 399],

    # "Pushups"
    [168, 182, 260, 302, 790],

    # "Chest Fly"
    [122, 145, 146, 206],

    # "Crunches"
    [91, 92, 93, 94, 176, 416, 95, 170],

    # "Kicks"
    [303, 631, 125, 126, 166],

    # "Squats"
    [111, 160, 185, 191, 300, 342, 346, 355, 387, 389, 407, 650, 795],

    # "Lunges"
    [112, 113, 346, 405],

    # "Leg Curls"
    [117, 118, 154, 792],

    # "Leg Press"
    [114, 115, 130, 788],

    # "Bicep Curls"
    [74, 80, 81, 86, 129, 138, 193, 205, 208, 275, 298, 305, 768],

    # "Tricep Extensions"
    [89, 90, 274, 344],

    # "Tricep Presses"
    [84, 85, 88, 186, 217, 218, 386],

    # "Dips"
    [82, 83, 162, 360],

    #
    # exercises in German
    #

    # Bizeps Curls
    [44, 26, 242, 24, 3, 815, 222],

    # Dips
    [29, 68],

    # French press
    [58, 25],

    # Hammercurls
    [46, 134],

    # Beinpresse
    [6, 54],

    # Beinstrecker
    [39, 69],

    # Kniebeuge
    [358, 390, 7, 402, 200, 762, 707],

    # Beinheben
    [35, 34],

    # Crunches
    [4, 33, 51, 32, 56],

    # Plank
    [417, 712],

    # Bankdrücken
    [77, 15, 720, 17],

    # Butterfly
    [30, 52],

    # Fliegende
    [18, 73, 722],

    # Kabelziehen
    [252, 252],

    # Frontziehen
    [10, 12],

    # Latzug
    [158, 226, 243, 244, ],

    # Rudern
    [245, 59, 70, 224, 76],

    # Frontdrücken
    [19, 153, 66, ],

    # Shrugs
    [8, 137, 67],

    # Waden
    [13, 23, 297],
]


def insert_variations(apps, schema_editor):
    """
    Forward migration. Add variation data to exercises
    """

    # We can't import the Exercise model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Exercise = apps.get_model('exercises', 'Exercise')
    Variation = apps.get_model('exercises', 'Variation')

    for group in exercise_variation_ids:
        variation = Variation()
        variation.save()

        for exercise_id in group:
            exercise = Exercise.objects.get(pk=exercise_id)
            exercise.variations = variation
            exercise.save()


def remove_variations(apps, schema_editor):
    """
    Backwards migration. Removes all variation data.
    """
    Exercise = apps.get_model('exercises', 'Exercise')
    Exercise.objects.all().update(variations=None)


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0006_auto_20201203_0203'),
    ]

    operations = [
        migrations.RunPython(insert_variations, remove_variations),
    ]
