#
#    Beta version of Mordenized Tk, 
#    some method is not defined or working.
#

import tkinter as t

import typing

def _round_rectangle(x1, y1, x2, y2, r, c, **kwargs):
        points = [x1+r, y1,
                x1+r, y1,
                x2-r, y1,
                x2-r, y1,
                x2, y1,
                x2, y1+r,
                x2, y1+r,
                x2, y2-r,
                x2, y2-r,
                x2, y2,
                x2-r, y2,
                x2-r, y2,
                x1+r, y2,
                x1+r, y2,
                x1, y2,
                x1, y2-r,
                x1, y2-r,
                x1, y1+r,
                x1, y1+r,
                x1, y1]

        return c.create_polygon(points, **kwargs, smooth=True)


class MTk(t.Tk):
    def __init__(self, background = None, *args) -> None:
        super().__init__()
        self.c = t.Canvas(background=('gray20', background)[background is not None], *args)
        self.background = background

        self.c.bind("<Button-1>", self._on_click)
        self.c.bind("<Motion>", self._on_motion)

        self._registered_buttons = {}
        self._current_selected = -1
        self._current_selected_color = 'green3'

        self.c.pack(fill=t.BOTH, expand=t.YES)
    
    def configure(self, background = None, *args) -> None:
        self.c.configure(background=(self.background, background)[background is not None], *args)
        self.configure(*args)

    def _register_button(self, id:int, x1:float, y1:float, x2:float, y2:float, 
                         command, args:dict[str,typing.Any], 
                         selected:str,
                         deselected:str) -> None:
        self._registered_buttons[x1, y1, x2, y2] = (id, command, args, selected, deselected)
    
    def _forget_button(self, id:int) -> None:
        for currentid, currentkey in (self._registered_buttons.values(), self._registered_buttons.keys()):
            if id == currentid:
                del self._registered_buttons[currentkey]
                break
    
    def _on_click(self, event) -> None:
        x, y = event.x, event.y
        for x1, y1, x2, y2 in self._registered_buttons:
            if x1 <= x <= x2 and y1 <= y <= y2 and self._registered_buttons[x1, y1, x2, y2][1] is not None:
                self._registered_buttons[x1, y1, x2, y2][1].__call__(*self._registered_buttons[x1, y1, x2, y2][2])
                break
    
    def _on_motion(self, event) -> None:
        x, y = event.x, event.y

        for x1, y1, x2, y2 in self._registered_buttons:
            if (x1 <= x <= x2 and y1 <= y <= y2) and self._current_selected != self._registered_buttons[x1, y1, x2, y2][0]:
                self.c.itemconfig(self._current_selected, fill = self._current_selected_color)
                self._current_selected = self._registered_buttons[x1, y1, x2, y2][0]
                self._current_selected_color = self._registered_buttons[x1, y1, x2, y2][4]
                self.c.itemconfig(self._current_selected, fill = self._registered_buttons[x1, y1, x2, y2][3])
                self.c.config(cursor="hand2")
                return
            
            elif (x1 <= x <= x2 and y1 <= y <= y2) and self._current_selected == self._registered_buttons[x1, y1, x2, y2][0]:
                return
            
        if self._current_selected != -1:
            self.c.itemconfig(self._current_selected, fill = self._current_selected_color)
            self.c.config(cursor="arrow")
            self._current_selected = -1

    def create_rectangle(self, *args, **kwargs) -> int:
        return self.c.create_rectangle(*args, **kwargs)
    
    def create_oval(self, *args, **kwargs) -> int:
        return self.c.create_oval(*args, **kwargs)
    
    def create_polygon(self, *args, **kwargs) -> int:
        return self.c.create_polygon(*args, **kwargs)
    
    def create_line(self, *args, **kwargs) -> int:
        return self.c.create_line(*args, **kwargs)
    
    def create_text(self, *args, **kwargs) -> int:
        return self.c.create_text(*args, **kwargs)
    
    def create_image(self, *args, **kwargs) -> int:
        return self.c.create_image(*args, **kwargs)
    
    def create_arc(self, *args, **kwargs) -> int:
        return self.c.create_arc(*args, **kwargs)
    
    def __str__(self) -> str:
        return super().title()
    
    def __repr__(self) -> str:
        return super().__repr__()
    
class Panal(object):
    def __init__(self, 
                 master:MTk,
                 x1:float, y1:float, x2:float, y2:float,
                 r:int,
                 color:str = None,
                 shadow:bool = None,
                 shadow_color:str = None,
                 shadow_offset:int = None,
                 shadow_direction:str = None) -> None:
        self.master = master
        self.args = dict(r=r, color=("green3", color)[color is not None], shadow=(False, shadow)[shadow is not None], shadow_offset=shadow_offset, shadow_direction=shadow_direction, shadow_color=("black", shadow_color)[shadow_color is not None])
        self.pos = (x1, y1, x2, y2)

        self.shadow = -1
        if shadow:
            shadowx1 = x1
            shadowx2 = x2
            shadowy1 = y1
            shadowy2 = y2

            if shadow_offset is None or shadow_offset < 0:
                raise ValueError("shadow_offset must be specified or bigger than 0")
            if shadow_direction is None:
                raise ValueError("shadow_direction must be specified")
            
            if shadow_direction.__contains__("n") or shadow_direction.__contains__("N"):
                shadowy1 -= shadow_offset
                shadowy2 -= shadow_offset
            if shadow_direction.__contains__("s") or shadow_direction.__contains__("S"):
                shadowy1 += shadow_offset
                shadowy2 += shadow_offset
            if shadow_direction.__contains__("w") or shadow_direction.__contains__("W"):
                shadowx1 -= shadow_offset
                shadowx2 -= shadow_offset
            if shadow_direction.__contains__("e") or shadow_direction.__contains__("E"):
                shadowx1 += shadow_offset
                shadowx2 += shadow_offset
            
            self.shadow = (_round_rectangle(shadowx1, shadowy1, shadowx2, shadowy2, r, master.c, fill = ("gray15", shadow_color)[shadow_color is not None]))

        self.ids = []
        self.ids.append(_round_rectangle(x1, y1, x2, y2, r, master.c, fill = ("green3", color)[color is not None]))
        self.ids.append(self.shadow)
        
    def configure(self, 
                  r:int = None,
                  color:str = None,
                  shadow:bool = None,
                  shadow_color:str = None,
                  shadow_offset:int = None,
                  shadow_direction:str = None) -> typing.Any: ...

    def forget(self) -> None:
        for i in range(len(self.ids)):
            self.master.c.delete(self.ids[i])
    
    def __str__(self) -> str:
        return f'Panal object in {self.master} with id {self.ids}'
    
    def __repr__(self) -> str:
        return f'Panal(master={self.master}, args={self.args}, pos={self.pos}, id={self.ids})'

class Text(object):
    def __init__(self,
                 master:MTk,
                 x:float, y:float,
                 text:str,
                 color:str = None,
                 font:str = None) -> None:
        self.master = master
        self.args = dict(text=text, color=("white", color)[color is not None], font=("{Seoge UI}", font)[font is not None])
        self.pos = (x, y)
        
        self.ids = []
        self.ids.append(self.master.c.create_text(x, y, text=text, fill = ("white", color)[color is not None], font=("{Seoge UI}", font)[font is not None]))
    
    def configure(self, 
                    text:str = None, 
                    color:str = None) -> typing.Any: ...
    
    def forget(self) -> None:
        for i in range(len(self.ids)):
            self.master.c.delete(self.ids[i])
    
    def __str__(self) -> str:
        return f'Text object in {self.master} with id {self.ids}'
    
    def __repr__(self) -> str:
        return f'Text(master={self.master}, args={self.args}, pos={self.pos}, id={self.ids})'

class ProgressBar(object):
    def __init__(self,
                 master:MTk,
                 x1:float, y1:float, x2:float, y2:float,
                 background:str = None,
                 color:str = None) -> None:
        self.value = 100

        self.master = master
        self.args = dict(background=("gray15", background)[background is not None], color=("green3", color)[color is not None])
        self.pos = (x1, y1, x2, y2)
        
        self.ids = []

        self.ids.append(_round_rectangle(x1, y1, x2, y2, y2-y1, master.c, fill=("gray15", background)[background is not None]))
        self.ids.append(_round_rectangle(x1, y1, x2, y2, y2-y1, master.c, fill=("green3", color)[color is not None]))
    
    def update(self, value:int) -> None:
        if value > 100:
            raise ValueError("value must be between 0 and 100")
        
        self.value = value
        self.master.c.delete(self.ids[1])
        self.ids[1] = _round_rectangle(self.pos[0], self.pos[1], ((self.pos[2] - self.pos[0]) * (value / 100)) + self.pos[0], self.pos[3], self.pos[3] - self.pos[1], self.master.c, fill = self.args["color"])
    
    def configure(self, 
                    background:str = None, 
                    color:str = None) -> typing.Any: ...
    
    def forget(self) -> None:
        for i in range(len(self.ids)):
            self.master.c.delete(self.ids[i])
    
    def __str__(self) -> str:
        return f'ProgressBar object in {self.master} with id {self.ids}'
    
    def __repr__(self) -> str:
        return f'ProgressBar(master={self.master}, args={self.args}, pos={self.pos}, id={self.ids}, currentProgress={self.value})'
    
class Button(object):
    def __init__(self,
                 master:MTk,
                 x1:float, y1:float, x2:float, y2:float,
                 r:int,
                 text:str,
                 background:str = None,
                 selectedcolor:str = None,
                 textcolor:str = None,
                 font:str = None,
                 shadow:bool = None,
                 shadow_color:str = None,
                 shadow_offset:int = None,
                 shadow_direction:str = None,
                 disablecolor:str = None,
                 command = None) -> None:
        self.master = master
        self.args = dict(r=r, background=("green3", background)[background is not None], textcolor=("white", textcolor)[textcolor is not None], shadow=(False, shadow)[shadow is not None], shadow_offset=shadow_offset, shadow_direction=shadow_direction, shadow_color=("gray15", shadow_color)[shadow_color is not None], disablecolor=("gray50", disablecolor)[disablecolor is not None], font=("{Seoge UI}", font)[font is not None], command = command, selectedcolor=("green4", selectedcolor)[selectedcolor is not None])
        self.pos = (x1, y1, x2, y2)
        
        self.shadow = -1
        if shadow:
            shadowx1 = x1
            shadowx2 = x2
            shadowy1 = y1
            shadowy2 = y2

            if shadow_offset is None or shadow_offset < 0:
                raise ValueError("shadow_offset must be specified or bigger than 0")
            if shadow_direction is None:
                raise ValueError("shadow_direction must be specified")
            
            if shadow_direction.__contains__("n") or shadow_direction.__contains__("N"):
                shadowy1 -= shadow_offset
                shadowy2 -= shadow_offset
            if shadow_direction.__contains__("s") or shadow_direction.__contains__("S"):
                shadowy1 += shadow_offset
                shadowy2 += shadow_offset
            if shadow_direction.__contains__("w") or shadow_direction.__contains__("W"):
                shadowx1 -= shadow_offset
                shadowx2 -= shadow_offset
            if shadow_direction.__contains__("e") or shadow_direction.__contains__("E"):
                shadowx1 += shadow_offset
                shadowx2 += shadow_offset
            
            self.shadow = (_round_rectangle(shadowx1, shadowy1, shadowx2, shadowy2, r, master.c, fill = ("gray15", shadow_color)[shadow_color is not None]))

        self.ids = []
        self.ids.append(_round_rectangle(x1, y1, x2, y2, r, master.c, fill=("green3", background)[background is not None]))
        self.ids.append(self.master.c.create_text((x1+x2)/2, (y1+y2)/2, text=text, fill = ("white", textcolor)[textcolor is not None], font=('{Seoge UI}', font)[font is not None]))
        self.ids.append(self.shadow)

        self.enabled = True
        self._enable()
    
    def configure(self, 
                  r:int = None, 
                  background:str = None, 
                  selectedcolor:str = None,
                  textcolor:str = None, 
                  shadow:bool = None, 
                  shadow_color:str = None, 
                  shadow_offset:int = None, 
                  shadow_direction:str = None, 
                  disablecolor:str = None, 
                  command = None) -> typing.Any: ...

    def forget(self) -> None:
        self._disable(self)
        for i in range(len(self.ids)):
            self.master.c.delete(self.ids[i])
    
    def __str__(self) -> str:
        return f'Button object in {self.master} with id {self.ids}'
    
    def __repr__(self) -> str:
        return f'Button(master={self.master}, args={self.args}, pos={self.pos}, id={self.ids})'
    
    def _enable(self) -> None:
        self.master._register_button(self.ids[0], self.pos[0], self.pos[1], self.pos[2], self.pos[3], self.args["command"], {}, self.args['selectedcolor'], self.args['background'])
        self.enabled = True

    def _disable(self) -> None:
        self.master._forget_button(self.ids[0])
        self.master.c.itemconfig(self.ids[0], background=self.args['disablecolor'])
        self.enabled = False
    
    def state(self, state:str):
        if state == 'normal':
            self._enable()
        elif state == 'disabled':
            self._disable()
        else:
            raise ValueError('Unknown state %s' % state)

class Image(object):
    def __init__(self,
                 master:MTk,
                 x:float, y:float,
                 image:t.PhotoImage) -> None:
        self.master = master
        self.args = dict(image=image)
        self.pos = (x, y)

        self.ids = []
        self.ids.append(self.master.c.create_image(self.pos[0], self.pos[1], image=image))
    
    def configure(self, 
                    image:t.PhotoImage = None) -> typing.Any:...
    
    def forget(self) -> None:
        for i in range(len(self.ids)):
            self.master.c.delete(self.ids[i])

    def __str__(self) -> str:
        return f'Image object in {self.master} with id {self.ids}'
    
    def __repr__(self) -> str:
        return f'Image(master={self.master}, args={self.args}, pos={self.pos}, id={self.ids})'