#Krishen Bhan
import tkinter
from PointLine import point_line
import PointLine
from collections import defaultdict
DEFAULT_FONT = ('Helvetica', 14)
class lineGUI:
    def __init__(self):
        self._root = tkinter.Tk()
        self._canvas = tkinter.Canvas(master = self._root, width = 1000, height = 1000, background = '#ffffff')
        self._canvas.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._root.rowconfigure(1, weight = 5)
        self._root.columnconfigure(0, weight = 1)
        self.reset()
    
        self._system._points.append(PointLine.Point(.9, .9))
        self._system.build_nodes((-2, 20))
        reset_button = tkinter.Button(master = self._root, text = 'Reset', font = DEFAULT_FONT, command = self.reset)

        reset_button.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = tkinter.N + tkinter.E)
        self._root.rowconfigure(0, weight = 1)
        info = tkinter.Label(master = self._root, text = 'Click in two places to make a line', font = DEFAULT_FONT)

        info.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tkinter.N + tkinter.W)
        self._root.columnconfigure(1, weight = 1)
       

      
    def reset(self):
        self._penDown = False
        self._canvas.delete("all")
        self._system = PointLine.line_system(PointLine.Point(.1,.1), [])
        self._lines = []
        self._system._points.append(PointLine.Point(.9, .9))
        self._system.build_nodes((-2, 20))
        self.path = None
        
    def run(self) -> None:
        self._root.mainloop()

    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        pt = PointLine.from_pixel(event.x, event.y, width, height)
        if self._penDown:
            self._lines.append(point_line((self._point, pt)))
            self._system.add_point_line(self._lines[-1])
            #print(self._system.angle_range(self._system._lines[2], pt))
        else:
            self._point = pt
        self._penDown = not self._penDown
        self._refresh()

    def _on_canvas_resized(self, event: tkinter.Event):
        self._canvas.delete("all")
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        
        
            #test self._system.add_point_line(line)
        #self._system.refresh()
        
   
        for line in self._lines:
            self._canvas.create_line(line.start().pixel(width, height), line.end().pixel(width, height))
        if self.path:
            end, path = self.path
            while end.frac() in path:
                dest = path[end.frac()]
                self._canvas.create_line(end.pixel(width, height),  dest.pixel(width, height), fill="red", dash=(2,4))
                end = dest
            

        
    def _refresh(self):
        self._canvas.delete("all")
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        
        
            #test self._system.add_point_line(line)
        #self._system.refresh()
        print(self._system._points)
        print(self._system._nodes)
        for line in self._lines:
            self._canvas.create_line(line.start().pixel(width, height), line.end().pixel(width, height))
        if self._lines == []:
            return
        self._system.refresh()    
        
            
            
        '''
        for pt in self._system._nodes:
            for line, n in self._system._nodes[pt]:
                self._canvas.create_line(line.start().pixel(width, height), line.end().pixel(width, height), fill="blue", dash=(2,4))
        
        redLines = self.fastPath(set(), [self._system._points[0]], 0, self._system._points[-1] )[0]
        
        
        for st, end in zip(redLines[:-1], redLines[1:]):
            self._canvas.create_line(st.pixel(width, height),  end.pixel(width, height), fill="red", dash=(2,4))
        self._canvas.create_line(redLines[-1].pixel(width, height), self._system._points[-1].pixel(width, height), fill="red", dash=(2,4))
       '''
        self.path = self.bestPath()
        if not self.path:
            return
        end, path = self.path
        while end.frac() in path:
            dest = path[end.frac()]
            self._canvas.create_line(end.pixel(width, height),  dest.pixel(width, height), fill="red", dash=(2,4))
            end = dest
            
        
    
            
            
            
       
     
        #self._system.node_reset()
        #self._system.line_reset()
    
    
    def bestPath(self):
        path = dict()
        def infinite():
            return 9999
        weight = defaultdict(infinite)
        gScore = defaultdict(infinite)
        endPt = self._system._points[1]
        explored = set()
        closed = []
        openList = [self._system._points[0]]
        weight[openList[0].frac()] = openList[0].frac_distance_from(endPt)
        gScore[openList[0].frac()] = 0
        
        
        while not openList == []:
            cur = min((pt for pt in openList), key=lambda x: weight[(x.x_coord(), x.y_coord())])
            if cur == endPt:
                return (endPt, path)
            explored.add((cur.x_coord(), cur.y_coord()))
            closed.append(cur)
            openList.remove(cur)
            for edge, pt in self._system._nodes[cur.frac()]:
                if pt.frac() not in explored:
                    explored.add(pt.frac())
                    if pt not in openList:
                        openList.append(pt)
                    temp = edge.mag() + gScore[cur.frac()]
                    if gScore[pt.frac()] > temp:
                        path[pt.frac()] = cur
                        gScore[pt.frac()] = temp
                        weight[pt.frac()] = temp + pt.frac_distance_from(endPt)
        
        
                        
            
    def fastPath(self, explored, path, dist, endPt): 
        cur = path[-1]
        explored.add((cur.x_coord(), cur.y_coord()))
        if cur == endPt:
            return (path, dist)
        

        fast = []
        #return min((self.fastPath(explored, path + [pt], dist + len(edge), endPt) for edge, pt in self._system._nodes[(cur.x_coord(), cur.y_coord())] if (pt.x_coord(), pt.y_coord()) not in explored), key=lambda x: x[1])
        for edge, pt in self._system._nodes[(cur.x_coord(), cur.y_coord())]:
            if (pt.x_coord(), pt.y_coord()) not in explored:
                fast.append(self.fastPath(explored, path + [pt], dist + edge.mag(), endPt))
        return min(fast, key=lambda x: x[1]) if fast else ([], 10000)
                
        
        
        
        
                
                    
                    
                
            
                
        
        
if __name__ == '__main__':
    lineGUI().run()
    
