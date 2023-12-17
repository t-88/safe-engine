import tkinter
import url

WIDTH , HEIGHT = 600 , 400

class Browser:
    def __init__(self):

        # init tkinter
        self.root = tkinter.Tk()
        self.root.title("safe engine")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(width=False,height=False)


        self.yscroll_speed = 20
        self.xscroll_speed = 40
        self.scroll_y = 0
        self.scroll_x = 0


        # rendering
        self.canvas = tkinter.Canvas(
                                        self.root,
                                        width=WIDTH,height=HEIGHT,
                                        yscrollincrement=self.yscroll_speed,xscrollincrement=self.xscroll_speed
                                    )
        self.canvas.pack()

        # bind the events
        self.root.bind("<KeyPress>",self.on_key_press_event)
        self.root.bind("<Button-4>",self.on_mouse_wheel_event)
        self.root.bind("<Button-5>",self.on_mouse_wheel_event)


        self.is_running = True


        self.url = url.URL()

    # browser functions
    def to_website(self,url : str):
        body =  self.url.request(url)
        if not body: body = f"[Error] Failed to get '{url}' sorry not sorry"
        
        self.canvas.delete("all")
        self.canvas.create_text(0,0,text=body,anchor="nw")


    # user interface functions



    def screen_scroll(self,dir):
        # scrolls the website screen on x axis and y axis

        offset = -1 if dir in ["up", "left"] else 1

        # y axis
        if dir in ["down","up"]:
            # skip scrolling up if you are on most top of the page 
            if dir == "up" and self.scroll_y <= 0: return
            self.scroll_y += offset * self.yscroll_speed
            self.canvas.yview_scroll(offset,"units")

        # x axis
        if dir in ["left","right"]:
            # skip scrolling left if you are on most left of the page 
            if dir == "left" and self.scroll_x <= 0: return
            self.scroll_x += offset * self.xscroll_speed
            self.canvas.xview_scroll(offset,"units")

    def on_key_press_event(self,event):
        if event.keysym == "Escape":
            self.is_running = False

        if event.keysym == "Left":
            self.screen_scroll("left")
        elif event.keysym == "Right":
            self.screen_scroll("right")


    def on_mouse_wheel_event(self,event):
        assert event.num in [4,5]

        scroll_dir = "up" if event.num == 4 else "down"
        self.screen_scroll(scroll_dir)




    def run(self):
        while self.is_running:
            self.update()
            self.render()
        
        self.root.quit()

    def update(self):
        self.root.update()

    def render(self):
        pass