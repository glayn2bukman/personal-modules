"""
    Author: Bukman; glayn2bukman@gmail.com, +256-701-173-049, +256-783-573-700
    About:
    
    This module extends the "wx" library. The extended wxClasses are given a flexible __init__ method 
    allowing binding of an object at creation (as done in the Kivy library). 
    
    NB: for a wx class named as wx.Class, _wx presents the class as wxClass
    
    eg instead of
        
        -------------------------------------------------
        import wx
        app = wx.App()
        
        def on_evt(e): pass
        
        frame = wx.Frame(None, title="Test Window")
        btn = wx.Button(frame, label="My Btn")

        frame.Bind(wx.SIZE, on_evt)
        btn.Bind(wx.EVT_BUTTON, on_evt)

        menubar = wx.MenuBar()
        
        ID_SAVE, ID_QUIT = 1, 2
        
        _file = wx.Menu()
        _file.Append(ID_SAVE, "&Save\tCtrl+S") 
        _file.Append(ID_QUIT, "&Quit\tF12")
        
        frame.Bind(wx.EVT_MENU, on_evt, id=ID_SAVE)
        frame.Bind(wx.EVT_MENU, on_evt, id=ID_QUIT)
        
        menubar.Append(_file, "&File")

        frame.SetMenuBar(menubar)

        frame.Center()
        frame.Show()
        
        app.MainLoop()
        --------------------------------------------------

        our code would be;
        
        --------------------------------------------------
        from _wx import *
        app = wx.App()
        
        def on_evt(e): pass
        
        frame = wxFrame(None, title="Test Window", handlers={"size":on_evt, "paint":on_evt})
        btn = wxButton(frame, label="My Btn", handlers={"click": on_evt})

        menus = '''
            &File:
                &Save\tCtrl+S
                ---
                &Quit\tF12
        '''

        wxMenuBar(frame, menus, handlers=[on_evt]*2)
        
        frame.Center()
        frame.Show()
        
        app.MainLoop()
        --------------------------------------------------
        

"""

import wx

EVENTS = {"click":[wx.EVT_BUTTON, wx.EVT_LEFT_DOWN],
          "right_click": [wx.EVT_RIGHT_DOWN],
          "keyboard": [wx.EVT_KEY_DOWN],
          "mouse": [wx.EVT_MOUSE_EVENTS],
          "enter": [wx.EVT_TEXT_ENTER],
          "text": [wx.EVT_TEXT],
          "cursor_on": [wx.EVT_ENTER_WINDOW],
          "cursor_out": [wx.EVT_LEAVE_WINDOW],
          "move": [wx.EVT_MOVE, wx.EVT_MOTION],
          "select": [wx.EVT_RADIOBUTTON, wx.EVT_COMBOBOX, wx.EVT_LISTBOX, wx.EVT_SLIDER],
          "menu": [wx.EVT_MENU],
          "size": [wx.EVT_SIZE],
          "paint": [wx.EVT_PAINT],
          }

def init(*args, **kwargs):
    if "events" in kwargs:
        # events = {evt: handler}
        events = kwargs["events"]
        del(kwargs["events"])
    else:
        events = []

    args = list(args)

    args[1].__init__(*([args[0]]+args[2:]), **kwargs)

    for evt in events:
        if evt in EVENTS:
            for _evt in EVENTS[evt]:
                try:
                    args[0].Bind(_evt, events[evt])
                except: pass
        else:
            args[0].Bind(evt, events[evt])

class wxFrame(wx.Frame):
    def __init__(*args, **kwargs):
        args = list(args)
        args.insert(1, wx.Frame)
        init(*args, **kwargs)

class wxButton(wx.Button):
    def __init__(*args, **kwargs):
        args = list(args)
        args.insert(1, wx.Button)
        init(*args, **kwargs)

class wxSlider(wx.Slider):
    def __init__(*args, **kwargs):
        args = list(args)
        args.insert(1, wx.Slider)
        init(*args, **kwargs)

class wxStaticText(wx.StaticText):
    def __init__(*args, **kwargs):
        args = list(args)
        args.insert(1, wx.StaticText)
        init(*args, **kwargs)

class wxTextCtrl(wx.TextCtrl):
    def __init__(*args, **kwargs):
        args = list(args)
        args.insert(1, wx.TextCtrl)
        init(*args, **kwargs)

class wxComboBox(wx.ComboBox):
    def __init__(*args, **kwargs):
        args = list(args)
        args.insert(1, ComboBox)
        init(*args, **kwargs)

class wxListBox(wx.ListBox):
    def __init__(*args, **kwargs):
        args = list(args)
        args.insert(1, ListBox)
        init(*args, **kwargs)

class wxStaticBitmap(wx.StaticBitmap):
    def __init__(*args, **kwargs):
        args = list(args)
        args.insert(1, wx.StaticBitmap)
        init(*args, **kwargs)



class wxMenu:
    """
    For popup menus...
    """
    def __init__(_, parent, menu, handlers=[]):

        if type(menu)==type({}):
            _.menu = wxMenuBar(None).generate_menu(menu, {}, parent)[0]
        elif type(menu)==type(""):
            _.menu = wxMenuBar(None).generate_menu2(menu, handlers, parent)[0][0]
        else:
            raise ValueError("Invalid menu items! please refer to wxMenuBar for correct way of creating a menu")

        _.parent = parent
        
        _.parent.Bind(wx.EVT_CONTEXT_MENU, _.wxMenu_popup)

    def wxMenu_popup(_, e):
        pos = e.GetPosition()
        pos = _.parent.ScreenToClient(pos)
        _.parent.PopupMenu(_.menu)

class wxMenuBar(wx.MenuBar, wx.Menu):
    """
    A classic menubar
    """

    menu_item_types = ("__normal__", "radio", "check")

    def __init__(_, mom, menus="", handlers=[]):
        if mom==None: return
        # args[0] : instance
        # args[1] : wxFrame (menubar parent)
        # args[2] : one of type STR or type LIST
        # args[3] (for args[2] of type STR) : LIST of menu-item handlers in their order as created in in args[2]

        # **************** args[2] of type LIST ********************
        """
            menu = [menu_1, menu_2, ...menu_N], where menu_i is in format;
                {"Menu title":
                    [
                        (item-type[OPTIONAL], icon[OPTIONAL], item-title, item-help[OPTIONAL], wx.EVT_MENU handler),
                        ...
                    ]
                }
             
             NB: 
                1) THE MENUS CAN BE AS NESTED eg for menus with submenus...
                2) Acceptable item-type vales are "radio"(radiobutton) and check(checkbox). If left out, "normal" will be assumed
                3) "---" or "separator" as as a menu separatorh(horizontal line btn menu items)
        """
            # complete example of menus is
        """
            args[2] = [
                {"File":
                    [
                        ("new-file-icon.png", "New File\tCtrl+N", handler),
                        ("Save\tCtrl+S", handler),

                        "---", # item separator

                        ("radio", "male", handler),
                        ("radio", "female", handler),

                        "---",

                        {"Recent Docunents": # sub-menu
                            [
                                ("file-icon.png", "new.py", hanlder),
                                ("file-icon.png", "wx.py", handler),
                                ("file-icon.png", "clock.py", handler)
                            ]
                        }
                    ]
                },
                
                {"Settings":
                    [
                        ("check", "Show Color", handler),
                        ("check", "Use spec file", handler)
                    ]
                }
            ]
        """
        # **************************************************************
        
        # ******************** args[2] of type STR *********************
        """General format is;
            Menu:
                menu-item-type(optional); menu-item-icon(optional); menu-item
        """
        # for the same example of typ LIST args[2] above (note that for STR args[2], there must be LIST args[3]!);
        """
            args[2] = '''
                File:
                    new-file-icon.png; New File\tCtrl+N
                    Save\tCtrl+S
                    ---
                    radio; male
                    radio; female
                    ---
                    Recent Docunents:
                        file-icon.png; new.py
                        file-icon.png; wx.py
                        file-icon.png; clock.py

                Settings:
                    check; Show Color
                    check; Use spec file

           '''
           
           args[3] = [handler]*9
           
        """
        # *************************************************************

        _.mom = mom

        wx.MenuBar.__init__(_)

        if type(menus) in (type([]), type(())): # list menu
            for menu in menus:
                _.Append(*_.generate_menu(menu, {}))

        elif type(menus)==type(""): # string menu
            if handlers ==[]: raise ValueError("No handlers given for the menu items")

            for menu in _.generate_menu2(menus, handlers):
                _.Append(*menu)

        mom.SetMenuBar(_)

    def generate_menu(_, menu, created_menus={}, wxMenu_parent=None):
        # menu: menu dict eg {"File":[("save\tCtrl+S",handler), ("save As\tCtrl+Shift+S", handler)]}
        # created_menus={}: already created menus. formtat: {"menu title": wx.MenuObject}

        menu_title = menu.keys()[0]
        menu_title = menu_title if type(menu_title)==type("") else menu_title[0] # could be given as (title, help)

        if not ("MAIN-MENU" in created_menus):
            new_menu = wx.Menu()
            created_menus["MAIN-MENU"] = (new_menu, menu_title)
            created_menus[menu_title] = new_menu
        
        for menu_item in menu[menu_title]:
            if type(menu_item)==type({}): # submenu...
                submenu = menu_item.keys()[0]
                submenu = [submenu] if type(submenu)==type("") else submenu # could be given as (submenu-title, help)...

                menus = []

                for index, title in enumerate([menu_title, submenu[0]]):
                    if title in created_menus:
                        menus.append(created_menus[title])
                    else:
                        new_menu = wx.Menu()
                        created_menus[title] = new_menu
                        menus.append(new_menu)
                    
                menus[0].AppendSubMenu(*([menus[1]]+submenu))
        
                _.generate_menu(menu_item, created_menus, wxMenu_parent)

            else:
                if menu_title in created_menus:
                    mother_menu = created_menus[menu_title]
                else:
                    new_menu = wx.Menu()
                    created_menus[menu_title] = new_menu
                    mother_menu = new_menu
                
                if menu_item in ("---", "separator"):
                    mother_menu.AppendSeparator()
                    continue

                if not (type(menu_item) in (type(()), type([]))):
                    raise TypeError("a menu item should be a tuple or list")

                if len(menu_item)<2: 
                    raise ValueError("menu item must have 2-4 items")

                    # check for item-type...
                if menu_item[0] in _.menu_item_types:
                    menu_item_type = menu_item[0]
                    menu_item = menu_item[1:]
                else:
                    menu_item_type = "__normal__"
                
                    # check for item-icon...                
                if menu_item[0][-4:] in (".jpg", ".png", ".jpeg"):
                    icon = menu_item[0]
                    menu_item = menu_item[1:]
                else:
                    icon = None

                handler, menu_item = menu_item[-1], list(menu_item)
                
                ID = wx.NewId()
                
                if menu_item_type=="__normal__": new_item = mother_menu.Append(*([ID]+menu_item[:-1]))
                elif menu_item_type=="radio": new_item = mother_menu.AppendRadioItem(*([ID]+menu_item[:-1]))
                elif menu_item_type=="check": new_item = mother_menu.AppendCheckItem(*([ID]+menu_item[:-1]))
                
                if icon!=None: 
                    new_item.SetBitmap(wx.Bitmap(icon))
                    new_item.SetBackgroundColour("#009494")
                
                if handler!=None:
                    try:
                        _.mom.Bind(wx.EVT_MENU, handler, id=ID)
                    except: 
                        wxMenu_parent.Bind(wx.EVT_MENU, handler, id=ID)
                
        return created_menus["MAIN-MENU"]


    def generate_menu2(_, menus, handlers, wxMenu_parent=None):

        if menus=="": raise ValueError("The menu string provided is empty!")

        code = menus.split("\n")

        all_menus, main_menus, started = [], [], 0 

        footing, current_footing = 0, 0 # footing is the indentation of the first menu item ie the standard from 
                                        # which to measure other indentations...
                                        # current_footing is the indent of the current parent menu...
        item_number = -1

        for line in code:
            _line = line.strip()
            if _line == "": continue

            _footing = line.index(line.strip())

            if _line[-1]==":":
                menu = wx.Menu()

                if (not started):
                    footing = _footing
                    started = 1
                    current_footing = footing
                    
                    all_menus.append(menu)
                    main_menus.append((menu, _line[:-1]))
                    continue

                if _footing > current_footing: # submenu...
                    all_menus[-1].AppendSubMenu(menu, _line[:-1])
                    all_menus.append(menu)
                elif _footing <= current_footing:
                    del(all_menus[-1])
                    all_menus.append(menu)
                    if _footing == footing: # main menu
                        main_menus.append((menu, _line[:-1]))
                
                current_footing = _footing

                continue
            
            if _footing <= current_footing:
                if len(all_menus)>1: del(all_menus[-1])
                current_footing = _footing

            if _line in ("---", "separator"):
                if started:
                    all_menus[-1].AppendSeparator()
                continue
                

                # check for item-type...
            menu_item = [item.strip() for item in _line.split(";")]
            
            if menu_item[0] in _.menu_item_types:
                menu_item_type = menu_item[0]
                menu_item = menu_item[1:]
            else:
                menu_item_type = "__normal__"
            
                # check for item-icon...                
            if menu_item[0][-4:] in (".jpg", ".png", ".jpeg"):
                icon = menu_item[0]
                menu_item = menu_item[1:]
            else:
                icon = None

            menu_item = list(menu_item)
            
            item_number += 1
            
            try:
                handler = handlers[item_number]
            except: raise ValueError("number of handlers does not match number of menu items!")
            
            ID = wx.NewId()
            
            if menu_item_type=="__normal__": new_item = all_menus[-1].Append(*([ID]+menu_item))
            elif menu_item_type=="radio": new_item = all_menus[-1].AppendRadioItem(*([ID]+menu_item))
            elif menu_item_type=="check": new_item = all_menus[-1].AppendCheckItem(*([ID]+menu_item))
            
            if icon!=None: 
                new_item.SetBitmap(wx.Bitmap(icon))
                new_item.SetBackgroundColour("#009494")
            
            if handler!=None:
                try:
                    _.mom.Bind(wx.EVT_MENU, handler, id=ID)
                except: 
                    wxMenu_parent.Bind(wx.EVT_MENU, handler, id=ID)

        return main_menus

if __name__ == "__main__":
    app = wx.App()

    def handler(e): print "***"

    f = wxFrame(None, title="shit", events={"size":handler})

    wxButton(f, label="Click Me", events={"click":handler})

    menubar = [ # menus can be in list/dict form or string form; this is in list/dict form... 
        
        {"&File": # menu File
            [
                ("&Save\tCtrl+S", handler),
                ("&Close\tF12", handler)
            ]
        },
        
        { "&Settings":[ # menu settings
            ("Color", handler),

            { "&Look and Feel":[
                ("radio", "onStart", handler),
                ("radio", "onFinish", handler),
                "---",
                ("check", "vibrate", handler)  
              ]            
            }
        
          ]
        
        }
    
    ]
        
    wxMenuBar(f, menubar)    
    
    # for second menu example, menu is in string(the simpler) form
    popup_menu = """
    Actions:
        Copy
        Paste
        ---
        Cut
        ---
        Undo:
            check; undo-one
            radio; undo-two
            ---
            UN-FREAKIN-DO:
                ufd-1
                ufd-2
        ---
        ---
        Redo
    """
    
    wxMenu(f, popup_menu, [handler]*12)

    wxStaticText(f, label="Click Me...", pos=(50,50), events={"click":handler})
    
    f.Center(); f.Show()
        
    app.MainLoop()
