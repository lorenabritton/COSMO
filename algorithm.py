"""
Questions 1 to 3 take a user's input, and then output a value between 1 and 5. 

q1_duration: returns duration (a decimal)

q2_expertise: returns expertise_level

q3_difficulty: returns difficulty_level



The .csv file contains the name of the hike, and then the distance and the difficulty. 

Hike_name | Difficulty | Length | Distance
"""



from main_rec import trails
import q1_duration
import q2_expertise
import q3_difficulty

def algorithm():
    duration = float(q1_duration.get_duration())
    # _, pace = q2_expertise.get_expertise()
    # difficulty_level = int(q3_difficulty.get_difficulty()) - 1 
    
    expertise_level, _ = q2_expertise.get_expertise()
    difficulty_level = int(q3_difficulty.get_difficulty(expertise_level)) - 1
    #subtracting by 1 makes difficulty_level go from 0-4
    
    
    
    # pace depends on expertise level
    adjusted_pace = pace + (2*int(difficulty_level))
    print(pace)
    print(adjusted_pace)
    
    farthest_user_can_go = (duration*60) / adjusted_pace  #  = distance (mi)
    print(farthest_user_can_go)
    
    for trail in trails:
        length_mi = trail['Length (mi)']
        # print(f"Length of '{trail['Trail Name']}': {length_mi} miles")
        length_difference = length_mi - farthest_user_can_go
        if length_difference >= 3:
            trails.remove(trail)
            
    
    print(trails)
    
    
    
    
    # for trail in trails:
    #     if trail[length] - farthest_user_can_go >= 3: #3 is an arbitrary value
    #         acceptable_hikes.remove(hike)


if __name__ == '__main__':
    algorithm()

