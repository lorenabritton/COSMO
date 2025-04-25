import csv
import ast
import sys
from math import radians, cos, sin, asin, sqrt


disclaimer = 'Britton & Chen, LLC provides COSMO™ for informational purposes only. Users assume all risks associated with hiking and agree to hold harmless Britton & Chen, LLC for any injuries, damages, or losses resulting from the use of the tool. Users should independently verify all information provided. By using the tool, users acknowledge and accept these terms.'


print(f'\n\U0001F415  Welcome to COSMO™: Creating Opportunities for Savoring the Majestic Outdoors! \U0001F415\n\nNote:\n{disclaimer}\n')

trails = []
final_trails = []
top_5_trails = []

# first, we're building our list of hiking trails
def build_trails():
    global trails
    with open('rec_script/Hiking_Data_Large.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name of Hike']
            coordinates_str = row['Location (Latitude, Longitude)']
            coordinates = ast.literal_eval(coordinates_str)
            latitude, longitude = coordinates
            trail_data = {
                'Trail Name': name,
                'Difficulty': int(row['Difficulty']),
                'Length (mi)': float(row['Length']),
                'Latitude': latitude,
                'Longitude': longitude
            }
            trails.append(trail_data)

build_trails()

# 1: defining a function to get the user's desired hike duration
def get_duration():
    
    input_string_1 = """\n1) How much time do you have available for your hike? \n\nPlease input the time in hours, with minutes as decimals. (e.g. 3 hr, 45 min \u2192 3.75): """
    
    while True:
        try:
            duration = float(input(input_string_1))
            if duration <= 0:
                input_string_1 = '\nPlease input a positive value:\n'
            elif duration >= 10000:
                input_string_1 = '\nNo hiking trails found. Please input a smaller value:\n'
            else:
                return duration
        except ValueError:
            input_string_1 = '\nInvalid input. Please enter a number:\n'
            

# 2: defining the function to get the user's expertise level
def get_expertise():
    expertise_options = range(1,6)
    input_string_2 = """\n2) What is your level of expertise?\n\nLevel 1: Relaxed, low-effort. 
Level 2: Not very physically taxing, but you'll work harder than in Level 1. Might experience some mild elevation gain.
Level 3: Longer, more elevation gain. You should be able to comfortably complete a 5K/3-mile jog.
Level 4: More strenuous and technically challenging. 
Level 5: Tough.

Please enter a number from 1-5: """
    while True:
        try:
            expertise_level = int(input(input_string_2))
            if expertise_level not in expertise_options:
                 input_string_2 = '\nPlease input a number from the list of options 1-5:\n'
            else:
                return expertise_level
        except ValueError:
            input_string_2 = '\nInvalid input. Please enter a number from the options:\n'

# 3: defining a function to get user's desired hike difficulty
def get_difficulty(expertise_level):
    difficulty_options = range(1,6)
    input_string_3 = """\n3) How difficult would you like your hike to be? 

Please enter a number from 1-5: """
    
    while True:
        try:
            difficulty_level = int(input(input_string_3))
            if difficulty_level not in difficulty_options:
                input_string_3 = '\nPlease input a number from the list of options 1-5:\n'
            else:
                if difficulty_level > expertise_level:
                    difference(expertise_level, difficulty_level)
                    return difficulty_level
                else:
                    return difficulty_level
        except ValueError:
            input_string_3 = '\nInvalid input. Please enter a number from the options:\n'

# handling differences between expertise level and difficulty level
def difference(expertise_level, difficulty_level):  
    while True:
        if 2 <= difficulty_level <= 5:
            diff = difficulty_level - expertise_level
            print(f'\nThe difficulty level is {diff} level(s) above your expertise level.')
            if diff == 1:
                diff_confirm = input(f'\nWould you like to continue? (Y/N) ').strip().upper()
                if diff_confirm == 'Y': # originally !=
                    break
                else:
                    print('\nExiting...')
                    sys.exit()
          
            if diff > 1:
                diff_confirm_q = input(f'\nWould you like to input a lower difficulty level? (Y/N)').strip().upper()
                if diff_confirm_q != 'Y':
                    print('\nUnable to recommend hikes at this level. \n\nExiting...')
                    sys.exit()
                else:
                    get_difficulty(expertise_level)
        else:
            print('\nDifficulty level is appropriate for your level of expertise.')
        break

# calculating distances to each hiking trail
def distance_math(user_lat, user_long, hike_lat, hike_long):
    # conversion of decimal degrees to radians 
    user_long_rad, user_lat_rad, hike_long_rad, hike_lat_rad = map(radians, [user_long, user_lat, hike_long, hike_lat])

    # Haversine formula 
    dlon = hike_long_rad - user_long_rad
    dlat = hike_lat_rad - user_lat_rad
    a = sin(dlat/2)**2 + cos(user_lat_rad) * cos(hike_lat_rad) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    # Limit decimals
    km = int('%.0f' % km)
    mi = km * 0.621371
    return mi

# creating a function to recommend trails based on user preferences
def algorithm(duration, expertise_level, difficulty_level):
    # different paces correspond with different expertise levels
    pace = {1: 60, 2: 50, 3: 45, 4: 38, 5: 34}.get(expertise_level, 0)
    # the adjusted pace takes into account the difficulty level of the hike
    adjusted_pace = pace + (2 * (difficulty_level - 1))
    # using dimensional analysis to get how far our user could go
    # duration is multiplied by 60 to convert from hours to minutes
    # adjusted_pace has the units of min/mile
    farthest_user_can_go = (duration * 60) / adjusted_pace

    for trail in trails:
        # filter based on difficulty level
        trail_difficulty = trail['Difficulty']
        # filter based on length
        length_mi = trail['Length (mi)']
        length_difference = length_mi - farthest_user_can_go

        # matching difficulty level
        if difficulty_level == trail_difficulty:
            # finding suitable length of trail
            # if the difference is negative, we add it
            # if the difference is positive and less than 
            if length_difference >= 3 or length_difference < 0:
                final_trails.append(trail)


        final_trails.sort(key=lambda x: abs(farthest_user_can_go - x['Length (mi)']))
        top_5_trails = final_trails[:5]
  
    
    # sorting trails by distance from user's location
def trails_f():
    # Input user's current location (set at Harvard's campus, Cambridge, MA)
    user_lat = float(42.2216)
    user_long = float(-71.0655)
    print('\nYour current location is ({}, {})'.format(user_lat, user_long) + 
         ': Cambridge, MA')
    # in future work, we would attempt to find the user's location based on their IP address. For our current model, we have set the user's location to be in Cambridge, MA.

    # Sort trails based on distance from user's inputted location
    top_5_trails.sort(key=lambda x: distance_math(user_lat, user_long, x['Latitude'], x['Longitude']))

    # Printing the three closest trails and their distances
    print('\nThe three matches closest to you are below!')
    for trail in final_trails[:3]:
        star = '\u2B50'
        #redefining variables within the loop so that apppropriate information can be printed
        difficulty_level = trail['Difficulty']
        length_mi = trail['Length (mi)']
        
        distance = distance_math(user_lat, user_long, trail['Latitude'], trail['Longitude'])
        stripped_trail_name = trail['Trail Name'].rstrip('\n')
        print(f'\n{stripped_trail_name} ({"{:.1f}".format(distance)} miles away)\n'
              
f'Difficulty: {star*difficulty_level} | Length: {length_mi} mi')
    


# Call the functions sequentially
duration = get_duration()
print('\n~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*')
expertise_level = get_expertise()
print('\n~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*')
difficulty_level = get_difficulty(expertise_level)
print('\n~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*')
algorithm(duration, expertise_level, difficulty_level)
trails_f()
