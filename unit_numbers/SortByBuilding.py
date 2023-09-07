def sort_by_building(unit_numbers):
    """
    Divides a list of unit numbers into buildings. 
    Each building has a distinct front and back side.

    Parameters:
        unit_numbers (int list): A list of unit numbers.

    Return:
        A dictionary with the following format: 
        {
            (int) : {
                "front" : (int list)
                "back" : (int list)
            }
        }
    """
    building_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    sides = ["front", "back"]
    split_buildings = {}
    ranges = {
        "front" : [
            (), (60, 73), (40, 49), (24, 33), (8, 17), (100, 105), 
            (206, 213), (108, 113), (218, 225), (134, 141), 
            (242, 252), (122, 129), (224, 234)
            ],
        "back" : [
            (), (48, 61), (32, 41), (16, 25), (0, 9), (200, 207), 
            (104, 109), (212, 219), (112, 117), (251, 261), 
            (128, 135), (233, 243), (116, 123)
            ],
    }
    
    for num in building_numbers:
        split_buildings[num] = {}
        for side in sides:
            split_buildings[num][side] = list(filter(
                lambda x: ranges[side][num][0] < x < ranges[side][num][1],
                unit_numbers
                ))
    return split_buildings