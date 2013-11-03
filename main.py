#http://my-python3-code.blogspot.com/2012/08/basic-tkinter-text-editor-online-example.html
import tkFileDialog
from Tkinter import *
import os.path
import sys

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))

class App:

    def doNew(self):
            # Clear the text
            self.text.delete(0.0, END)

    def doSaveAs(self):
            # Returns the saved file
            file = tkFileDialog.asksaveasfile(mode='w')
            textoutput = self.text.get(0.0, END) # Gets all the text in the field
            file.write(textoutput.rstrip()) # With blank perameters, this cuts off all whitespace after a line.
            file.write("\n") # Then we add a newline character.

    def doOpen(self):
            # Returns the opened file
            file = tkFileDialog.askopenfile(mode='r')
            fileContents = file.read() # Get all the text from file.

            # Set current text to file contents
            self.text.delete(0.0, END)
            self.text.insert(0.0, fileContents)  
            
    def verify_requirements(self):
        if not os.path.isfile(os.path.join(self.path,"as.exe")):
            return str(os.path.join(self.path,"as.exe"))
        if not os.path.isfile(os.path.join(self.path,"objcopy.exe")):
            return str(os.path.join(self.path,"objcopy.exe"))
        if not os.path.isfile(os.path.join(self.path,"Thumbs.db")):
            return str(os.path.join(self.path,"Thumbs.db"))
        return False
    
    def do_error(self, error_msg):
        error_pop_up = Toplevel()
        error_pop_up.title("Error")

        msg = Message(error_pop_up, text=error_msg)
        msg.pack()

        button = Button(error_pop_up, text="Dismiss", command=error_pop_up.destroy)
        button.pack()
        
    def doRomInsert(self):
        missing_file = self.verify_requirements()
        if missing_file:
            self.do_error("The file "+missing_file+" is missing. Compile aborted.")
            return False
            
        file = tkFileDialog.askopenfile(mode='w+')
        
        
    def doTestCompile(self):
        missing_file = self.verify_requirements()
        if missing_file:
            self.do_error("The file "+missing_file+" is missing. Compile aborted.")
            return False
        
    def doBinCompile(self):
        missing_file = self.verify_requirements()
        if missing_file:
            self.do_error("The file "+missing_file+" is missing. Compile aborted.")
            return False
            
        open_file = tkFileDialog.asksaveasfile(mode='w')
        #os.chdir(self.path)
        name_of_file = open_file.name
        
        source = os.path.join(self.path,"temp.asm")
        
        with open(os.path.join(self.path,"temp.asm"), "w+") as data:
            textoutput = self.text.get(0.0, END)
            data.write(textoutput.rstrip())
            data.write("\n")
        
        os.system("as -mthumb -mthumb-interwork "+source)
        if os.path.isfile(name_of_file):
            os.remove(name_of_file)
        os.system("objcopy -O binary a.out "+name_of_file)
        os.remove(source)
        os.remove("a.out")
        
    def __init__(self):
            # Set up the screen, the title, and the size.
            self.root = Tk()
            self.root.title("THUMB Editor")
            self.root.minsize(width=500,height=400)
            self.path = module_path()
                   
            # Set up basic Menu
            menubar = Menu(self.root)
   
            # Set up a separate menu that is a child of the main menu
            filemenu = Menu(menubar,tearoff=0)
            filemenu.add_command(label="New File", command=self.doNew, accelerator="Ctrl+N")
            
            #Create a menu for compiling.
            compile_menu = Menu(menubar,tearoff=0)
            compile_menu.add_command(label="Test Compile", command=self.doTestCompile, accelerator="Ctrl+Shift+P")
            compile_menu.add_command(label="Output to .bin", command=self.doBinCompile, accelerator="Ctrl+P")
            compile_menu.add_command(label="Insert into Rom", command=self.doRomInsert, accelerator="Ctrl+U")
   
            # Try out openDialog
            filemenu.add_command(label="Open", command=self.doOpen, accelerator="Ctrl+O")
   
            # Try out the saveAsDialog
            filemenu.add_command(label="Save", command=self.doSaveAs, accelerator="Ctrl+Shift+S")
            menubar.add_cascade(label="File", menu=filemenu)
            menubar.add_cascade(label="Compile", menu=compile_menu)
            self.root.config(menu=menubar)
   
            # Set up the text widget
            self.text = Text(self.root)
            self.text.pack(expand=YES, fill=BOTH) # Expand to fit vertically and horizontally

app = App()
app.root.mainloop()
