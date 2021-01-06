import tkinter as tk
import random

tplist = ['♠','♦','♣','♥']
pointlist = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
colist = ['black','red','black','red']

class Card():
    def __init__(self,cd_type,cd_point,back_flag,x,y,w,h,canvas):
        self.cd_type = cd_type
        self.tp_str = ''
        self.cd_point = cd_point
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.back_flag = back_flag
        self.canvas = canvas
        self.next = None
        self.move_flag = False
        self.disp_card()

    def disp_card(self):
        self.rec = self.canvas.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h,
                                                fill='white',outline='black')
        if self.back_flag:
            self.tp_str = pointlist[self.cd_point-1] + tplist[self.cd_type-1]
            self.label = self.canvas.create_text(self.x+14,self.y+8,text=self.tp_str,fill=colist[self.cd_type-1],font=('Gadugi',12))
        else:
            self.canvas.delete(self.rec)
            self.rec = self.canvas.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h,
                                                fill='yellow',outline='black')    

    def overturn(self):
        if self.back_flag:
            self.canvas.delete(self.label)
        self.back_flag = not self.back_flag
        self.canvas.delete(self.rec)
        self.disp_card()
    
    def move(self,move_x,move_y):
        # self.canvas.move(self.rec,move_x,move_y)
        # if self.back_flag:
        #     self.canvas.move(self.label,move_x,move_y)    
        if self.back_flag:
            self.canvas.delete(self.label)
        self.canvas.delete(self.rec)
        self.x = self.x + move_x
        self.y = self.y + move_y
        # print(self.x,self.y,move_x,move_y)
        self.disp_card()

    def update(self):
        if self.back_flag:
            self.canvas.delete(self.label)
        self.canvas.delete(self.rec)
        self.disp_card()

    def set_pos(self,pos_x,pos_y):
        # d_x = pos_x - self.x
        # d_y = pos_y - self.y
        # self.move(d_x,d_y)
        # self.x = pos_x
        # self.y = pos_y
        if self.back_flag:
            self.canvas.delete(self.label)
        self.canvas.delete(self.rec)
        self.x = pos_x
        self.y = pos_y
        self.disp_card()

    def remove(self):
        if self.back_flag:
            self.canvas.delete(self.label)
        self.canvas.delete(self.rec)

        
class App(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master,width=0,height=0)
        self.pack()
        self.master = master
        self.canvas = tk.Canvas(self.master,width=900,height=600,bg='green')
        self.canvas.pack()
        self.canvas.create_text(400,400,text='Jazzie!',fill='black',font=('Blackadder ITC',38))
        self.para_set()
        self.var_init()
        self.win_init()

    def para_set(self):
        self.card_w = 70
        self.card_h = 100
        self.x_gap = 15
        self.y_gap = 20
        self.left_margin = 20
        self.top_margin = 20
        self.col_num = 10

        self.rest_new = 5
        self.btm_x_gap = 5
        self.btm_margin = 20
        self.right_margin = 50
    
    def var_init(self):
        self.cards_pool = []
        self.cardset_pool = []
        self.list_pool = []
        self.select_pool = []
        self.btm_pool = []
        self.fns_pool = []
        self.fns_flag = False

        for c in range(10):
            self.list_pool.append([])
        
        # print(self.list_pool)

        for cg in range(2):
            for tp in range(4):
                for num in range(13):
                    self.cardset_pool.append((tp+1,num+1,cg))
        # print(self.cardset_pool)

    def win_init(self):
    
        for i in range(self.col_num):
            self.canvas.create_rectangle(self.left_margin+self.card_w*i+self.x_gap*i,
                                    self.top_margin,
                                    self.left_margin+self.card_w*(i+1)+self.x_gap*i,
                                    self.top_margin+self.card_h,
                                    outline='black')
        
        self.canvas.bind("<Button-1>", self.clk_1)
        self.canvas.bind("<B1-Motion>", self.drag_1)
        self.canvas.bind("<ButtonRelease-1>", self.rls_1)

        for r in range(4):
            for c in range(self.col_num):
                tp,num,_ = self.get_cardinf(1)[0]
                card = Card(tp,num,False,self.left_margin+self.card_w*c+self.x_gap*c,
                                                        self.top_margin+self.y_gap*r,
                                                        self.card_w,self.card_h,self.canvas)
                self.list_pool[c].append(card)

        for r in range(1):
            for c in range(4):
                tp,num,_ = self.get_cardinf(1)[0]
                card = Card(tp,num,False,self.left_margin+self.card_w*c+self.x_gap*c,
                                                        self.top_margin+self.y_gap*(r+4),
                                                        self.card_w,self.card_h,self.canvas)
                self.list_pool[c].append(card)
        
        
        for r in range(1):
            for c in range(6):
                tp,num,_ = self.get_cardinf(1)[0]
                card = Card(tp,num,True,self.left_margin+self.card_w*(c+4)+self.x_gap*(c+4),
                                                        self.top_margin+self.y_gap*(r+4),
                                                        self.card_w,self.card_h,self.canvas)
                self.list_pool[c+4].append(card)
        
        for r in range(1):
            for c in range(4):
                tp,num,_ = self.get_cardinf(1)[0]
                card = Card(tp,num,True,self.left_margin+self.card_w*c+self.x_gap*c,
                                                        self.top_margin+self.y_gap*(r+5),
                                                        self.card_w,self.card_h,self.canvas)
                self.list_pool[c].append(card)
        
        self.listlast_enab()
        # self.print_listpool()
        # print(self.list_pool)

        # # c1 = Card(1,2,True,200,200,self.card_w,self.card_h,self.canvas)
        # c1.overturn()
        # c1.move(-200,-200)
        # c1.overturn() 
        for i in range(self.rest_new):
            card = Card(1,1,False,900-self.right_margin-self.card_w+i*self.btm_x_gap,
                600-self.card_h-self.btm_margin,self.card_w,self.card_h,self.canvas)
            self.btm_pool.append(card)

    def listlast_enab(self):
        for l in self.list_pool:
            if len(l):
                l[-1].move_flag = True


    def get_cardinf(self,num):
        inf_slice = random.sample(self.cardset_pool,num)
        for item in inf_slice:
            self.cardset_pool.remove(item)
        return inf_slice

    def clk_1(self,event):
        if self.fns_flag:
            return
        # print(event.x,event.y)
        if self.btm_pool and (900-self.right_margin-self.card_w < event.x < 900-self.right_margin+self.btm_x_gap*len(self.btm_pool)) \
                        and (600 - self.btm_margin-self.card_h < event.y < 600 - self.btm_margin):
            # print('new group')
            self.add_list()
            card = self.btm_pool[-1]
            card.remove()
            self.btm_pool.remove(card)
            return


        self.last_x,self.last_y = event.x,event.y
        self.select_pool.clear()
        # print(event.x,event.y)
        x_num,y_num = self.find_pos(event.x,event.y)
        if x_num == None or y_num == None:
            return
        
        card = self.list_pool[x_num][y_num]
        if card.move_flag:
            self.select_pool.append(card)
            self.list_pool[x_num].remove(card)            
            while card.next:
                card = card.next
                self.select_pool.append(card)
                self.list_pool[x_num].remove(card)
        # print(len(self.list_pool[x_num]))
        # print(x_num,y_num)
        self.lv_x = x_num
        self.lv_y = y_num
        # self.select_pool.append
    
    def drag_1(self,event):
        if not len(self.select_pool):
            return
        c = self.select_pool[0]
        for card in self.select_pool:
            # x_bias,y_bias = card.x-event.x,card.y-event.y
            card.move(event.x-self.last_x,event.y-self.last_y)
        self.last_x,self.last_y = event.x,event.y
        # print(self.select_pool)

    def rls_1(self,event):
        if self.fns_flag:
            return

        if not len(self.select_pool):
            return
        # self.updateflag(self.lv_x)
        x_num,y_num = self.find_pos(event.x,event.y)
        # print(x_num,y_num)
        if (x_num != None) and (y_num != None):
            if (not len(self.list_pool[x_num])):
                for item in self.select_pool:
                    self.list_pool[x_num].append(item)
                self.updatelist(self.lv_x)
                self.updatelist(x_num)
                if len(self.list_pool[self.lv_x]) and self.list_pool[self.lv_x][-1].back_flag == False:
                    self.list_pool[self.lv_x][-1].overturn()
                    self.listlast_enab()
                if len(self.list_pool[self.lv_x]):
                    self.list_pool[self.lv_x][-1].next = None

            elif (y_num == len(self.list_pool[x_num])-1) and \
                (self.select_pool[0].cd_type == self.list_pool[x_num][-1].cd_type) and \
                (self.select_pool[0].cd_point == self.list_pool[x_num][-1].cd_point-1):
                self.list_pool[x_num][-1].next=self.select_pool[0]
                for item in self.select_pool:
                    self.list_pool[x_num].append(item)
                # self.print_listpool()
                self.updatelist(x_num)
                self.updateflag(self.lv_x)
                if len(self.list_pool[self.lv_x]) and self.list_pool[self.lv_x][-1].back_flag == False:
                    self.list_pool[self.lv_x][-1].overturn()
                    self.listlast_enab()
                if len(self.list_pool[self.lv_x]):
                    self.list_pool[self.lv_x][-1].next = None
                # print(self.select_pool)
            else:
                cd = self.select_pool[0]
                self.list_pool[self.lv_x].append(cd)
                while cd.next:
                    cd = cd.next
                    self.list_pool[self.lv_x].append(cd)
                # print(2)
                self.updatelist(self.lv_x)

        else:
            cd = self.select_pool[0]
            self.list_pool[self.lv_x].append(cd)
            while cd.next:
                cd = cd.next
                self.list_pool[self.lv_x].append(cd)
            # print(2)
            self.updatelist(self.lv_x)
            #return

        self.select_pool.clear()
        self.print_listpool()

    def updatelist(self,col):
        if not len(self.list_pool[col]):
            return
        
        for r in range(len(self.list_pool[col])):
            card = self.list_pool[col][r]
            card.x = self.left_margin+col*(self.x_gap+self.card_w)
            card.y = self.top_margin+r*(self.y_gap)
            # print(card.x,card.y)
            card.update()
        self.updateflag(col)
        # if self.list_pool[col][-1].back_flag == False:
        #     self.list_pool[col][-1].overturn()
        # self.print_listpool()

    def find_pos(self,x,y):
        cn = (x-self.left_margin)//(self.card_w+self.x_gap)
        rn = None
        if 0 <=cn <= 9 and (self.left_margin + cn*(self.card_w+self.x_gap) < 
                        x <self.left_margin + cn*(self.card_w+self.x_gap)+self.card_w):
            pass
        else:
            cn = None
        if cn != None and (not len(self.list_pool[cn])):
            # print('cn:%i' % (cn))
            return cn,0
        if cn != None:
            rn_max = len(self.list_pool[cn])
            rn = (y - self.top_margin)//self.y_gap
            if rn >= 0 and rn < rn_max:
                pass
            elif rn >= rn_max and (self.top_margin+(rn_max-1)*self.y_gap < y < self.top_margin+(rn_max-1)*self.y_gap+self.card_h):
                rn = rn_max - 1
            else:
                rn = None
        # print('cn:%i,rn:%i' % (cn,rn))
                
        return cn,rn

    def add_list(self):
        for col in range(len(self.list_pool)):
            tp,num,_ = self.get_cardinf(1)[0]
            card = Card(tp,num,True,900,600,self.card_w,self.card_h,self.canvas)
            print('add')
            if len(self.list_pool[col]):
                if card.cd_type == self.list_pool[col][-1].cd_type and \
                    card.cd_point == self.list_pool[col][-1].cd_point -1:
                    self.list_pool[col][-1].next = card
            self.list_pool[col].append(card)
            self.updatelist(col)
            # self.updateflag(col)


    def updateflag(self,col):
        if not len(self.list_pool[col]):
            return
        for card in self.list_pool[col]:
            card.move_flag = False
        chain = []
        chain.append(self.list_pool[col][-1])
        for i in range(len(self.list_pool[col])-1):
            if self.list_pool[col][-i-2].back_flag and \
                chain[-1].cd_type == self.list_pool[col][-i-2].cd_type and \
                chain[-1].cd_point == self.list_pool[col][-i-2].cd_point -1:
                chain.append(self.list_pool[col][-i-2])
            else:
                break
        for item in chain:
            item.move_flag = True
        if len(chain) == 13:
            tp = chain[0].cd_type
            for card in chain:
                card.remove()
                self.list_pool[col].remove(card)
            if len(self.list_pool[col]):
                self.list_pool[col][-1].next = None
                if self.list_pool[col][-1].back_flag == False:
                    self.list_pool[col][-1].overturn()
            pos_x = self.right_margin+self.btm_x_gap*len(self.fns_pool)
            pos_y = 600-self.btm_margin-self.card_h
            card = Card(tp,13,True,pos_x,pos_y,self.card_w,self.card_h,self.canvas)
            self.fns_pool.append(card)
        if len(self.fns_pool) == 8:
            self.finish()

    def finish(self):
        self.fns_flag = True
        self.canvas.create_text(400,250,text='WIN!',fill='red',font=('Impact',38))

    def print_listpool(self):
        for i in range(len(self.list_pool)):
            print('\nlist:%i:\n' % (i))
            for item in self.list_pool[i]:
                print(item.cd_type,item.cd_point)

if __name__=='__main__':
    root = tk.Tk()
    root.title('Spider!')
    root.geometry('900x600')
    root.resizable(0,0)
    app = App(root)
    root.mainloop()
