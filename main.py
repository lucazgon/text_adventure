'''
mini text adventure game!
- think escape room
- think dnd / zelda

vertical slice:
room theme: 
- do the thing you don't want to do early rather than later (i'm literaly not doing that now lol)
- whats done can't be undone
- life is short enjoy it
- things tend to be stronger with moderation of everything

- a shy magical entity wants to bring you joy and has stuck you inside a room hoping some of the stories or artifacts will give 
you a new lease on life

- wake up, bed, side table, window, large kitchen table, locked door, piping hot tea, roaring fire contained in a rock, book shelf
- look at the tea, its hot! 
- you're not at the table w/ the tea, you're in bed still
- move to table
- you're at the table
- look at the table
- theres tea, a note, 
- drink the tea, its scalding, you burnt the heck out of your lips, theres 3/4 of tea left
- theres something under the tea, a key!
- look at the door,  
- the door is beautifully carved oak, it has a small figure standing infront of the sun with the moon nd the starts towering over them. 
- try the tea on the door
- the tea doesnt work on the door
- try the key on the door
- the door opens!

What did I learn from this?
- inside a room has interconnected nodes that may not need to be represented by grid locations?
- when you enter a room it should describe "generally" all the nodes
- when you enter a node, a more in depth description should be given / list all "known" objects
- unknown objects should be added to the known list after a condition is met (moving a painting etc)
- what if objects are in a drawer, and the drawer is closed? the "known objects" should change. 
- maybe a container object. if key provided openable. sometimes not closable (if broken)

Things that I think would be cool / should include
- ability for the user to type and act
- keyword keys. if you want to destroy a glass case, using anything that is large, heavy or a weapon should be able to do the trick!
- locked pathways, you can go around, or find a key


'''

import os

def get_names(list):
    names_list = []
    for item in list:
        names_list.append(item.name)
    return names_list

class Player():
    def __init__(self):
        self.name = "d_name"
        self.inventory = []
        self.location = None
        self.actions = {"look" : self.look,
                        "take" : self.take,
                        "drop" : self.drop,
                        "use" : self.use,
                        "inventory" : self.show_inventory,
                        "move" : self.move}

    def look(self, primary_object = None):
        objects = self.parse_items()
        if len(objects) > 0:
            print(objects[0].desc)
        else:
            self.location.generate_desc()

    def move(self):
        locs = self.parse_locs()

        if len(locs) > 0:
            new_loc = locs[0]
            if new_loc in self.location.connected_locs:
                self.location = new_loc
                self.location.generate_desc()
        else:
            print("where?")

    def take(self):
        objects = self.parse_items()
        for object in objects:
        # this will need an update for sure
            self.inventory.append(self.location.known_items.pop(self.location.known_items.index(object)))
            print(f"you took: {object.name}")
    
    def drop(self):
        objects = self.parse_items()
        for object in objects:
        # this will need an update for sure
            self.location.known_items.append(self.inventory.pop(self.inventory.index(object)))
            print(f"you dropped: {object.name}")


    def use(self):
        '''
        primary object: the thing we are operating
        secondary object: a modifier, a key or something in our inventory

        if there's no key to the object, we just use it
        '''
        objects = self.parse_items()

        if len(objects) == 1:
            primary_object = objects[0]
            if primary_object.keys == None:
                # flip switch / open box
                primary_object.use()
            for object in primary_object.sub_items:
                self.location.known_items.append(object)
        elif len(objects) == 2:
            if objects[0] in objects[1].keys:
                # open locked door / break window w/ blunt object
                objects[0].use()
        else:
            print("that doesn't work :'C")
    
    def show_inventory(self):
        print(get_names(self.inventory))

    def parse_locs(self):
        locs = []

        for loc in self.location.connected_locs:
            if loc.name in self.user_input:
                print(loc.name)
                locs.append(loc)
        
        return locs


    def parse_items(self):
        # this is probably too broad, I probably want to split into multiple pieces 

        items = []
        #items in inventory
        for item in self.inventory:
            if item.name in self.user_input:
                #print(item.name)
                items.append(item)
        
        #items on location
        for item in self.location.known_items:
            if item.name in self.user_input:
                #print(item.name)
                items.append(item)
        
        return items

    
    def handle_input(self):
        self.user_input = input(">")
        actions = []

        # split up the input to find the first action word
        # bassed on the word found, we should probably split it up into different categories maybe
        input_split = self.user_input.split(" ")
        for word in input_split:
            if word in self.actions:
                #print(word)
                actions.append(word)
        
        if len(actions) == 1:
            self.actions[actions[0]]()
        else:
            print("action unclear")
     
        # if items have names longer than one word, we are gonna have major issue
        # okay now we need locations in here as well... try to determine the action first  

class Location():

    def __init__(self):
        self.name = "d_name"
        self.desc = "d_desc"

        self.known_items = []
        self.connected_locs = []

        # kind of works, but doesn't lock down specific pathways :/
        self.keys = None
        self.open = True

    def generate_desc(self):
        # print where you are, a list of objects close at hand, a list of connected locations
        known_items_list = []
        locs_list = []
        for item in self.known_items:
            known_items_list.append(item.name)
        for loc in self.connected_locs:
            locs_list.append(loc.name)
        print(f"{self.name}\nyou see: {known_items_list}, paths: {locs_list}")
        print(self.desc)

class Item():
    def __init__(self):
        # maybe items should obstruct pathways rather than certain pathways being "locked"
        # while door is here, obstruct player movement to other room
        # this doesn't work if there are 2 ways to get into another room (window / door)
        self.name = "d_name"
        self.desc = "d_desc"

        self.open = True
        self.sub_items = []
        self.obstructed_locs = []
        self.keys = None
        self.trigger = False

    def use(self):
        print(f"you use the {self.name}")
        if self.trigger == True:
            self.trigger = False
        else:
            self.trigger = True

def golem_scenario():
    
    # item definitions

    # player items
    note = Item()
    note.name = "king's note"
    note.desc = "hello brave adventurer, please clear out this musty cave for me. thank you!"

    sword = Item()
    sword.name = "longsword"
    sword.desc = "it's the cheapest sword money can buy"

    # room 1 items
    golem = Item()
    golem.name = "d_name"
    golem.desc = "d_desc"

    desk = Item()
    desk.name = "d_name"
    desk.desc = "d_desc"

    coin_pouch = Item()
    coin_pouch.name = "coin pouch"
    coin_pouch.desc = "a small leather pouch made from the hide of a creature that no longer roams the earth. it holds 5 coins"

    skeleton = Item()
    skeleton.name = "skeleton"
    skeleton.desc = "the skeleton is wearing tattered fancy robes. their rib cage has been shattered"
    skeleton.sub_items = [coin_pouch]

    curtain = Item()
    curtain.name = "curtain"
    curtain.desc = "age has left its mark on this curtain. a drawstring rests to the side of it"
    curtain.sub_items = []

    # item connections

    # room definitions

    entrance = Location()
    entrance.name = "entrance"
    entrance.desc = "this is a massive stone carved room with a large ornate desk in the center.\n\
A satin purple curtain covers the back wall.\n\
There are skeletons and stone statues dotted about the room."
    entrance.known_items = [skeleton,curtain]

    trophy_room = Location()
    trophy_room.name = "trophy room"
    trophy_room.desc = "this is a dome shaped room. \
There are statues placed on plinths in a semicircle. \
There are many paintings spread out along the wall."


    security_checkpoint = Location()
    security_checkpoint.name = "security checkpoint"
    security_checkpoint.desc = "this is a long hallway.\
there is a bust of a statue affixed to a round base in the middle of the room. \
tn front of the statue is a desk and a notice board with a bunch of scraps of paper that appear to be warning signs. "

    # room connections

    
    entrance.connected_locs = [security_checkpoint,trophy_room]
    trophy_room.connected_locs = [entrance]
    security_checkpoint.connected_locs = [entrance]
    
    new_player = Player()
    new_player.location = entrance
    new_player.inventory = [sword,note]

    while True:
        
        new_player.handle_input()
        #os.system("clear")
    pass

def main():

    golem_scenario()
    return

if __name__ == "__main__":
    main()

'''
room title

2 sentences describing the general look of the room

1 sentence describing ways to go
'''