import tkinter
import url
from html_parser.html_parser import HtmlParser
from html_parser.html_tree_builder import HtmlTreeBuilder
from html_parser.tree_node import TreeNode,TreeNodeType
import helper

WIDTH , HEIGHT = 800 , 600

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
        self.root.config(bg="white")
            
        self.search_bar_frame =  tkinter.Frame(self.root,width=WIDTH,height=50,bg="white")
        self.search_bar_input = tkinter.Entry(self.search_bar_frame)
        self.search_bar_input.insert(0,"https://example.com/")
        self.search_bar_button = tkinter.Button(self.search_bar_frame,text="Search",command=self.on_search)
        


        self.search_bar_input.grid(row=0, column=0,padx=5)
        self.search_bar_button.grid(row=0, column=1,padx=5)
        self.search_bar_frame.pack(anchor="e",pady=2)


        self.canvas = tkinter.Canvas(
                                        self.root,
                                        bg="white",
                                        width=WIDTH,height=HEIGHT - self.search_bar_frame.winfo_height(),
                                        yscrollincrement=self.yscroll_speed,xscrollincrement=self.xscroll_speed
                                    )
        self.canvas.pack()




        # bind the events
        self.root.bind("<KeyPress>",self.on_key_press_event)
        self.root.bind("<Button-4>",self.on_mouse_wheel_event)
        self.root.bind("<Button-5>",self.on_mouse_wheel_event)


        self.is_running = True
        self.error_exit = False


        self.url = url.URL()

    # browser functions
    def to_website(self,url : str):
        body =  self.url.request(url)
        if not body: body = f"[Error] Failed to get '{url}' sorry not sorry"
        
        return body

    def on_search(self):
        # return if not input is given
        if not self.search_bar_input.get(): return


        html_src = self.to_website(self.search_bar_input.get())
        self.render_document(html_src)

    def render_document(self,src):
        tokens = HtmlParser().parse(src=src)
        builder = HtmlTreeBuilder()
        tree =  builder.build(tokens)
        
        out_str = builder.print()
        self.canvas.create_text(0,0,text=out_str,anchor="nw")
        # self.traverse_and_render_tree(tree)

    def traverse_and_render_tree(self,node):
        # start by root
        if node.typ == TreeNodeType.Root:
            for node in node.value:
                self.render_tag(node)
        else:
            print(f"[Unreachable] Unkown TreeNode {node}")
            exit(-1)

    def render_tag(self,node):
        # ignore this tags, they are not visible
        if node.tag in ["html"]:
            for child in node.value:
                self.render_tag(child)
        else:
            print(f"[Unreachable] Unhandled tag {node.tag}")
            # self.error_exit = True
            exit(-1)


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
        while self.is_running and not self.error_exit:
            self.update()
            self.render()
        
        self.root.quit()

    def update(self):
        self.root.update()

    def render(self):
        pass