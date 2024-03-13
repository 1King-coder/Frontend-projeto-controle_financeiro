import customtkinter as ctk
from tkinter import TclError

class PageModel:

    def __init__ (self, master: 'ctk.CTk') -> None:

        self.master = master
        
        self.widgets = {
            name: [widget, list()] 
            for name, widget in ctk.__dict__.items()
            if "CTk" in name and name != "CTk" and name != "CTkBaseClass"
        }

        # This loop creates the methods to make a widget dinamicaly
        for widget_name in [*self.widgets]:
            
            setattr(
                self,
                widget_name[3:], # removes "CTk" from widget names
                self.gen_widget(widget_name)
            )

    def gen_widget(self, widget_name: str):
        # Wrapper function to generate a widget to be placed in the master's
        # window/container

        def widget (widget_config: dict, pos_config: dict) -> None:
            # Basically takes the widget object from the ctk module by
            # pulling its dict
            wid = ctk.__dict__[widget_name](self.master, **widget_config)

            self.add_widget(wid, pos_config)

            return wid

        return widget

    def build (self) -> bool:
        # Places the widgets in the window/container

        try:
            for _, widget_list in self.widgets.values():
                for widget in widget_list:
                    # widget[0] - Object | widget[1] - position config
                    try:
                        if 'row' in widget[1].keys():
                            widget[0].grid(**widget[1])
                            continue
                        
                        widget[0].place(**widget[1])

                    except TclError:
                        widget_list.remove(widget)
                        continue

            return True
        

        except Exception as e:
            print(f"An error has occurred while building the page {self.__class__}")
            print(e.args)
            return False
    
    def add_widget (self, widget, pos_config: dict) -> None:
        for wid_class , wid_list in self.widgets.values():

            if not isinstance(widget, wid_class):
                continue

            wid_list.append((widget, pos_config))

    
    


        
    