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
-

'''

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

    def look(self):
        self.location.generate_desc()

    def move(self, new_loc):
        if new_loc in self.location.connected_locs:
            self.location = new_loc
            self.location.generate_desc()
        
        '''
        if self.location.connected_locs[0].open == False:
            print(f"cannot go to {self.location.connected_locs[0].name}, its locked")
        else:
        # if you cannot pass because the path is blocked, tell the player
        # if you can pass, you do
            self.location = self.location.connected_locs[0]
            self.location.generate_desc()
        '''
    def take(self, primary_object):
        # this will need an update for sure
        self.inventory.append(self.location.known_items.pop(self.location.known_items.index(primary_object)))
        print(f"you took: {primary_object.name}")

        '''
        self.inventory.append(self.location.known_items.pop(1))
        print(f"you took: {get_names(self.inventory)}")
        '''

    def use(self, primary_object, secondary_object = None):
        '''
        primary object: the thing we are operating
        secondary object: a modifier, a key or something in our inventory

        if there's no key to the object, we just use it
        '''
        if primary_object.keys == None:
            # flip switch / open box
            primary_object.use()
            for object in primary_object.sub_items:
                self.location.known_items.append(object)
        elif secondary_object in primary_object.keys:
            # open locked door / break window w/ blunt object
            primary_object.use()
        else:
            print("that doesn't work :'C")
        '''
        if  self.inventory[0] in self.location.connected_locs[0].keys:
            self.location.connected_locs[0].open = True
            print(f"{self.inventory[0].name} used!")
        elif self.location.known_items[0].keys == None:
            print("using!")
        else:
            print("not used!")
        '''

    def handle_input(self):
        user_input = input(">")
        if "take" in user_input :
            pass

class Location():
    '''
    maybe location should be more like "node" some completely abstract location where you can interact with only certain objects while you're there
    if you open a box should you be at the box node until you leave it? its more like a workspace than a place
    - when you're at a desk, you can only do desk things
    - when you open the drawer you can only do drawer things

    naw thats werid, what happens if a monster wants to beat you up and you go to the "drawer" location???
    '''

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
        print(f"you stand in a {self.name}. you see: {known_items_list}, nearby: {locs_list}")
        pass

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

    def use(self):
        print(f"you use the {self.name}")
        #print(get_names(self.sub_items))
        # add sub items to known items?
        pass

def main():
    '''
    '''
    
    item_a = Item()
    item_a.name = "box key"

    item_b = Item()
    item_b.name = "box"
    item_b.keys = [item_a]

    item_c = Item()
    item_c.name = "shelf"

    item_d = Item()
    item_d.name = "red book"
    item_e = Item()
    item_e.name = "blue book"

    item_c.sub_items =[item_d,item_e]

    loc_a = Location()
    loc_a.name = "kitchen"

    loc_b = Location()
    loc_b.name = "dining room"
    #loc_b.keys = [item_a, item_b]
    loc_b.open = False

    loc_a.known_items = [item_a,item_b,item_c]
    loc_a.connected_locs.append(loc_b)

    new_player = Player()
    new_player.location = loc_a
    
    new_player.look()
    new_player.take(item_a)
    #new_player.take(item_d)
    
    #new_player.move()
    new_player.use(item_c)
    #new_player.move()
    new_player.look()
    new_player.take(item_e)
    new_player.move(loc_b)




if __name__ == "__main__":
    main()