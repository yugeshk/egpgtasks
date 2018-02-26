from gi.repository import Gtk
import sqlite3
import os
import datetime

class DemoApp():

    def __init__(self):
        window = Gtk.Window()
        window.set_border_width(10)
        window.set_title("To Do List")
        window.set_position(Gtk.WindowPosition.CENTER)
        window.connect('destroy', self.destroy)

        #Boxes To Hold Different Widgets
        window_box = Gtk.VBox(Gtk.Orientation.HORIZONTAL, spacing = 20)
        todo_box = Gtk.VBox(Gtk.Orientation.HORIZONTAL, spacing = 5)
        grid_box = Gtk.VBox(Gtk.Orientation.HORIZONTAL, spacing = 5)

        window.add(window_box)


        self.todo = Gtk.Entry()
        self.todo.set_placeholder_text("Add an Entry Here")
        self.todo_time = Gtk.Entry()
        self.todo_time.set_placeholder_text("By when?")

        self.button = Gtk.Button("Add task")
        self.button.connect("clicked", self.button_clicked)

        todo_box.pack_start(self.todo, True, True, 0)
        todo_box.pack_start(self.todo_time, True, True, 0)
        todo_box.pack_start(self.button, True, True, 0)

        self.store = Gtk.ListStore(str, str, str)
        self.populate_store()
        
        self.treeview = Gtk.TreeView(model=self.store)
        renderer_1 = Gtk.CellRendererText()        
        column_1 = Gtk.TreeViewColumn('Task', renderer_1, text=0) 
        column_1.set_sort_column_id(0)
        self.treeview.append_column(column_1)
        renderer_2 = Gtk.CellRendererText(xalign=1)
        column_2 = Gtk.TreeViewColumn('Do by', renderer_2, text=1)
        column_2.set_sort_column_id(1)
        self.treeview.append_column(column_2)
        renderer_3 = Gtk.CellRendererText(xalign=1)
        column_3 = Gtk.TreeViewColumn('Added on', renderer_3, text=2)
        column_3.set_sort_column_id(2)
        self.treeview.append_column(column_3)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.treeview)
        scrolled_window.set_min_content_height(200)

        self.delete_button = Gtk.Button('Delete Selected Task')
        self.delete_button.connect('clicked', self.delete_button_clicked)

        grid_box.pack_start(scrolled_window, True, True, 0)
        grid_box.pack_start(self.delete_button, True, True, 5)

        #Box Compositions
        window_box.pack_start(todo_box, True, True, 0)
        window_box.pack_start(grid_box, True, True, 0)

        window.show_all()

    def button_clicked(self, window):
    	directory = os.path.dirname(os.path.realpath(__file__))
    	database = sqlite3.connect(os.path.join(directory,'todolist.db'))
    	if database:
    		database.execute("INSERT INTO JOBS (DO,BY, ADDED) \
    			VALUES ("'"{}"'","'"{}"'","'"{}"'")".format(self.todo.get_text(), self.todo_time.get_text(), datetime.datetime.now()))
    		print('Job Added')
    		database.commit()
    		database.close()
    		self.todo.set_text('')
    		self.todo_time.set_text('')
    		self.populate_store()
    	else:
    		raise ValueError("database not found!!")
    def destroy(self, window):
    	Gtk.main_quit()

    def delete_button_clicked(self, button):

    	selection = self.treeview.get_selection()
    	model, paths = selection.get_selected_rows()
    	directory = os.path.dirname(os.path.realpath(__file__))
    	database = sqlite3.connect(os.path.join(directory,'todolist.db'))

    	for path in paths:
    		iter = model.get_iter(path)
    		database.execute("DELETE from JOBS where DO = '{}';".format(self.store[iter][0]))
    		model.remove(iter)

    	database.commit()
    	database.close()

    def populate_store(self):
    	directory = os.path.dirname(os.path.realpath(__file__))
    	database = sqlite3.connect(os.path.join(directory,'todolist.db'))
    	if database:
    		self.store.clear()
    		print("Opened Successfully")
    		table = database.execute("SELECT do, by, added from JOBS")
    		for row in table:
    			self.store.append([row[0],row[1],row[2]])
    		database.close()
    	else:
    		raise ValueError("database not found!!")

def main():
    app = DemoApp()
    Gtk.main()


if __name__ == '__main__':
	main()