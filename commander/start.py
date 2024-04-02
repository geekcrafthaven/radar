# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


from commander.radar.feature.PointsPool import Point


try:
    import tkinter
    from tkinter import Frame, Tk, FLAT, Entry, Text, Scrollbar, END, ANCHOR
    from tkinter.font import Font
    from tkinter import GROOVE, Canvas, Label, StringVar, Toplevel
except Exception as msg:
    print('commander error: import tkinter: %s' % msg)
    import sys
    sys.exit(1)


class TkText:
    """
    __output handler
    """

    END = 'end'

    def __init__(self, _text):
        self.t = _text

    def insert(self, position, data, alias=''):
        self.t.insert(position, data, alias)

    def update(self):
        self.t.update()

    def get(self, start, end):
        return self.t.get(start, end)

    def set_color(self, alias, color):
        self.t.tag_configure(alias, foreground=color)

    def seek(self, position):
        self.t.see(position)

    def delete(self, start, end):
        self.t.delete(start, end)

    def set_enabled(self, enabled):
        if enabled:
            self.t.configure(state='normal')
        else:
            self.t.configure(state='disabled')


class PlainText:
    """
    __output handler
    """

    END = 'end'

    def __init__(self):
        pass

    def insert(self, position, data, alias=''):
        sys.stdout.write(data)

    def update(self):
        pass

    def get(self, start, end):
        return None

    def set_color(self, alias, color):
        pass

    def seek(self, position):
        pass

    def delete(self, start, end):
        pass

    def set_enabled(self, enabled):
        pass

# This is the child which appears when the button is pressed.


class RadarWindow(Frame):
    def __init__(self, _parent):
<<<<<<< HEAD

=======
>>>>>>> d018f15 (stuff)
        self.__width = 400
        self.__height = 400

        win = Toplevel(_parent)
        win.geometry("%dx%d" % (self.width, self. height))
        win.title('map')

<<<<<<< HEAD
        def ignore_quit():
            pass
        win.protocol("WM_DELETE_WINDOW", ignore_quit)
=======
        # my_str1 = StringVar()
        # l1 = Label(win,  textvariable=my_str1)
        # l1.grid(row=1, column=2)
        # my_str1.set("Hi I am Child window")
>>>>>>> d018f15 (stuff)

        self.w = Canvas(win,
                        width=self.width,
                        height=self.height)

        self.w.bind("<Configure>", self.on_resize)

        self.w.pack()

<<<<<<< HEAD
=======
        # y = int(200 / 2)
        # self.w.create_line(0, y, 200, y, fill="#476042")

        # win.overrideredirect(1)  # No win decoration.
        # win.bd = 10
        # Frame.__init__(self, win, relief=GROOVE)

>>>>>>> d018f15 (stuff)
    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def on_resize(self, event):
<<<<<<< HEAD
        self.__width = event.width
        self.__height = event.height
        self.w.config(width=self.width, height=self.height)

        # wscale = float(event.width)/self.width
        # hscale = float(event.height)/self.height
        # self.w.scale("all", 0, 0, wscale, hscale)

=======
        # determine the ratio of old width/height to new width/height
        # wscale = float(event.width)/self.width
        # hscale = float(event.height)/self.height
        self.__width = event.width
        self.__height = event.height
        # resize the canvas
        self.w.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        # self.w.scale("all", 0, 0, wscale, hscale)

    # ... and this is the handler for the button being pressed.
    # def onDropDown(self):
    #    popUp = ChildPopUpWindow(self)

>>>>>>> d018f15 (stuff)
    def draw_points(self):
        from commander.radar.feature.PointsPool import pool
        from commander.radar.feature.PointsPool import fields

        self.w.delete('all')

        self.w.create_rectangle(1, 1, self.width, self.height,
                                fill='#000000', outline='red', width=2)

        point_size = 10
        area_id = 0
        for item in fields.fields:
            if item.active:
                fill_color = '#3f3f3f'
            else:
                fill_color = '#000000'
            self.w.create_rectangle((item.x0 + self.width/2), item.y0,
                                    (item.x1 + self.width/2), item.y1,
                                    fill=fill_color, outline='yellow', width=2)
            self.w.create_text(item.x0 + self.width/2 + point_size, item.y0 + point_size,
                               text='%d' % area_id, fill='yellow')
            area_id += 1

        for item in pool.points:
            x0 = (item.x+self.width/2)-point_size
            y0 = (item.y)-point_size
            x1 = (item.x+self.width/2)+point_size
            y1 = (item.y)+point_size
            color = '#0000%02X' % int(0xff/Point.MAX_COUNTER * item.counter)
            self.w.create_oval(x0, y0, x1, y1, fill=color, outline=None)
            self.w.create_text(x0+point_size, y0+point_size,
                               text='%d' % item.identifier, fill='yellow')


class CommanderTk(Frame):
    """
    control terminal
    """

    def __init__(self):
        self.__tk = Tk()
        Frame.__init__(self, self.__tk, relief=FLAT)

        from commander.termbase.TermBase import TermBase
        TermBase.termbase.quit_commander_tk = self.on_quit

        from commander.termbase import TermAbout
        self.master.title('%s rev %s' %
                          (TermAbout.tool_name(), TermAbout.tool_revision))

        try:
            import os
            if os.name.lower() == 'posix':
                img = tkinter.PhotoImage(file='termbase/res/terminal2.png')
                self.master.tk.call('wm', 'iconphoto', self.master._w, img)
            elif os.name.lower() == 'nt':
                self.master.iconbitmap('termbase/res/terminal2.ico')
            else:
                pass
        except:
            pass

        self.in_font = Font(family="Courier", size=10)
        (w, h) = (self.in_font.measure(' ' * 140),
                  self.in_font.metrics("linespace") * 50)

        self.master.geometry('%dx%d' % (w, h))
        self.grid(sticky='nwes')
        self._create_widgets()

        dirname = os.path.dirname(__file__)
        filename = 'commander.history'
        filename = os.path.realpath(os.path.join(dirname, filename))

        self.master.protocol("WM_DELETE_WINDOW", self.__del__)

        from commander.termbase.InputHistory import InputHistory
        self.history = InputHistory(filename)
        try:
            self.history.load()
        except Exception:
            self.history.create()
            pass

        self.after(100, self._update_display)

        self.__map_window = RadarWindow(self.__tk)

    def __del__(self):
        from commander.termbase.TermBase import TermBase
        TermBase.termbase.__del__()
        try:
            self.master.quit()
        except Exception as message:
            print(message)

    def _create_widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.entry = Entry(self, takefocus=1, font=self.in_font)
        self.entry.grid(row=1, column=0, padx=0, pady=0,
                        ipadx=0, ipady=0, sticky='nswe')
        self.entry.bind('<Return>', self._enter_event)
        self.entry.bind('<Up>', self._up_event)
        self.entry.bind('<Down>', self._down_event)

        self.tkOutput = Text(self, takefocus=0, font=self.in_font)
        self.tkOutput.grid(row=0, column=0, padx=0, pady=0,
                           ipadx=0, ipady=0, sticky='nwes')
        self.tkOutput.bind('<Return>', self._enter_event)

        self.textYScroll = Scrollbar(self)
        self.textYScroll.grid(row=0, column=1, padx=0,
                              pady=0, ipadx=0, ipady=0, sticky='ns')

        self.textYScroll.config(command=self.tkOutput.yview)
        self.tkOutput.config(yscrollcommand=self.textYScroll.set)

        from commander.config import get_shortcuts, font_color
        for item in get_shortcuts():
            if item.enabled:
                if item.exclusive:
                    self.master.bind(item.key, self.__short_key_event)
                else:
                    self.master.bind(item.key, add='+',
                                     func=self.__short_key_event)

        text = TkText(self.tkOutput)
        text.set_color('internal', font_color())

        from commander.termbase.DisplayHandler import DisplayHandler
        assert DisplayHandler.display is not None, 'commander start error: display not set'
        DisplayHandler.display.text = text

        self.entry.focus_set()

    def __short_key_event(self, _event):

        SHIFT = 0x0001
        CAPS_LOCK = 0x0002
        CONTROL = 0x0004
        LEFT_HAND_ALT = 0x0008
        NUM_LOCK = 0x0010
        RIGHT_HAND_ALT = 0x0080
        MOUSE_BUTTON_1 = 0x0100
        MOUSE_BUTTON_2 = 0x0200
        MOUSE_BUTTON_3 = 0x0400

        mod = []
        if _event.state & SHIFT or _event.state & CAPS_LOCK:
            mod.append('Shift')
        if _event.state & CONTROL:
            mod.append('Control')
        if _event.state & LEFT_HAND_ALT or _event.state & RIGHT_HAND_ALT:
            mod.append('Alt')

        key_type = _event.type.name

        key_detail = _event.keysym

        from commander.config import get_shortcuts
        for item in get_shortcuts():
            if item.enabled:
                if item.is_equal(mod, key_type, key_detail):
                    self.entry.focus_set()
                    el = self.entry.get().strip()
                    if len(el) > 0:
                        self.entry.delete(0, END)
                        self.update()

                    from commander.termbase.TermBase import TermBase
                    TermBase.termbase.interpret_cmd(item.value)
                    self.update()

    def _up_event(self, event):
        self.entry.focus_set()
        self.entry.delete(0, END)
        self.entry.insert(0, self.history.remember_prev())
        self.entry.select_from(ANCHOR)
        self.entry.select_to(END)

    def _down_event(self, event):
        self.entry.focus_set()
        self.entry.delete(0, END)
        self.entry.insert(0, self.history.remember_next())
        self.entry.select_from(ANCHOR)
        self.entry.select_to(END)

    def _enter_event(self, event):
        self.entry.focus_set()
        el = self.entry.get().strip()
        if len(el) > 0:
            self.history.append(el)
            try:
                self.history.store()
            except Exception:
                self.history.create()
                self.history.store()
                pass

            self.entry.delete(0, END)
            self.update()

            from commander.termbase.TermBase import TermBase
            TermBase.termbase.interpret_cmd(el)
            self.update()

    def on_quit(self):
        try:
            self.master.quit()
        except Exception as message:
            print(message)

    def _update_display(self):
        from commander.termbase.TermBase import TermBase
        TermBase.termbase.perform()

        from commander.radar.feature.PointsPool import pool
        pool.perform()
        self.__map_window.draw_points()

        self.after(100, self._update_display)

    def start(self):
        from commander.termbase.TermBase import TermBase
        TermBase.termbase.start()
