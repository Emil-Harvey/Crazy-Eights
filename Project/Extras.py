from tkinter import *

'''
marquee - from stack overflow.
example usage:
marquee = Marquee(root, text="Hello, world", borderwidth=2, relief="sunken")
marquee.pack(side="top", fill="x", pady=20)
'''
class Marquee(Canvas):
    text =None
    def __init__(self, parent, text, font, margin=2, borderwidth=1, relief='flat', fps=30):
        super().__init__(parent, borderwidth=borderwidth, relief=relief, bg= "darkgreen")

        self.fps = fps

        # start by drawing the text off screen, then asking the canvas
        # how much space we need. Use that to compute the initial size
        # of the canvas.
        self.text = self.create_text(0, -1000, text=text, font=font, fill="yellow2", anchor="w", tags=("text",))
        ##self.itemconfigure(text, text=parent.getvar('ticker'))
        (x0, y0, x1, y1) = self.bbox("text")
        width = (x1 - x0) + (2 * margin) + (2 * borderwidth)
        height = (y1 - y0) + (2 * margin) + (2 * borderwidth)
        self.configure(width=width, height=height)

        # start the animation
        self.animate()

    def animate(self):
        (x0, y0, x1, y1) = self.bbox("text")
        if x1 < 0 or y0 < 0:
            # everything is off the screen; reset the X
            # to be just past the right margin
            x0 = self.winfo_width()
            y0 = int(self.winfo_height() / 2)
            self.coords("text", x0, y0)
        else:
            self.move("text", -2, 0)

        # do again in a few milliseconds
        self.after_id = self.after(int(1000 / self.fps), self.animate)


#root = tk.Tk()
