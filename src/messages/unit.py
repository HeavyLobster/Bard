from src.util import embeds

def format_string(string):

    # Return strings without decimal points or with exponents without editing
    if not "." in string or "e" in string:
        return string

    # Split string into an integer portion and a decimal portion
    splitString = string.split(".")

    # If the first two digits after the decimal point are zeroes, just return
    # the integer portion
    if splitString[1][:2] == "00" or splitString[1][:2] == "0":
        return splitString[0]

    # If there are already only two or fewer decimal places of precision, return the string
    if len(splitString[1]) < 3:
        return string

    # Put the string back together while excluding everything after
    # the first two digits after the decimal point
    string = splitString[0] + "." + splitString[1][:2]

    return string


# Converts between imperial and metric unit and displays the result
async def convert(msg):

    # An array with each element being a space-separated word
    command = msg.content.split()

    # Make sure command is formatted properly
    if len(command) != 3:
        return await embeds.desc_only(msg.channel, f"!unit [value] [unit]")

    # Interpret command
    try:
        amount = float(command[1])
    except ValueError:
        formattedString = command[1] + f" is not a number I understand."
        return await embeds.desc_only(msg.channel, formattedString)

    unit = command[2].lower()

    # Save amount as a properly formatted string
    formattedAmount = format_string(command[1])

    # Metric length
    if unit in ["cm", "centimetre", "centimeter", "centimetres", "centimeters"]:

        # Calculate changes
        inches = amount * 0.3937
        feet = amount * 0.0328

        # Format strings
        inches = format_string(str(inches))
        feet = format_string(str(feet))

        formattedString = formattedAmount + f" centimeters is:\n" + inches + f" inches\n" + feet + f" feet"

    elif unit in ["m", "metre", "meter", "metres", "meters"]:

        # Calculate changes
        inches = amount * 39.3701
        feet = amount * 3.2808

        # Format strings
        inches = format_string(str(inches))
        feet = format_string(str(feet))

        formattedString = formattedAmount + f" meters is:\n" + inches + f" inches\n" + feet + f" feet"

    elif unit in ["km", "kilometre", "kilometer", "kilometres", "kilometers"]:

        # Calculate changes
        miles = amount * 0.6213
        feet = amount * 3280.84

        # Format strings
        miles = format_string(str(miles))
        feet = format_string(str(feet))

        formattedString = formattedAmount + f" kilometers is " + miles + f" miles\n" + feet + f" feet"

    # Metric weight
    elif unit in ["g", "gram", "grams"]:

        # Calculate changes
        ounces = amount * 0.0352
        pounds = amount * 0.0022

        # Format strings
        ounces = format_string(str(ounces))
        pounds = format_string(str(pounds))

        formattedString = formattedAmount + f" grams is:\n" + ounces + f" ounces\n" + pounds + f" pounds"

    elif unit in ["kg", "kilogram", "kilograms"]:

        # Calculate changes
        pounds = amount * 2.2046

        # Format strings
        pounds = format_string(str(pounds))

        formattedString = formattedAmount + f" kilograms is " + pounds + f" pounds"

    # Metric volume
    elif unit in ["ml", "millilitre", "milliliter", "millilitres", "milliliters"]:

        # Calculate changes
        teaspoons = amount * 0.2028
        tablespoons = amount * 0.0676
        fluidOunces = amount * 0.0338

        # Format strings
        teaspoons = format_string(str(teaspoons))
        tablespoons = format_string(str(tablespoons))
        fluidOunces = format_string(str(fluidOunces))

        formattedString = formattedAmount + f" milliliters is:\n" + teaspoons + f" teaspoons\n" + tablespoons + f" tablespoons\n" + fluidOunces + f" fluid ounces"

    elif unit in ["l", "litre", "liter", "litres", "liters"]:

        # Calculate changes
        fluidOunces = amount * 33.814
        cups = amount * 4.1666
        pints = amount * 2.1133
        quarts = amount * 1.0566
        gallons = amount * 0.2641

        # Format strings
        fluidOunces = format_string(str(fluidOunces))
        cups = format_string(str(cups))
        pints = format_string(str(pints))
        quarts = format_string(str(quarts))
        gallons = format_string(str(gallons))

        formattedString = formattedAmount + f"liters is:\n" + cups + f" cups\n" + pints + f" pints\n" + quarts + f" quarts\n" + gallons + f" gallons"

    # Metric temperature
    elif unit in ["c", "celsius"]:

        # Calculate changes
        fahrenheit = (amount * 1.8) + 32

        # Format strings
        fahrenheit = format_string(str(fahrenheit))

        formattedString = formattedAmount + f"°C is " + fahrenheit + f"°F"

    # US length
    elif unit in ["i", "in", "inch", "inches"]:

        # Calculate changes
        centimeters = amount * 2.54

        # Format strings
        centimeters = format_string(str(centimeters))

        formattedString = formattedAmount + f" inches is " + centimeters + f" centimeters"

    elif unit in ["f", "ft", "foot", "feet"]:

        # Calculate changes
        meters = amount * 0.3048

        # Format strings
        meters = format_string(str(meters))

        formattedString = formattedAmount + f" feet is " + meters + f" meters"

    elif unit in ["mi", "mile", "miles"]:

        # Calculate changes
        kilometers = amount * 1.6093

        # Format strings
        kilometers = format_string(str(kilometers))

        formattedString = formattedAmount + f" miles is " + kilometers + f" kilometers"

    # US weight
    elif unit in ["oz", "ounce", "ounces"]:

        # Calculate changes
        grams = amount * 28.3495

        # Format strings
        grams = format_string(str(grams))

        formattedString = formattedAmount + f" ounces is " + grams + f" grams"

    elif unit in ["lb", "pound", "pounds"]:

        # Calculate changes
        kilograms = amount * 0.4535

        # Format strings
        kilograms = format_string(str(kilograms))

        formattedString = formattedAmount + f" pounds is " + kilograms + f" kilograms"

    # US volume
    elif unit in ["cup", "cups"]:

        # Calculate changes
        milliliters = amount * 236.588
        liters = amount * 0.2365

        # Format strings
        milliliters = format_string(str(milliliters))
        liters = format_string(str(liters))

        formattedString = formattedAmount + f" cups is:\n" + milliliters + f" milliliters\n" + liters + f" liters"

    elif unit in ["pt", "pint", "pints"]:

        # Calculate changes
        milliliters = amount * 473.176
        liters = amount * 0.4731

        # Format strings
        milliliters = format_string(str(milliliters))
        liters = format_string(str(liters))

        formattedString = formattedAmount + f" pints is:\n" + milliliters + f" milliliters\n" + liters + f" liters"

    elif unit in ["qt", "quart", "quarts"]:

        # Calculate changes
        milliliters = amount * 946.353
        liters = amount * 0.9463

        # Format strings
        milliliters = format_string(str(milliliters))
        liters = format_string(str(liters))

        formattedString = formattedAmount + f" quarts is:\n" + milliliters + f" milliliters\n" + liters + f" liters"

    elif unit in ["gal", "gallon", "gallons"]:

        # Calculate changes
        liters = amount * 3.7854

        # Format strings
        liters = format_string(str(liters))

        formattedString = formattedAmount + f" gallons is " + liters + f" liters"

    # US temperature
    elif unit in ["f", "fahrenheit"]:

        # Calculate changes
        celsius = (amount - 32) / 1.8

        # Format strings
        celsius = format_string(str(celsius))

        formattedString = formattedAmount + f"°F is " + celsius + f"°C"

    # Failure case
    else:
        return await embeds.desc_only(msg.channel, f"Invalid unit.")

    return await embeds.desc_only(msg.channel, formattedString)
