import pygame, sys, webbrowser, os
from CONFIG import *
from datetime import datetime
from pathlib import Path

PATH = (os.path.dirname(os.path.realpath(__file__)))[:-4]

class interface(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
        pygame.display.set_caption(WINDOW_TITLE)
        try:
            icon = pygame.image.load('../images/icon.png')
            pygame.display.set_icon(icon)
        except:
            pass
    def refresh(self,objects=None):
        self.screen.fill((0,0,0))
        if objects != None and isinstance(objects,list):
            for obj in objects:
                if hasattr(obj,'draw'):
                    obj.draw(self.screen)
                else:
                    print(f'Failed to draw object {obj} due to missing function: draw(scr)')
        pygame.display.flip()
        self.clock.tick(30)

class button(object):
    def __init__(self,rect,boxcol1,boxcol2=None,string1=None,string2=None,font=None,size=32):
        self.button = pygame.Rect(rect)
        self.expandupwards = False
        self.init_height = self.button.h
        self.init_y = self.button.y
        self.colour_passive = boxcol1
        self.colour = self.colour_passive
        self.stayselected = False
        if boxcol2 != None:
            self.colour_active = boxcol2
        if string1 != None:
            self.font = pygame.font.Font(font,min(self.button.h-2,size))
            self.string_passive = string1
            self.string = self.string_passive
            if isinstance(string1,list) or isinstance(string1,tuple):
                string = string1[0].split('\n')
            elif isinstance(string1,str):
                string = string1.split('\n')
            if string2 != None:
                self.string_active = string2
                if isinstance(string2,list) or isinstance(string2,tuple):
                    stringb = string2[0].split('\n')
                elif isinstance(string2,str):
                    stringb = string2.split('\n')
                tmps2 = []
                for line in stringb:
                    tmps2.append(self.font.render(line,False,(0,0,0)).get_width() + 10)
                var2 = max(tmps2)
                self.button.w = max(var2,self.button.w)
                self.button.h = max((self.font.render(stringb[0],False,(0,0,0)).get_height()*len(stringb))+10,self.button.h)
            tmps1 = []
            for line in string:
                tmps1.append(self.font.render(line,False,(0,0,0)).get_width() + 10)
                var = max(tmps1)
                self.button.w = max(var,self.button.w)
            self.button.h = max((self.font.render(string[0],False,(0,0,0)).get_height()*len(string))+10,self.button.h)


        self.active = False
    def press_button(self):
        if not(self.active):
            if hasattr(self,'colour_active'):
                self.colour = self.colour_active
            if hasattr(self,'string_active'):
                self.string = self.string_active
            self.active = True
    def release_button(self):
        if self.active:
            if self.colour != self.colour_passive:
                self.colour = self.colour_passive
            if hasattr(self,'string_passive'):
                self.string = self.string_passive
            self.active = False
    def get_rect(self):
        return self.button
    def change_height(self,val):
        self.button.h = self.init_height + val
    def change_posY(self,val):
        self.button.y = self.init_y - val
    def draw(self,screen):
        if isinstance(self.colour,list) or isinstance(self.colour,tuple):
            if len(self.colour) == 2:
                pygame.draw.rect(screen,self.colour[0],self.button,0)
                pygame.draw.rect(screen,self.colour[1],self.button,2)
            else:
                pygame.draw.rect(screen,self.colour[0],self.button,0)
        else:
            pygame.draw.rect(screen,self.colour,self.button,0)

        if hasattr(self,'string') and (isinstance(self.string,list) or isinstance(self.string,tuple)):
            if len(self.string) == 2:
                i = 0
                string = self.string[0].split('\n')
                for line in string:
                    surface = self.font.render(line,True,self.string[1])
                    screen.blit(surface,(self.button.x + 5, self.button.y + 5 + (i * surface.get_height())))
                    i += 1
            else:
                i = 0
                string = self.string.split('\n')
                for line in string:
                    surface = self.font.render(line,True,self.input_colour)
                    screen.blit(surface,(self.button.x + 5, self.button.y + 5 + (i * surface.get_height())))
                    i += 1
            #screen.blit(surface,(self.button.x+5,self.button.y+5))

class textfield(button):
    def __init__(self,colour,rect,boxcol1,boxcol2=None,font=None,size=32):
        super().__init__(rect,boxcol1,boxcol2)
        self.rect = super().get_rect()
        self.stayselected = True
        self.expandupwards = True
        self.user_text = ['']
        self.size = size
        self.font = pygame.font.Font(font,min(self.rect.h-2,size))
        self.input_colour = colour
        self.surface = self.font.render(self.user_text[0],True,self.input_colour)
    def message_handler(self):
        self.user_text = ['']
    def draw(self,screen):
        super().change_height((len(self.user_text)*self.surface.get_height())-20)
        if self.expandupwards:
            super().change_posY((len(self.user_text)*self.surface.get_height())-20)
        super().draw(screen)
        i = 0
        prevline = ' '
        for line in self.user_text:
            if i > 0 and line.startswith(' ') and prevline.endswith(''):
                line = line[1:]
                self.user_text[i-1] = self.user_text[i-1] + ' '
            prevline = line
            self.surface = self.font.render(line,True,self.input_colour)
            screen.blit(self.surface,(self.rect.x + 5, self.rect.y + 5 + (i * self.surface.get_height())))
            i += 1
        #self.button.w = max(100,self.surface.get_width() + 10)

class open_file_button(button):
    def __init__(self,filename,rect,boxcol1,boxcol2=None,string1=None,string2=None,font=None,size=32,type='NORMAL'):
        super().__init__(rect,boxcol1,boxcol2,string1,string2,font,size)
        self.filename = filename
        self.type = type
    def press_button(self):
        super().press_button()
        if self.type == 'NORMAL':
            self.file_handler()
        elif self.type == 'RECENT':
            self.recent_log()
    def file_handler(self):
        if os.path.exists(self.filename):
            webbrowser.open(self.filename)
    def recent_log(self):
        paths = sorted(Path(self.filename).iterdir(), key=os.path.getmtime)
        if len(paths) > 0:
            webbrowser.open(paths[0])
        else:
            print('Folder appears to be empty')


def main_loop(objs):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in objs:
                    if hasattr(obj,'press_button') and obj.button.collidepoint(event.pos):
                        obj.press_button()
                    elif obj.stayselected == True and hasattr(obj,'release_button'):
                        obj.release_button()
            if event.type == pygame.MOUSEBUTTONUP:
                for obj in objs:
                    if hasattr(obj,'release_button') and obj.stayselected == False and obj.button.collidepoint(event.pos):
                        obj.release_button()

            if event.type == pygame.KEYDOWN:
                for obj in objs:
                    if isinstance(obj,textfield) and obj.active:
                        if event.key == pygame.K_BACKSPACE:
                            obj.user_text[-1] = (obj.user_text[-1])[:-1]
                            if (obj.user_text[-1]) == '' and len(obj.user_text) > 1:
                                del obj.user_text[-1]
                            elif len(obj.user_text) > 1:
                                current_line = obj.user_text[-1].split(' ')
                                new_line = obj.user_text[-2] + current_line[0]
                                tmpsfc = obj.font.render(new_line,True,(0,0,0))
                                if tmpsfc.get_width() + 10 < obj.button.w:
                                    obj.user_text[-2] = new_line
                                    if len(current_line) > 1:
                                        obj.user_text[-1] = (obj.user_text[-1])[len(current_line[0]):]
                                    else:
                                        del obj.user_text[-1]
                        elif event.key == pygame.K_RETURN:
                            obj.message_handler()
                        elif event.key == pygame.K_ESCAPE:
                            obj.release_button()
                        else:
                            tmpsfc = obj.font.render(obj.user_text[-1] + event.unicode,True,(0,0,0))
                            if obj.button.w < tmpsfc.get_width() + 10:
                                word = event.unicode
                                if word != ' ' and ' ' in obj.user_text[-1]:
                                    for char in (obj.user_text[-1])[::-1]:
                                        if char != ' ':
                                            word += char
                                        else:
                                            tmpsfc = obj.font.render(word,True,(0,0,0))
                                            if tmpsfc.get_width() + 10 < obj.button.w:
                                                obj.user_text[-1] = (obj.user_text[-1])[:-len(word)]
                                                obj.user_text[-1] += ' '
                                                obj.user_text.append(word[::-1])

                                            else:
                                                obj.user_text.append(word)
                                            break
                                else:
                                    obj.user_text[-1] += ' '
                                    obj.user_text.append('')
                            else:
                                obj.user_text[-1] += event.unicode
                        break
        bot.refresh(objs)

if __name__ == '__main__':
    #necessary initialisation
    bot = interface()

    #create boxes here
    send_txt = textfield((255,255,255),(30,SCREEN_DIMENSIONS[1]-52,SCREEN_DIMENSIONS[0]-60,32),((50,80,100),(50,50,100)),((70,100,120),(60,60,110)),size=24)
    recent_log = open_file_button(f'{PATH}\\data\\user logs\\',(20,20,20,30),((50,80,100),(50,50,100)),((70,100,120),(60,60,110)),('Recent Logs',(255,255,255)),('Opening...',(255,255,255)),size=24,type='RECENT')
    error_log = open_file_button(f'{PATH}\\data\\error logs\\',(20,50,20,30),((50,80,100),(50,50,100)),((70,100,120),(60,60,110)),('Recent Errors',(255,255,255)),('Opening...',(255,255,255)),size=24,type='RECENT')



    #add objects to this list
    objs = [send_txt,recent_log,error_log]

    main_loop(objs)
