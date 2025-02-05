from colorama import Fore, Back, Style
from typing import List as _List, Tuple as _Tuple

_FORE_ALLOWED_VALUES =  [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
_BACK_ALLOWED_VALUES =  [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
_STYLE_ALLOWED_VALUES = [Style.DIM, Style.NORMAL, Style.BRIGHT]

class Formatted:
    _lines:_List[_Tuple[int,str]]
    # each line is a tuple of (indentation:int, text_line:str)
    _fore:_List[str]
    _back:_List[str]
    _style:_List[str]
    _expand_tabs_value:int

    def __init__(self,expand_tabs_value:int=3):
        self._style = [Style.NORMAL]
        self._fore = [Fore.WHITE]
        self._back = [Back.BLACK]
        self._lines = [(0,"")]
        self._expand_tabs_value = expand_tabs_value
    
    def indent(self,times:int=1):
        indt,text = self._lines[-1]
        indt += times
        self._lines[-1] = (indt, text)
        return self
    
    def unindent(self,times:int=1):
        indt, text = self._lines[-1]
        indt -= times
        if indt<0:
            indt = 0
        self._lines[-1] = (indt, text)
        return self
    
    def ret(self):
        indt = self._lines[-1][0]
        self._lines.append((indt, ""))
        return self
    
    def __raw_append(self,text:str):
        indt, line = self._lines[-1]
        line += text
        self._lines[-1] = (indt, line)

    def append(self, text:str,*,fore=None,back=None,style=None):
        if fore is not None:
            self._fore.append(fore)
            self.__raw_append(fore)
        if back is not None:
            self._back.append(back)
            self.__raw_append(back)
        if style is not None:
            self._style.append(style)
            self.__raw_append(style)
        self.__raw_append(text)
        if fore is not None:
            self.dropFore()
        if back is not None:
            self.dropBack()
        if style is not None:
            self.dropStyle()
        return self
    
    def fore(self,color:str):
        assert color in _FORE_ALLOWED_VALUES, f"Invalid fore color: {color}"
        self._fore.append(color)
        self.__raw_append(color)
        return self
    def back(self,color:str):
        assert color in _BACK_ALLOWED_VALUES, f"Invalid back color: {color}"
        self._back.append(color)
        self.__raw_append(color)
        return self
    def style(self,style:str):
        assert style in _STYLE_ALLOWED_VALUES, f"Invalid style: {style}"
        self._style.append(style)
        self.__raw_append(style)
        return self
    
    def dropFore(self):
        self._fore.pop()
        self.__raw_append(self._fore[-1])
        return self
    def dropBack(self):
        self._back.pop()
        self.__raw_append(self._back[-1])
        return self
    def dropStyle(self):
        self._style.pop()
        self.__raw_append(self._style[-1])
        return self
    

    def concatenate(self,formatted:"Formatted",*,inline=True):
        base_indt,base_text = self._lines[-1]
        numlines = len(formatted._lines)
        for n in range(numlines):
            indt,text = formatted._lines[n]
            if n!=0 or (not inline):
                self._lines.append((base_indt+indt,text))
            else:
                self._lines[-1] = (base_indt+indt, base_text+text)
        self._fore = formatted._fore
        self._back = formatted._back
        self._style = formatted._style
        return self
    
    def reset(self):
        self.append(Style.RESET_ALL)
        self._style = Style.NORMAL
        self._fore = Fore.WHITE
        self._back = Back.BLACK

    def __str__(self):
        delim = f"{Fore.RESET}{Back.RESET}{Style.RESET_ALL}"
        ret = ""
        for indt, text in self._lines:
            ret += f"\t"*indt + text + f"\n"
        ret = ret.expandtabs(self._expand_tabs_value)
        return delim + ret + delim
    
    def __repr__(self):
        return str(self)